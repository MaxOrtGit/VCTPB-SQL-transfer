from multiprocessing import connection
from xmlrpc.client import Boolean
from savefiles import get_setting
from sqlalchemy import create_engine, MetaData, Table, Column, Numeric, Integer, String, Boolean, DateTime, ARRAY


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
    Column('date_created', DateTime),
    Column('date_winner', DateTime),
    Column('date_closed', DateTime),
    Column('bet_ids', String), #array of int 
    Column('message_ids', String), #array of int
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
    Column('date_created', DateTime),
    Column('message_ids', String), #array of int
  )
  
  user = Table(
    "user", meta,
    Column('code', String(8), primary_key = True),
    Column('username', String(25)),
    Column('color', String(6)),
    Column('hidden', Boolean),
    Column('balances', String), #array of Tuple(bet_id, balance after change, date)
    Column('active_bet_ids', String), #array of strings code of active bets
    Column('loans', String), #array of Tuple(balance, date created, date paid)
  )
  
  meta.create_all(engine)
  
