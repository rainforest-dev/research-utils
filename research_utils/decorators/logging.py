import sys
from typing import Any, Callable
import functools
from enum import Enum
import logging

grey = "\x1b[38;21m"
green = "\x1b[1;32m"
yellow = "\x1b[33;21m"
red = "\x1b[31;21m"
bold_red = "\x1b[31;1m"
reset = "\x1b[0m"

class Logging_Level(Enum):
  DEBUG = logging.DEBUG
  INFO = logging.INFO
  WARNING = logging.WARNING
  ERROR = logging.ERROR
  CRITICAL = logging.CRITICAL

class CustomFormatter(logging.Formatter):
  format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

  def __init__(self, fmt: str = format, datefmt: str = None, style = '%') -> None:
      super().__init__(fmt=fmt, datefmt=datefmt, style=style)
      self.FORMATS = {
          logging.DEBUG: grey + fmt + reset,
          logging.INFO: green + fmt + reset,
          logging.WARNING: yellow + fmt + reset,
          logging.ERROR: red + fmt + reset,
          logging.CRITICAL: bold_red + fmt + reset
      }

  def format(self, record: logging.LogRecord):
      log_fmt = self.FORMATS.get(record.levelno)
      formatter = logging.Formatter(log_fmt)
      return formatter.format(record)

def log(*args, level: int, item, **kwargs):
  level = Logging_Level(level)
  if level == Logging_Level.DEBUG:
    logging.debug(item)
  elif level == Logging_Level.INFO:
    print(item)
    logging.info(item)
  elif level == Logging_Level.WARNING:
    logging.warning(item)
  elif level == Logging_Level.ERROR:
    logging.error(item)
  elif level == Logging_Level.CRITICAL:
    logging.critical(item)
  else:
    pass

def config_logger(level: Logging_Level=Logging_Level.WARNING, format='[%(asctime)s %(levelname)-8s] %(message)s', datefmt='%Y%m%d %H:%M:%S'):
  def decorator(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
      logger = logging.getLogger()
      logger.setLevel(level.value)
      if len(logger.handlers) == 0:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level.value)
        handler.setFormatter(CustomFormatter())
        logger.addHandler(handler)
      return func(*args, **kwargs)
    return inner
  return decorator

def logger(log_func: Callable[[int, Any], None]=None, level: Logging_Level=Logging_Level.DEBUG, transform: Callable=None):
  log_func = log if log_func is None else log_func
  def decorator(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
      items = func(*args, **kwargs)
      try:
        for item in items.items() if isinstance(items, dict) else items:
          log_func(*args, level=level.value, item=item if transform is None else transform(item), **kwargs)
      except:
        log_func(*args, level=level.value, item=items if transform is None else transform(items), **kwargs)
      return items
    return inner
  return decorator
