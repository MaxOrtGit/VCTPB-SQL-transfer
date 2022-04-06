from datetime import datetime
from pytz import timezone
import jsonpickle

from sqlaobjs import Session
from sqlalchemy import select

from DBMatch import Match
from DBUser import User
from DBBet import Bet
from Color import Color
from Channels import Channels

from configparser import ConfigParser

def get_date():
  central = timezone('US/Central')
  return datetime.now(central)

def get_date_string():
  return get_date().strftime("%Y-%m-%d-%H-%M-%S")



def get_all_db(table_name, session=None):
  if session is None:
    with Session.begin() as session:
      return session.scalars(select(eval(table_name))).all()
  return session.scalars(select(eval(table_name))).all()
  
  
def get_from_db(table_name, code, session=None):
  if session is None:
    with Session.begin() as session:
      return session.get(eval(table_name), code, populate_existing=True)
  return session.get(eval(table_name), code, populate_existing=True)
    
    
def get_condition_db(table_name, condition, session=None):
  if session is None:
    with Session.begin() as session:
      return get_condition_db(table_name, condition, session)
  return session.scalars(select(eval(table_name)).where(condition)).all()
    
    
def get_mult_from_db(table_name, codes, session=None):
  if session is None:
    with Session.begin() as session:
      return get_mult_from_db(table_name, codes, session)
  if table_name == "Color":
    return session.scalars(select(Color).where(Color.name.in_(codes))).all()
  else:
    obj = eval(table_name)
    return session.scalars(select(obj).where(obj.code.in_(codes))).all()


def delete_from_db(ambig, table_name=None, session=None):
  #wont update relationships
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
  #session.expire_all()
    
    
def add_to_db(obj, session=None):
  #will update relationships
  if session is None:
    with Session.begin() as session:
      return add_to_db(obj, session)
  session.add(obj)
  session.expire_all()


def is_key_in_db(table_name, key, session=None):
  if session is None:
    with Session.begin() as session:
      return is_key_in_db(table_name, key, session)
  return session.get(eval(table_name), key, populate_existing=True) is not None
      
      
def get_channel_from_db(channel_name, session=None):
  if session is None:
    with Session.begin() as session:
      return get_channel_from_db(channel_name, session)
    
  channels = session.scalars(select(Channels)).one()
  if channel_name == "bet":
    return channels.bet_channel_id
  elif channel_name == "match":
    return channels.match_channel_id
  else:
    return None
  
def set_channel_in_db(channel_name, channel_value, session=None):
  if session is None:
    with Session.begin() as session:
      return set_channel_in_db(channel_name, channel_value, session)
  channels = session.scalars(select(Channels)).one()
  if channel_name == "bet":
    channels.bet_channel_id = channel_value
  elif channel_name == "match":
    channels.match_channel_id = channel_value
                           
                          
def get_setting(setting_name):
  #setting_names: "discord_token", "github_token", "guild_ids", "override_savedata", "save_repo"
  configur = ConfigParser()
  configur.read('settings.ini')
  val = configur.get('settings', setting_name)
  if setting_name == "guild_ids" or setting_name == "override_savedata":
    return jsonpickle.decode(val)
  return configur.get("settings", setting_name)
