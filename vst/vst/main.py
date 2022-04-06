import os
from initdb import *
import sqlalchemy
print(sqlalchemy.__version__)

print("running")

if os.path.isfile("savedata.db"):
  print("savedata.db exists, overwriting")
  #delete savedata.db
  os.remove("savedata.db")
  create_db()
  files_to_db()
else:
  create_db()
  files_to_db()


if False:
  quit()

from dbinterface import get_from_db, get_all_db, get_mult_from_db, delete_from_db, add_to_db, is_key_in_db, get_channel_from_db, set_channel_in_db, get_setting, get_condition_db, get_date_string




def test_get():
  print("\ntest_get")
  matches = get_all_db("Match")

  match_codes = [match.code for match in matches]
  print(match_codes)

  match = get_from_db("Match", match_codes[1])
  print(match)
  


def test_get_mult():
  print("\ntest_get_mult")
  
  matches = get_all_db("Match")
  bets = get_all_db("Bet")
  users = get_all_db("User")
  
  print(matches)
  print(bets)
  print(users)

  match_codes = [match.code for match in matches]

  matches = get_mult_from_db("Match", match_codes[2:8])
  match_codes = [match.code for match in matches]

  print(is_key_in_db("Match", match_codes[0]))
  print(is_key_in_db("Match", "1234567l"))


def test_is_key_in_db():
  print("\ntest_is_key_in_db")
  matches = get_all_db("Match")
  match = matches[0]
  
  bets = get_all_db("Bet")
  bet = bets[0]
  
  users = get_all_db("User")
  user = users[0]
  
  
  print(is_key_in_db("Match", match.code))
  print(is_key_in_db("Match", match.code[:-1] + "l"))
  print(is_key_in_db("Bet", bet.code))
  print(is_key_in_db("Bet", bet.code[:-1] + "l"))
  print(is_key_in_db("User", user.code))
  print(is_key_in_db("User", user.code[:-1] + "l"))
  

def test_delete_match():
  print("\ntest_delete_match")

  with Session.begin() as session:
    matches = get_all_db("Match", session)

    match_codes = [match.code for match in matches]
    code = match_codes[0]
    
    match = get_from_db("Match", code, session)
    print(match.code)
    bets_codes = [bet.code for bet in match.bets]
    print(bets_codes)
    delete_from_db(match, session=session)
    

    match = get_from_db("Match", code, session)
    print(match)
    
    bets = get_mult_from_db("Bet", bets_codes, session)
    print(bets)
    
    
def test_delete_bet():
  print("\ntest_delete_bet")
  
  with Session.begin() as session:
    bets = get_all_db("Bet", session)
    
    bet_codes = [bet.code for bet in bets]
    
    code = bet_codes[0]
    
    bet = get_from_db("Bet", code, session)
    
    match = bet.match
    m_code = match.code
    
    delete_from_db(bet, session=session)
    
    bet = get_from_db("Bet", code, session)
    
    match = get_from_db("Match", m_code, session)
    
    print(bet)
    print(match)
  

def test_delete_user():
  print("\ntest_delete_user")
  with Session.begin() as session:
    users = get_all_db("User", session)
    user = users[-1]
    ucode = user.code
    for x in range(10):
      try:
        match = user.matches[0]
        print(match.creator.username)
        mcode = match.code
        bet = match.bets[x]
        bcode = bet.code
        print(bet.user.username)
      except:
        print("no bets")
      else:
        print("bet")
        break
    
    delete_from_db(user, session=session)
    print(ucode)
    user = get_from_db("User", ucode, session)
    
    match = get_from_db("Match", mcode, session)
    bet = get_from_db("Bet", bcode, session)
    print(user)
    print(match)
    print(bet)
    
  

def test_relat_ctp():
  print("\ntest_relat_ctp")
  #test relationship child to parent

  #need to use with for getting parents
  with Session.begin() as session:
    bets = get_all_db("Bet", session)
    bet = bets[-1]
    match = bet.match
    print(match)
    user = match.creator
    print(user)


def test_relat_ptc():
  print("\ntest_relat_ptc")
  #test relationship parent to child

  with Session.begin() as session:
    users = get_all_db("User", session)
    user = users[0]
    print(user, user.username)
    matches = user.matches
    print(matches)
    nmatch = get_from_db("Match", matches[0].code, session)
    nbets = nmatch.bets
    print(nbets)
    bets = matches[0].bets
    print(bets)


def test_relat_get_match():
  print("\ntest_relat_get_match")
  #test relationship parent to child
  
  with Session.begin() as session:
    matches = get_all_db("Match", session)
    code = matches[-1].code
    
    match = get_from_db("Match", code, session)
    user = match.creator
    print(user)
    bets = match.bets
    print(bets)
  

def test_get_then_set():
  print("\ntest_get_then_set")
  
  with Session.begin() as session:
    matches = get_all_db("Match", session)
    
    
    for match in matches[::-1]:
      print("get")
      try:
        bets = match.bets
        print(match.code, bets)
        bet = bets[0]
        print(bet.color_hex)
        mcode = match.code
      except:
        print("no bets")
      else:
        print("found bet")
        break
    else:
      print("no bets found")
    
    print(bet.color_hex)
    bet.color_hex = "123456"
    print(bet.color_hex)
    
    matchd = get_from_db("Match", mcode, session)
    
    betd = matchd.bets[0]
    
    print(betd.color_hex)
    
    






def test_get_color():
  print("\ntest_get_color")
  
  colors = get_all_db("Color")
  print(colors)
  
  color_name = colors[0].name
  
  color = get_from_db("Color", color_name)
  print(color)
    
  
def test_get_mult_color():
  print("\ntest_get_mult_color")
  
  colors = get_all_db("Color")

  color_names = [color.name for color in colors]

  colorss = get_mult_from_db("Color", color_names[2:8])
  print(colorss)
  color_names = [color.name for color in colorss]

  print(color_names)
  print(is_key_in_db("Color", color_names[0]))
  print(is_key_in_db("Color", "1234567l"))


def test_is_key_in_db_color():
  print("\ntest_is_key_in_db_color")
  
  colors = get_all_db("Color")
  color = colors[0]
  
  print(is_key_in_db("Color", color.name))
  print(is_key_in_db("Color", color.name[:-1] + "l"))


def test_add_color():
  print("\ntest_add_color")
  
  color = Color("Orange", "FFA500")
  add_to_db(color)
  
  color = get_from_db("Color", "Orange")
  print(color)
  
  
def test_add_color_to_match(session = None):
  if session is None:
    with Session.begin() as session:
      print("\ntest_add_color_to_match")
      return test_add_color_to_match(session)
  else:
    matches = get_all_db("Match", session)
    match = matches[0]
    print(match, match.color, match.color_hex)
    color = get_from_db("Color", "Orange", session)
    
    add_to_db(color, session)
    match.set_color(color)
    
    match = get_from_db("Match", match.code, session)
    print(match.color)
    print(match.color_hex)
    

def test_delete_color():
  print("\ntest_delete_color")
  
  with Session.begin() as session:
    matches = get_all_db("Match", session)
    match = matches[0]
    
    if match.color is None:
      print("-----adding color------")
      test_add_color_to_match(session)
      print("-----adding color------")
    print(match, match.color, match.color_hex)
    
    
    color = get_from_db("Color", "Orange", session)
    print(color.name)
    match_codes = [match.code for match in color.matches]
    print(match_codes)
    delete_from_db(color, session=session)
    

    color = get_from_db("Color", "Orange", session)
    print(color)
    
    matchess = get_mult_from_db("Match", match_codes, session)
    print(matchess)
    match_colors = [match.color for match in matchess]
    print(match_colors)
    match_code = matchess[0].code
    
    match = get_from_db("Match", match_code, session)
    print(match.color)
    print(match.color_hex)
    
    
    
def test_get_channel_id():
  print("\ntest_get_channel_id")
  print(get_channel_from_db("bet"))
  print(get_channel_from_db("match"))


def test_set_channel_id():
  print("\ntest_set_setting")
  
  print(get_channel_from_db("bet"))
  set_channel_in_db("bet", 123456789)
  print(get_channel_from_db("bet"))
  

def test_get_setting():
  print("\ntest_get_setting")
  #setting_names: "discord_token", "github_token", "guild_ids", "override_savedata", "save_repo"
  settings = ["discord_token", "github_token", "guild_ids", "override_savedata", "save_repo"]
  for setting in settings:
    print(f"{setting}: {get_setting(setting)}, {type(get_setting(setting))}")
  
def ambig_to_obj(ambig, prefix, session=None):
  if isinstance(ambig, int) or isinstance(ambig, str):
    obj = get_from_db(prefix, ambig, session)
  elif isinstance(ambig, User) or isinstance(ambig, Match) or isinstance(ambig, Bet):
    obj = ambig
  else:
    obj = None
    print(ambig, type(ambig))
  return obj
  
def add_balance_user(user_ambig, change, description, date, session=None):
  if session is None:
    with Session.begin() as session:
      return add_balance_user(user_ambig, change, description, date, session=session)
      
  user = ambig_to_obj(user_ambig, "User")
  if user is None:
    return None
  user.balances.append((description, Decimal(str(round(user.balances[-1][1] + Decimal(str(change)), 5))), date))
  user.balances.sort(key=lambda x: x[2])
  #user.balances = user.balances + []
  user.color_hex = "eeedee"
  return user

def test_add_balance_to_user():
  print("\ntest_add_balance_to_user")
  
  with Session.begin() as session:
    user = get_all_db("User", session)[0]
    bet_id = "award_" + user.get_unique_code("award_") + "_" + "testttt"
    print(bet_id)
    print(str(user.balances)[-200:], user.get_balance(), user.color_hex)
    abu = add_balance_user(user, 10, bet_id, get_date(), session)
    print(str(abu.balances)[-200:], user.get_balance(), user.color_hex)
    
    userer = get_all_db("User", session)[0]
    print(str(userer.balances)[-200:], userer.get_balance(), userer.color_hex)

def test_get_condition():
  print("\ntest_get_condition")
  num = "7"
  print(get_condition_db("Bet", Bet.code.startswith(num)))


def test_user_active_bets():
  print("\ntest_user_active_bets")
  
  with Session.begin() as session:
    user = get_all_db("User", session)[0]
    #print(user.active_bets)
    user.bets[-1].winner = 0
    user.bets[-2].winner = 0
    user.bets[-3].winner = 0
    bet = user.bets[-4]

    bet.winner = 0

    print(user.active_bets)
    bet.winner = 1

    print(bet.winner)
    session.flush([bet])
    session.refresh(user)
    #session.flush([user.bets[-4]])
    #session.expire(user)
    print(user.active_bets, "diff")
    
  with Session.begin() as session:
    user = get_all_db("User", session)[0]
    print(user.active_bets)
    

test_user_active_bets()
quit()

test_get()
test_get_mult()
test_is_key_in_db()
#test_delete_match()
#test_delete_bet()
#test_delete_user()
test_relat_ctp()
test_relat_ptc()
test_relat_get_match()
test_get_then_set()


test_get_color()
test_get_mult_color()
test_is_key_in_db_color()
test_add_color()
test_add_color_to_match()
test_delete_color()


test_get_channel_id()
test_set_channel_id()
test_get_setting()

test_add_balance_to_user()

test_get_condition()
test_user_active_bets()