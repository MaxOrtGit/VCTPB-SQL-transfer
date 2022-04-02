from datetime import datetime
from pytz import timezone

from sqlaobjs import Session
from sqlalchemy import select

from DBMatch import Match
from DBUser import User
from DBBet import Bet
from Color import Color

def get_date():
  central = timezone('US/Central')
  return datetime.now(central)

def get_all_db(table_name, session=None):
  if session is None:
    with Session.begin() as session:
      return get_all_db(table_name, session)
  else:
    if table_name == "match":
      return session.scalars(select(Match)).all()
    elif table_name == "bet":
      return session.scalars(select(Bet)).all()
    elif table_name == "user":
      return session.scalars(select(User)).all()
    elif table_name == "color":
      return session.scalars(select(Color)).all()
    else:
      return None


def get_from_db(table_name, code, session=None):
  if session is None:
    with Session.begin() as session:
      return get_from_db(table_name, code, session)
  else:
    if table_name == "match":
      return session.get(Match, str(code), populate_existing=True)
    elif table_name == "bet":
      return session.get(Bet, str(code), populate_existing=True)
    elif table_name == "user":
      return session.get(User, int(code), populate_existing=True)
    else:
      return None
    
    
def get_mult_from_db(table_name, codes, session=None):
  if session is None:
    with Session.begin() as session:
      if table_name == "match":
        return session.execute(select(Match).where(Match.code.in_(codes))).scalars().all()
      elif table_name == "bet":
        return session.execute(select(Bet).where(Bet.code.in_(codes))).scalars().all()
      elif table_name == "user":
        return session.execute(select(User).where(User.code.in_(codes))).scalars().all()
      else:
        return None
  else:
    if table_name == "match":
      return session.execute(select(Match).where(Match.code.in_(codes))).scalars().all()
    elif table_name == "bet":
      return session.execute(select(Bet).where(Bet.code.in_(codes))).scalars().all()
    elif table_name == "user":
      return session.execute(select(User).where(User.code.in_(codes))).scalars().all()
    else:
      return None


def delete_from_db(ambig, table_name=None, session=None):
  if isinstance(ambig, str) or isinstance(ambig, int):
    code = ambig
    if session is None:
      with Session.begin() as session:
        if table_name == "match":
          session.delete(session.get(Match, str(code)))
        elif table_name == "bet":
          session.delete(session.get(Bet, str(code)))
        elif table_name == "user":
          session.delete(session.get(User, int(code)))
    else:
      if table_name == "match":
        session.delete(session.get(Match, str(code)))
      elif table_name == "bet":
        session.delete(session.get(Bet, str(code)))
      elif table_name == "user":
        session.delete(session.get(User, int(code)))
  else:
    if session is None:
      with Session.begin() as session:
        session.delete(ambig)
    else:
      session.delete(ambig)
    
    
def add_to_db(obj, session=None):
  if session is None:
    with Session.begin() as session:
      session.add(obj)
  else:
    session.add(obj)