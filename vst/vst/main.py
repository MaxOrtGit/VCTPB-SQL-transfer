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



from dbinterface import get_from_db, get_all_db, get_mult_from_db, delete_from_db, add_to_db





def test_get():
  print("\n\n")
  matches = get_all_db("match")

  match_codes = [match.code for match in matches]
  print(match_codes)

  match = get_from_db("match", match_codes[1])
  print(match)


  print("\n\n")
  #test get_mult

  matches = get_mult_from_db("match", match_codes[2:8])
  print(matches)
  match_codes = [match.code for match in matches]

  print(match_codes)


def test_delete():
  print("\n\n")

  with Session.begin() as session:
    matches = get_all_db("match", session=session)

    match_codes = [match.code for match in matches]
    code = match_codes[0]
    
    match = get_from_db("match", code, session)
    print(match.code)
    bets_codes = [bet.code for bet in match.bets]
    print(bets_codes)
    delete_from_db(match, session=session)
    

    match = get_from_db("match", code, session)
    print(match)
    
    bets = get_mult_from_db("bet", bets_codes, session)
    print(bets)
    
  


def test_relat_ctp():
  print("\n\n")
  #test relationship child to parent

  #need to use with for getting parents
  with Session.begin() as session:
    bets = get_all_db("bet", session=session)
    bet = bets[-1]
    match = bet.match
    print(match)
    user = match.creator
    print(user)

def test_relat_ptc():
  print("\n\n")
  #test relationship parent to child

  with Session.begin() as session:
    users = get_all_db("user", session=session)
    user = users[0]
    print(user)
    match = user.matches[0]
    print(match)
    bet = match.bets[0]
    print(bet)


test_get()
test_delete()
test_relat_ctp()
test_relat_ptc()