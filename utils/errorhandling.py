from selenium.common.exceptions import NoSuchElementException

def handle_nosuch_and_value_error(func):
  def wrapper(*args, **kwargs):
    try:
      func(*args, **kwargs)
    except ValueError:
      return None
    except NoSuchElementException:
      return None
  
  return wrapper