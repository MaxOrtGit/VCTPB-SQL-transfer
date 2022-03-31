from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()
Engine = create_engine('sqlite:///savedata.db')
Session = sessionmaker(bind = Engine)()