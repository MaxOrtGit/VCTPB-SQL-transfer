from dbinterface import get_from_list
import math
from sqlalchemy import Column, Integer, String, DateTime
import jsonpickle
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()



class Bet(Base):
  
  __tabelname__ = "bet"
  
  code = Column(String(8), primary_key = True)
  t1 = Column(String(50))
  t2 = Column(String(50))
  tournament_name = Column(String(100))
  winner = Column(Integer)
  amount_bet = Column(Integer)
  team_num = Column(Integer)
  color = Column(String(6))
  match_id = Column(String(8))
  user_id = Column(Integer)
  date_created = Column(DateTime)
  message_ids = Column(String)
  
  
  def __init__(self, code, t1, t2, tournament_name, amount_bet, team_num, color, match_id, user_id, date_created):
    
    self.code = code
    
    self.t1 = t1
    self.t2 = t2
    self.tournament_name = tournament_name
    
    self.winner = 0
    
    self.amount_bet = amount_bet
    self.team_num = team_num
    
    self.color = color
    
    self.match_id = match_id
    self.user_id = user_id
    self.date_created = date_created

    #team num of winner
    self.message_ids = []


  def get_message_ids(self):
    return jsonpickle.decode(self.message_ids)
  
  def save_message_ids(self, message_ids):
    self.message_ids = jsonpickle.encode(message_ids)
  

  def to_string(self):
    date_formatted = self.date_created.strftime("%d/%m/%Y at %H:%M:%S")
    return "Match ID: " + str(self.match_id) + ", User ID: " + str(self.user_id) + ", Amount Bet: " + str(self.bet_amount) + ", Team Bet On: " + str(self.team_num) + ", Date Created: " + str(date_formatted) + ", Date Closed: " + str(self.date_closed) + ", Winner: " + str(self.winner) + ", Identifyer: " + str(self.code) + ", Message IDs: " + str(self.message_ids)

  
  
  def get_team(self):
    if self.team_num == 1:
      return self.t1
    elif self.team_num == 2:
      return self.t2
    
  def get_match(self):
    return get_from_list("match", self.match_id)
    
  def get_team_and_payout(self):
    match = get_from_list("match", self.match_id)

    team = ""
    payout = 0.0
    print()
    if self.team_num == 1:
      team = match.t1
      payout = self.bet_amount * match.t1o - self.bet_amount
    elif self.team_num == 2:
      team = match.t2
      payout = self.bet_amount * match.t2o - self.bet_amount

    return(team, payout)

  def get_team_and_winner(self):

    team = ""
    winner = ""

    if self.team_num == 1:
      team = self.t1
    elif self.team_num == 2:
      team = self.t2

    if self.winner == 1:
      winner = self.t1
    elif self.winner == 2:
      winner = self.t2
    elif self.winner == 0:
      winner = "None"

    return(team, winner)

  async def short_to_string(self, bot):
    
    (team, payout) = self.get_team_and_payout()

    return f"User: <@!{self.user_id}>, Team: {team}, Amount: {self.bet_amount}, Payout: {int(math.floor(payout))}"

  async def basic_to_string(self, bot, match=None):
    if match is None:
      match = get_from_list("match", self.match_id)

    return f"Bet: {self.code}, User: <@!{self.user_id}>, Team: {self.get_team()}, Amount: {self.bet_amount}, Match ID: {match.code}"
  
  def balance_to_string(self, balance):
    
    match = get_from_list("match", self.match_id)
    (team, winner) = self.get_team_and_winner()

    return f"{match.t1} vs {match.t2}, Bet on: {team}, Winner: {winner}, Amount bet: {math.floor(self.bet_amount)}, Balance change: {math.floor(balance)}"

def is_valid_bet(code, t1, t2, tournament_name, amount_bet, team_num, color, match_id, user_id, date_created):
  errors = [False for _ in range(10)]
  if len(code) != 8 or isinstance(code, str) == False:
    errors[0] = True
  if len(t1) > 50 or isinstance(t1, str) == False:
    errors[1] = True
  if len(t2) > 50 or isinstance(t2, str) == False:
    errors[2] = True
  if len(tournament_name) > 100 or isinstance(tournament_name, str) == False:
    errors[3] = True
  if isinstance(amount_bet, int) == False or amount_bet < 1:
    errors[4] = True
  if isinstance(team_num, int) == False or team_num < 1 or team_num > 2:
    errors[5] = True
  if len(color) > 6 or isinstance(color, str) == False:
    errors[6] = True
  if len(match_id) != 8 or isinstance(match_id, str) == False:
    errors[7] = True
  if isinstance(user_id, int) == False:
    errors[8] = True
  if isinstance(date_created, str) == False:
    errors[9] = True

  return errors
  
        
    