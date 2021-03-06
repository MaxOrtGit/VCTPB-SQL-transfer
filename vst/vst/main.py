import os
from initdb import *
from sqlalchemy import and_

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

from dbinterface import get_from_db, get_all_db, get_mult_from_db, delete_from_db, add_to_db, is_key_in_db, get_channel_from_db, set_channel_in_db, get_setting, get_condition_db, get_date_string, get_new_db, is_condition_in_db
from time import time



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
    print(color.matches)
    
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
    bet_id = "award_" + user.get_unique_code() + "_" + "testttt"
    print(bet_id)
    print(str(user.balances)[-200:], user.get_balance(), user.color_hex)
    abu = add_balance_user(user, 10, bet_id, get_date(), session)
    print(str(abu.balances)[-200:], user.get_balance(), user.color_hex)
    
    userer = get_all_db("User", session)[0]
    print(str(userer.balances)[-200:], userer.get_balance(), userer.color_hex)

def test_get_condition():
  print("\ntest_get_condition")
  hex = "a"
  print(get_condition_db("Bet", Bet.code.startswith(hex)))


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
    session.expire(user)
    print(user.active_bets, "diff")
    
def test_user_open_matches():
  print("\ntest_user_open_matches")
  
  with Session.begin() as session:
    user = get_all_db("User", session)[0]
    print(user.username)
    a_matches = user.active_bets
    print(a_matches)
    matches = get_all_db("Match", session)
    print(matches[-1].bets, matches[-2].bets, matches[-3].bets)
    print(matches[-1].bets[0].user.username, matches[-2].bets[0].user.username, matches[-3].bets[0].user.username)
    
    
    del_num = 0
    match1 = matches[-1]
    match1.winner = 0
    match1.date_closed = None
    for bet1 in match1.bets:
      del_num += 1
      bet1.winner = 0
    match1_bet_user_ids = [bet.user_id for bet in match1.bets]
    print(match1_bet_user_ids, user.code, user.code in match1_bet_user_ids)
    print(type(match1_bet_user_ids), type(user.code), type(user.code in match1_bet_user_ids))
    print(match1.code, match1.winner, match1.bets, user.code in match1_bet_user_ids)
    
    match2 = matches[-2]
    match2.winner = 0
    match2.date_closed = None
    for bet2 in match2.bets:
      del_num += 1
      #print("deleted", bet2.code)
      delete_from_db(bet2, session=session)
    session.flush()
    session.expire_all()
    match2_bet_user_ids = [bet.user_id for bet in match2.bets]
    print(match2.code, match2.winner, match2.bets, user.code in match2_bet_user_ids)
    
      
    match3 = matches[-3]
    match3.winner = 0
    old_date = match3.date_closed
    match3.date_closed = None
    for bet3 in match3.bets:
      del_num += 1
      #print("deleted", bet3.code)
      delete_from_db(bet3, session=session)
    session.flush()
    session.expire_all()
    match3_bet_user_ids = [bet.user_id for bet in match3.bets]
    print(match3.code, match3.winner, match3.bets, user.code in match3_bet_user_ids)
    
    print(f"init done", del_num)
    bets = user.bets
    match_ids = [bet.match_id for bet in bets]
    
    for open_match in user.open_matches(session):
      print(open_match, open_match.code in match_ids)
      
    print(user.open_matches(session))
    match3.winner = 1
    match3.date_closed = old_date
    
    print(match3.winner)
    
    session.flush([match1, match2, match3])
    session.expire(user)
    print(user.open_matches(session), "diff")
    
def test_get_new_db():
  print("\ntest_get_new_db")
  
  with Session.begin() as session:
    match = get_new_db("Match", session)
    print(match.date_created)
    
    matches = get_all_db("Match", session)
    newest_date = matches[0].date_created
    for match in matches:
      if match.date_created > newest_date:
        newest_date = match.date_created
    print(newest_date)

def test_is_condition_in_db():
  print("\ntest_is_condition_in_db")
  
  with Session.begin() as session:
    match = get_all_db("Match", session)[3]
    print(is_condition_in_db("Match", (Match.t1 == match.t1) & (Match.t2 == match.t2), session))
    print(is_condition_in_db("Match", (Match.t1 == match.t1) & (Match.t2 == match.t2 + "h"), session))

def test_get_speed():
  print("\ntest_get_speed")
  
  startTime = time()
  with Session.begin() as session:
    matches = get_all_db("Match", session)
    match_codes = [match.code for match in matches[:20]]
  endTime = time()
  
  print(endTime - startTime)
  
  startTime = time()
  with Session.begin() as session:
    matches = []
    for match_code in match_codes:
      matches.append(get_from_db("Match", match_code, session))
  endTime = time()
  
  print(endTime - startTime)
  
  startTime = time()
  with Session.begin() as session:
    matches = get_mult_from_db("Match", match_codes, session)
  endTime = time()
  
  print(endTime - startTime)
  
  
def test_parent_speeds():
  print("\ntest_parent_speeds")
  
  with Session.begin() as session:
    bets = get_all_db("Bet", session)[:20]

    startTime = time()
    
    matches = []
    for bet in bets:
      matches.append(bet.match)
      
    endTime = time()
    
    print(endTime - startTime)
    session.expire_all()
    
  with Session.begin() as session:
    bets = get_all_db("Bet", session)[:20]
    
    startTime = time()
    match_ids = [bet.match_id for bet in bets]
    matches = get_mult_from_db("Match", match_ids, session)
    
    endTime = time()
    
    print(endTime - startTime)
  

test_user_open_matches()
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
test_user_open_matches()

test_get_new_db()
test_is_condition_in_db()

test_get_speed()
test_parent_speeds()