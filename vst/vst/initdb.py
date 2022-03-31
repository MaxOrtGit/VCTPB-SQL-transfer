from decimal import Decimal
from multiprocessing import connection
from xmlrpc.client import Boolean
from savefiles import get_setting
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dbinterface import get_all_objects
import jsonpickle
from sqlalchemy.exc import IntegrityError 

import base

from DBUser import User, is_valid_user
from DBMatch import Match, is_valid_match
from DBBet import Bet, is_valid_bet

def create_db():
  
  if not get_setting("init_sql_db"):
    print("savedata.db does not exist.\nquitting")
    quit()

  engine = create_engine('sqlite:///savedata.db')
  base.Base.metadata.create_all(engine, checkfirst=True)
  
  

def files_to_db():
  
  engine = create_engine('sqlite:///savedata.db')
  session = sessionmaker(bind = engine)()
  
  matches = get_all_objects("match")
  
  
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
      print(jsonpickle.encode(match))
      print(list(enumerate(errors)))
      print(list(enumerate([match.code, match.t1, match.t2, match.t1o, match.t2o, match.t1oo, match.t2oo, match.tournament_name, match.odds_source, match.winner, match.color, match.creator, match.date_created, match.date_winner, match.date_closed, match.bet_ids, match.message_ids])))
      return
    
    dbmatch = Match(match.code, match.t1, match.t2, match.t1o, match.t2o, match.t1oo, match.t2oo, match.tournament_name, match.winner, match.odds_source, match.color, match.creator, match.date_created, match.date_winner, match.date_closed, match.bet_ids, match.message_ids)
    session.add(dbmatch)
    
  session.commit()
    
    
  bets = get_all_objects("bet") 
    
  for bet in bets:
    errors = is_valid_bet(bet.code, bet.t1, bet.t2, bet.tournament_name, bet.winner, bet.bet_amount, bet.team_num, bet.color, bet.match_id, bet.user_id, bet.date_created, bet.message_ids)
    error = False
    for e in errors:
      if e:
        error = True
    if error:
      print("Error in bet:", bet.code)
      print(jsonpickle.encode(bet))
      print(list(enumerate(errors)))
      print(list(enumerate([bet.code, bet.t1, bet.t2, bet.tournament_name, bet.winner, bet.bet_amount, bet.team_num, bet.color, bet.match_id, bet.user_id, bet.date_created, bet.message_ids])))
      return

    dbbet = Bet(bet.code, bet.t1, bet.t2, bet.tournament_name, bet.winner, bet.bet_amount, bet.team_num, bet.color, bet.match_id, bet.user_id, bet.date_created, bet.message_ids)
    session.add(dbbet)
  
  session.commit()
  
  
  users = get_all_objects("user")
  
  for user in users:
    print(user.show_on_lb)
    errors = is_valid_user(user.code, user.username, user.color, user.show_on_lb, user.balance, user.active_bet_ids, user.loans)
    error = False
    for e in errors:
      if e:
        error = True
    if error:
      print("Error in user:", user.code)
      print(jsonpickle.encode(user))
      print(list(enumerate(errors)))
      print(list(enumerate([user.code, user.username, user.color, user.show_on_lb, user.balance, user.active_bet_ids, user.loans])))
      return
    
    dbuser = User(user.code, user.username, user.color, user.show_on_lb, user.balance, user.active_bet_ids, user.loans)
    session.add(dbuser)
    
  try:
    session.commit()
  except IntegrityError as IE:
    print("error:", IE)
    pass
  
  
  matchess = session.query(Match).all()
  mbets = [m.bets for m in matchess]
  mcreator = [m.creator for m in matchess]
  
  #print(mbets)
  #print(mcreator)
  
  betss = session.query(Bet).all()
  bcodes = [b.code for b in betss]
  bmatch = [b.match for b in betss]
  buser = [b.user for b in betss]
  
  #print(bmatch)
  #print(buser)
  
  #print(bresult)
  
  userss = session.query(User).all()
  ucodes = [u.code for u in userss]
  ubets = [u.bets for u in userss]
  umatches = [u.matches for u in userss]
  
  #print(ubets)
  #print(umatches)
  #print(uresult)
  
  
  
  print("\n\nmatchs bets, bets match")
  #print(mbets)
  #print(bmatch)
  
  
  print("\n\nuser bets, bets user")
  #print(ubets)
  #print(buser)
  
  print("\n\nuser matches, matches user")
  #print(umatches)
  #print(mcreator)
  