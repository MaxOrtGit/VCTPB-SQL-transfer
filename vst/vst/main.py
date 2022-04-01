from savefiles import get_setting
import os
from initdb import *
import sqlalchemy
print(sqlalchemy.__version__)

print("running")

if os.path.isfile("savedata.db"):
  print("savedata.db exists")
  #delete savedata.db
  os.remove("savedata.db")
  create_db()
  files_to_db()
else:
  if get_setting("init_sql_db"):
    create_db()
    files_to_db()
  else:
    print("savedata.db does not exist.\nquitting")
    quit()



from dbinterface import get_all_db, get_from_db

matches = get_all_db("match")
print(matches)
code = matches[10].code

match = get_from_db("match", code)

print(match.t1)

with Session.begin() as session:
  umatch = get_from_db("match", code, session)
  umatch.t1 = "test"

print(match.t1)

match = get_from_db("match", code)

print(match.t1)