
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Numeric, Integer, String, DateTime
import jsonpickle

Base = declarative_base()

match = Table(
  'match', meta, 
  Column('code', String(8), primary_key = True),
  Column('t1', String(50)),
  Column('t2', String(50)),
  Column('t1o', Numeric(5, 3)),
  Column('t2o', Numeric(5, 3)),
  Column('t1oo', Numeric(5, 3)),
  Column('t2oo', Numeric(5, 3)),
  Column('tournament_name', String(100)),
  Column('odds_source', String(50)),
  Column('winner', Integer),
  Column('color', String(6)),
  Column('creator', Integer),
  Column('date_created', DateTime(timezone = True)),
  Column('date_winner', DateTime(timezone = True)),
  Column('date_closed', DateTime(timezone = True)),
  Column('bet_ids', String), #array of int 
  Column('message_ids', String), #array of int
)

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
  bet_ids = Column(String) #array of int
  message_ids = Column(String) #array of int
  
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
    
    
    self.bet_ids = jsonpickle.encode([])
    self.message_ids = jsonpickle.encode([])
  
  
  
  def get_bet_ids(self):
    return jsonpickle.decode(self.bet_ids)

  def get_message_ids(self):
    return jsonpickle.decode(self.message_ids)
  
  def set_bet_ids(self, bet_ids):
    self.bet_ids = jsonpickle.encode(bet_ids)

  def set_message_ids(self, message_ids):
    self.message_ids = jsonpickle.encode(message_ids)
  
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