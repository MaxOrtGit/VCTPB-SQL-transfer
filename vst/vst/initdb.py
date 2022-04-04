from decimal import Decimal
from multiprocessing import connection
from xmlrpc.client import Boolean
from savefiles import get_setting, get_file
from olddbinterface import get_all_objects
from dbinterface import *
from oldcolorinterface import get_all_colors_key_hex
import ujson
from sqlalchemy.exc import IntegrityError 
from sqlalchemy import select

from sqlaobjs import *

from Color import Color
from DBUser import User, is_valid_user
from DBBet import Bet, is_valid_bet
from DBMatch import Match, is_valid_match
from Channels import Channels

def create_db():

  with Engine.begin() as connection:
    mapper_registry.metadata.create_all(connection)
  
  

def files_to_db():
  
  matches = get_all_objects("match")
  bets = get_all_objects("bet") 
  users = get_all_objects("user")
  colors = get_all_colors_key_hex()
  
  dbmatches = []
  dbbets = []
  dbusers = []
  dbcolors = []
  
  for color in colors:
    dbcolor = Color(color[0].capitalize(), color[1])
    dbcolors.append(dbcolor)
  
  for match in matches:
    match.t1o = Decimal(str(match.t1o))
    match.t2o = Decimal(str(match.t2o))
    match.t1oo = Decimal(str(match.t1oo))
    match.t2oo = Decimal(str(match.t2oo))
    
    
    errors = is_valid_match(match.code, match.t1, match.t2, match.t1o, match.t2o, match.t1oo, match.t2oo, match.tournament_name, match.odds_source, match.winner, match.color, match.creator, match.date_created, match.date_winner, match.date_closed, match.bet_ids, match.message_ids)
    error = False
    for e in errors:
      if e:
        error = True
    if error:
      print("Error in match:", match.code)
      #print(ujson.dumps(match))
      print(list(enumerate(errors)))
      print(list(enumerate([match.code, match.t1, match.t2, match.t1o, match.t2o, match.t1oo, match.t2oo, match.tournament_name, match.odds_source, match.winner, match.color, match.creator, match.date_created, match.date_winner, match.date_closed, match.bet_ids, match.message_ids])))
      quit()
      return
    
    dbmatch = Match(match.code, match.t1, match.t2, match.t1o, match.t2o, match.t1oo, match.t2oo, match.tournament_name, match.winner, match.odds_source, match.color, match.creator, match.date_created, match.date_winner, match.date_closed, match.bet_ids, match.message_ids)
    dbmatches.append(dbmatch)

    
  for bet in bets:
    errors = is_valid_bet(bet.code, bet.t1, bet.t2, bet.tournament_name, bet.winner, bet.bet_amount, bet.team_num, bet.color, bet.match_id, bet.user_id, bet.date_created, bet.message_ids)
    error = False
    for e in errors:
      if e:
        error = True
    if error:
      print("Error in bet:", bet.code)
      #print(ujson.dumps(bet))
      print(list(enumerate(errors)))
      print(list(enumerate([bet.code, bet.t1, bet.t2, bet.tournament_name, bet.winner, bet.bet_amount, bet.team_num, bet.color, bet.match_id, bet.user_id, bet.date_created, bet.message_ids])))
      quit()
      return

    dbbet = Bet(bet.code, bet.t1, bet.t2, bet.tournament_name, bet.winner, bet.bet_amount, bet.team_num, bet.color, bet.match_id, bet.user_id, bet.date_created, bet.message_ids)
    dbbets.append(dbbet)
    
  for user in users:
    errors = is_valid_user(user.code, user.username, user.color, user.show_on_lb, user.balance, user.active_bet_ids, user.loans)
    error = False
    for e in errors:
      if e:
        error = True
    if error:
      print("Error in user:", user.code)
      #print(ujson.dumps(user))
      print(list(enumerate(errors)))
      print(list(enumerate([user.code, user.username, user.color, user.show_on_lb, user.balance, user.active_bet_ids, user.loans])))
      quit()
      return
    
    dbuser = User(user.code, user.username, user.color, user.show_on_lb, user.balance, user.active_bet_ids, user.loans)
    dbusers.append(dbuser)
    
    channel = Channels(get_file("bet_channel_id"), get_file("match_channel_id"))
    
    
  with Session.begin() as session:
    session.add_all(dbmatches)
    session.add_all(dbbets)
    session.add_all(dbusers)
    session.add_all(dbcolors)
    session.add(channel)
  
  
  