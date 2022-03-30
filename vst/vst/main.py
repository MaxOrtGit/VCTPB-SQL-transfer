from savefiles import get_setting
import os
from initdb import *

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



#import sqlinterface