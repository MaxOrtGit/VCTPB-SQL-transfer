from sqlalchemy.types import TypeDecorator, VARCHAR, String
import jsonpickle
from decimal import Decimal

class JSONLIST(TypeDecorator):
  
  impl = VARCHAR

  def process_bind_param(self, value, dialect):
    if value is not None:
      value = jsonpickle.encode(value)
    return value

  def process_result_value(self, value, dialect):
    if value is not None:
      value = jsonpickle.decode(value)
    return value
  
  
class DECIMAL(TypeDecorator):
      
  impl = String
  
  def load_dialect_impl(self, dialect):
    return dialect.type_descriptor(VARCHAR(6))
  
  def process_bind_param(self, value, dialect):
    if value is not None:
      value = str(value)
      if len(value) > 6:
        f, s = value.split('.')
        if len(f) > 2:
          f = "99"
        if len(s) > 3:
          s = s[:3] 
        value = Decimal(f + '.' + s)
      
    return str(value)
  
  def process_result_value(self, value, dialect):
    if value is not None:
      value
    return Decimal(value)
  