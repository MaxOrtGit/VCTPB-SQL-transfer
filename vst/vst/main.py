from savefiles import get_setting
import os
import initdb

print("running")

if os.path.isfile("savedata.db"):
  print("savedata.db exists")
  #delete savedata.db
  os.remove("savedata.db")
  initdb.create_db()
else:
  if get_setting("init_sql_db"):
    initdb.create_db()
  else:
    print("savedata.db does not exist.\nquitting")
    quit()



#import sqlinterface