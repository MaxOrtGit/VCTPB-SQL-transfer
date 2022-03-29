from savefiles import get_setting
import os

print("running")

if os.path.isfile("savedata.db"):
  print("savedata.db exists")
else:
  if get_setting("init_sql_db"):
    import initdb
  else:
    print("savedata.db does not exist.\nquitting")
    quit()



#import sqlinterface