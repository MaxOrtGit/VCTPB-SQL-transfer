import jsonpickle 
import math
from datetime import datetime
from pytz import timezone
from savefiles import save_file, get_file, delete_file, get_prefix

from sqlaobjs import Session

def get_date():
  central = timezone('US/Central')
  return datetime.now(central)

def get_all_db(table_name):
  return Session.query(eval(table_name)).all()


def get_from_db(table_name, id):
  return Session.query(eval(table_name)).filter_by(id=id).first()