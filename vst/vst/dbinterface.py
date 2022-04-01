from datetime import datetime
from sqlalchemy.orm import selectinload
from pytz import timezone
from savefiles import save_file, get_file, delete_file, get_prefix

from sqlaobjs import Session
from sqlalchemy import select, delete

from DBMatch import Match
from DBUser import User
from DBBet import Bet

def get_date():
  central = timezone('US/Central')
  return datetime.now(central)

def get_all_db(table_name, session=None):
  if session is None:
    with Session.begin() as session:
      if table_name == "match":
        return session.scalars(select(Match)).all()
      elif table_name == "bet":
        return session.scalars(select(Bet)).all()
      elif table_name == "user":
        return session.scalars(select(User)).all()
      else:
        return None
  else:
    if table_name == "match":
      return session.scalars(select(Match)).all()
    elif table_name == "bet":
      return session.scalars(select(Bet)).all()
    elif table_name == "user":
      return session.scalars(select(User)).all()
    else:
      return None


def get_from_db(table_name, code, session=None):
  if session is None:
    with Session.begin() as session:
      if table_name == "match":
        return session.get(Match, str(code))
      elif table_name == "bet":
        return session.get(Bet, str(code))
      elif table_name == "user":
        return session.get(User, int(code))
      else:
        return None
  else:
    if table_name == "match":
      return session.get(Match, str(code))
    elif table_name == "bet":
      return session.get(Bet, str(code))
    elif table_name == "user":
      return session.get(User, int(code))
    else:
      return None


#delete is session.delete(obj)