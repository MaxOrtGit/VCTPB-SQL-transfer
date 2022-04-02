from olddbinterface import get_from_list
import math
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqltypes import JSONLIST
from datetime import datetime

from sqlaobjs import mapper_registry

@mapper_registry.mapped
class Color():
  
  __tablename__ = "colors"
  
  name = Column(String(32), primary_key=True, nullable=False)
  hex = Column(String(6), nullable=False)
  
  
  
  def __init__(self, name, hex):
    self.name = name
    self.hex = hex