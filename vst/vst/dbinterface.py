from datetime import datetime
from pytz import timezone

from sqlaobjs import Session
from sqlalchemy import select, func

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
      return session.scalars(select(eval(table_name))).all()
  else:
    return session.scalars(select(eval(table_name))).all()


def get_from_db(table_name, code, session=None):
  if session is None:
    with Session.begin() as session:
      return session.get(eval(table_name), code, populate_existing=True)
  else:
    return session.get(eval(table_name), code, populate_existing=True)
    
    
def get_mult_from_db(table_name, codes, session=None):
  if session is None:
    with Session.begin() as session:
      return session.execute(select(eval(table_name)).where(Match.code.in_(codes))).scalars().all()
  else:
    return session.execute(select(eval(table_name)).where(Match.code.in_(codes))).scalars().all()


def delete_from_db(ambig, table_name=None, session=None):
  if isinstance(ambig, str) or isinstance(ambig, int):
    code = ambig
    if session is None:
      with Session.begin() as session:
        session.delete(session.get(eval(table_name), code))
    else:
      session.delete(session.get(eval(table_name), code))
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

def is_key_in_db(table_name, key, session=None):
  if session is None:
    with Session.begin() as session:
      is_key_in_db(table_name, key, session)
  else:
    if table_name == "color":
      return session.execute(select(func.count(eval(table_name))).where(eval(table_name).name == key)) > 0
    else:
      return session.execute(select(func.count(eval(table_name))).where(eval(table_name).code == key)) > 0
      