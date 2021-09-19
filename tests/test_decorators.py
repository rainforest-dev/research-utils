import logging
from research_utils.decorators.logging import Logging_Level, config_logger, logger
from research_utils.decorators.arguments import ignore_unknown_kwargs


def test_ignore_unknown_kwargs():
  @ignore_unknown_kwargs
  def positional_or_keywords(x, y):
    return x, y

  @ignore_unknown_kwargs
  def keyword_with_default(x, y, z=True):
    return x, y, z

  @ignore_unknown_kwargs
  def variable_length(x, y, *args, **kwargs):
    return x, y, args, kwargs

  @ignore_unknown_kwargs
  def keyword_only(x, *, y):
    return x, y

  assert (positional_or_keywords(x=3, y=5, z=10))
  assert (positional_or_keywords(3, y=5))
  assert (positional_or_keywords(3, 5))
  assert (positional_or_keywords(3, 5, z=10))
  assert (keyword_with_default(2, 2))
  assert (keyword_with_default(2, 2, z=False))
  assert (keyword_with_default(2, 2, False))
  assert (variable_length(2, 3, 5, 6, z=3))
  assert (keyword_only(1, y=3))


def test_logging_array():
  @config_logger(level=Logging_Level.DEBUG)
  @logger(level=Logging_Level.WARNING)
  def log_array():
    return 1, 2, 3, 4

  result = log_array()
  assert result == (1, 2, 3, 4)


def test_logging_dict():
  @config_logger(level=Logging_Level.INFO)
  @logger(transform=lambda x: f'{x[0]}\t{x[1]}')
  def log_dict():
    return {'one': 1, 'two': 2}

  result = log_dict()
  assert result == {'one': 1, 'two': 2}


class Logger():
  def __init__(self) -> None:
    self.__logger = logging.getLogger(__name__)

  @config_logger(level=Logging_Level.WARNING)
  @logger(lambda self, level, item: self.__logger.log(level=level, msg=item),
          level=Logging_Level.ERROR,
          transform=lambda x: f'{x[0]}\t{x[1]}')
  def test(self):
    return {'one': 1, 'two': 2}


def test_logging_with_class_logger():
  Logger().test()
