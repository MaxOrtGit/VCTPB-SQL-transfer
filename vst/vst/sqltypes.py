from sqlalchemy.types import TypeDecorator, VARCHAR
import jsonpickle

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