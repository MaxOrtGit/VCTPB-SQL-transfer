from multiprocessing import connection
from xmlrpc.client import Boolean
from savefiles import get_setting
#to do check for setting to init or quit
if not get_setting("init_sql_db"):
  print("savedata.db does not exist.\nquitting")
  quit()


from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
engine = create_engine('sqlite:///college.db', echo = True)
meta = MetaData()

students = Table(
  'students', meta, 
  Column('id', Integer, primary_key = True), 
  Column('name', String), 
  Column('lastname', String),
  Column('if', Boolean),
)
meta.create_all(engine)