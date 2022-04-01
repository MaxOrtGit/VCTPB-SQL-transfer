from datetime import datetime
import re
from pytz import timezone
from savefiles import save_file, get_file, delete_file, get_prefix

from sqlaobjs import session

from DBMatch import Match
from DBUser import User
from DBBet import Bet

def get_date():
  central = timezone('US/Central')
  return datetime.now(central)

def get_all_db(table_name):
  if table_name == "match":
    return session.get(Match, id)
  elif table_name == "user":
    return session.get(User, id)
  elif table_name == "bet":
    return session.get(Bet, id)
  else:
    return None
  return session.query(eval(table_name)).all()

def get_from_db(table_name, id):
  if table_name == "match":
    return session.get(Match, id)
  elif table_name == "user":
    return session.get(User, id)
  elif table_name == "bet":
    return session.get(Bet, id)
  else:
    return None

#session.query(Match).filter(Match.code == "test")
