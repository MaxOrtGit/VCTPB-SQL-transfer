from multiprocessing import connection
from xmlrpc.client import Boolean
from savefiles import get_setting
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData, Table, Column, Numeric, Integer, String, Boolean, DateTime
from dbinterface import get_all_objects
import jsonpickle

from DBUser import User, is_valid_user
from DBMatch import Match, is_valid_match
from DBBet import Bet, is_valid_bet


from sqltypes import JSONLIST

def create_db():
  
  if not get_setting("init_sql_db"):
    print("savedata.db does not exist.\nquitting")
    quit()

  engine = create_engine('sqlite:///savedata.db', echo = True)
  meta = MetaData()

  match = Table(
    'match', meta, 
    Column('code', String(8), primary_key = True),
    Column('t1', String(50)),
    Column('t2', String(50)),
    Column('t1o', Numeric(5, 3)),
    Column('t2o', Numeric(5, 3)),
    Column('t1oo', Numeric(5, 3)),
    Column('t2oo', Numeric(5, 3)),
    Column('tournament_name', String(100)),
    Column('odds_source', String(50)),
    Column('winner', Integer),
    Column('color', String(6)),
    Column('creator', Integer),
    Column('date_created', DateTime(timezone = True)),
    Column('date_winner', DateTime(timezone = True)),
    Column('date_closed', DateTime(timezone = True)),
    Column('bet_ids', JSONLIST), #list of int 
    Column('message_ids', JSONLIST), #list of int
  )
  
  bet = Table(
    'bet', meta, 
    Column('code', String(8), primary_key = True),
    Column('t1', String(50)),
    Column('t2', String(50)),
    Column('tournament_name', String(100)),
    Column('winner', Integer),
    Column('amount_bet', Integer),
    Column('team_num', Integer),
    Column('color', String(6)),
    Column('match_id', String(8)),
    Column('user_id', Integer),
    Column('date_created', DateTime(timezone = True)),
    Column('message_ids', JSONLIST), #list of int
  )
  
  user = Table(
    "user", meta,
    Column('code', String(8), primary_key = True),
    Column('username', String(32)),
    Column('color', String(6)),
    Column('hidden', Boolean),
    Column('balances', JSONLIST), #list of Tuple(bet_id, balance after change, date)
    Column('active_bet_ids', JSONLIST), #list of strings code of active bets
    Column('loans', JSONLIST), #list of Tuple(balance, date created, date paid)
  )
  
  meta.create_all(engine)
  


def files_to_db():
  
  engine = create_engine('sqlite:///savedata.db')
  session = sessionmaker(bind = engine)
  
  matches = get_all_objects("match")
  for match in matches:
    errors = is_valid_match(match.code, match.t1, match.t2, match.t1o, match.t2o, match.t1oo, match.t2oo, match.tournament_name, match.winner, match.odds_source, match.color, match.creator, match.date_created, match.date_winner, match.date_closed, match.bet_ids, match.message_ids)
    error = False
    for e in errors:
      if e:
        error = True
    if error:
      print("Error in match:", match.code)
      print(jsonpickle.encode(match))
      return
    
    dbmatch = Match(match.code, match.t1, match.t2, match.t1o, match.t2o, match.t1oo, match.t2oo, match.tournament_name, match.winner, match.odds_source, match.color, match.creator, match.date_created, match.date_winner, match.date_closed, match.bet_ids, match.message_ids)
    session.add(dbmatch)
  session.commit()