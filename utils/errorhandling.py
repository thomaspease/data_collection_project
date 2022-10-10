from selenium.common.exceptions import NoSuchElementException
from functools import wraps

def handle_nosuch_and_value_error(func):
  def wrapper(*args, **kwargs):
    try:
      result = func(*args, **kwargs)
      return result
    except ValueError as v:
      return print(v)
    except NoSuchElementException as v:
      return print(v)
  
  return wrapper