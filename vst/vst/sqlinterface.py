from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from User import User
from Match import Match
from Bet import Bet

engine = create_engine('sqlite:///savedata.db')
session = sessionmaker(bind=engine)()


Base = declarative_base()
