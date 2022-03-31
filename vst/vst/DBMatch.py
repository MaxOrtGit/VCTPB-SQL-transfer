
from decimal import Decimal
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Numeric, Integer, String, DateTime
import jsonpickle
from datetime import datetime
from sqltypes import JSONLIST
Base = declarative_base()

class Match(Base):
  
  __tabelname__ = "match"
  
  code = Column(String(8), primary_key = True)
  t1 = Column(String(50))
  t2 = Column(String(50))
  t1o = Column(Numeric(5, 3))
  t2o = Column(Numeric(5, 3))
  t1oo = Column(Numeric(5, 3))
  t2oo = Column(Numeric(5, 3))
  tournament_name = Column(String(100))
  odds_source = Column(String(50))
  winner = Column(Integer)
  color = Column(String(6))
  creator = Column(Integer)
  date_created = Column(DateTime(timezone = True))
  date_winner = Column(DateTime(timezone = True))
  date_closed = Column(DateTime(timezone = True))
  bet_ids = Column(JSONLIST) #array of int
  message_ids = Column(JSONLIST) #array of int
  
  def __init__(self, code, t1, t2, t1o, t2o, t1oo, t2oo, tournament_name, odds_source, color, creator, date_created):


    self.code = code
    self.t1 = t1
    self.t2 = t2
    self.t1o = t1o
    self.t2o = t2o
    self.t1oo = t1oo
    self.t2oo = t2oo

    self.tournament_name = tournament_name
    
    self.winner = 0
    
    self.odds_source = odds_source

    self.color = color
    
    #id of user that created match
    self.creator = creator

    self.date_created = date_created

    self.date_winner = None
    self.date_closed = None
    
    
    self.bet_ids = []
    self.message_ids = []
  
  def __init__(self, code, t1, t2, t1o, t2o, t1oo, t2oo, tournament_name, winner, odds_source, color, creator, date_created, date_winner, date_closed, bet_ids, message_ids):
    self.code = code
    self.t1 = t1
    self.t2 = t2
    self.t1o = t1o
    self.t2o = t2o
    self.t1oo = t1oo
    self.t2oo = t2oo
    self.tournament_name = tournament_name
    self.winner = winner
    self.odds_source = odds_source
    self.color = color
    self.creator = creator
    self.date_created = date_created
    self.date_winner = date_winner
    self.date_closed = date_closed
    self.bet_ids = bet_ids
    self.message_ids = message_ids
  
  
  
  def to_string(self):
    date_formatted = self.date_created.strftime("%d/%m/%Y at %H:%M:%S")
    return "Teams: " + str(self.t1) + " vs " + str(self.t2) + ", Odds: " + str(self.t1o) + " / " + str(self.t2o) +  ", Old Odds: " + str(self.t1oo) + " / " + str(self.t2oo) + ", Tournament Name: " + str(self.tournament_name) + ", Odds Source: " + str(self.odds_source) + ", Created On: " + str(date_formatted) + ", Bet IDs: " + str(self.bet_ids) + ", Date Closed: " + str(self.date_closed) + ", Winner: " + str(self.winner) + ", Identifyer: " + str(self.code) + ", Message IDs: " + str(self.message_ids)


  def short_to_string(self):
    return "Teams: " + str(self.t1) + " vs " + str(self.t2) + ", Odds: " + str(self.t1o) + " / " + str(self.t2o)

  def winner_name(self):
    if self.winner == 0:
      return "None"
    elif self.winner == 1:
      return self.t1
    else:
      return self.t2

  def basic_to_string(self):
    return f"Match: {self.code}, Teams: {self.t1} vs {self.t2}, Odds: {self.t1o} vs {self.t2o}, Tournament Name: {self.tournament_name}"
  
  
  
def is_valid_match(code, t1, t2, t1o, t2o, t1oo, t2oo, tournament_name, winner, odds_source, color, creator, date_created, date_winner, date_closed, bet_ids, message_ids):
  errors = [False for _ in range(17)]
  if isinstance(code, str) == False or len(code) != 8:
    errors[0] = True
  if isinstance(t1, str) == False or len(t1) > 50:
    errors[1] = True
  if isinstance(t2, str) == False or len(t2) > 50:
    errors[2] = True
  if isinstance(tournament_name, str) == False or len(tournament_name) > 100:
    errors[3] = True
  if isinstance(t1o, Decimal) == False or t1o < 0:
    errors[4] = True
  if isinstance(t2o, Decimal) == False or t2o < 0:
    errors[5] = True
  if isinstance(t1oo, Decimal) == False or t1oo < 0:
    errors[6] = True
  if isinstance(t2oo, Decimal) == False or t2oo < 0:
    errors[7] = True
  if isinstance(winner, int) == False or winner < 0 or winner > 2:
    errors[8] = True
  if isinstance(odds_source, String) == False or len(odds_source) > 50:
    errors[9] = True
  if isinstance(color, str) == False or len(color) > 6:
    errors[10] = True
  if isinstance(creator, int) == False:
    errors[11] = True
  if isinstance(date_created, datetime) == False:
    errors[12] = True
  if isinstance(date_winner, datetime) == False:
    errors[13] = True
  if isinstance(date_closed, datetime) == False:
    errors[14] = True
  if isinstance(bet_ids, list) == False:
    errors[15] = True
  if isinstance(message_ids, list) == False:
    errors[16] = True

  return errors

