from abc import abstractmethod
from functools import reduce


class SQLArgument:
  def __init__(self):
    pass

  @property
  @abstractmethod
  def sql(self):
    return NotImplemented


class OperatorSQLArgument(SQLArgument):
  def __init__(self, field, operator=None, bound=None):
    super().__init__()
    self.__field = field
    self.__operator = operator
    self.__bound = bound

  @property
  def sql(self):
    if self.__operator is None and self.__bound is not None:
      return
    else:
      return f'{self.__field} {self.__operator} {self.__bound}'


class ConditionSQLArgument(SQLArgument):
  def __init__(self, *args, keyword=None):
    super().__init__()
    self.__keyword = keyword
    self.__args = args

  @property
  def sql(self):
    if self.__keyword is None:
      return
    else:
      return reduce(lambda arg1, arg2: f'{arg1.sql} {self.__keyword} {arg2.sql}', self.__args)


class AND(ConditionSQLArgument):
  def __init__(self, *args):
    super().__init__(*args, keyword='AND')


class Lower(OperatorSQLArgument):
  def __init__(self, field, bound):
    super().__init__(field, operator='<=', bound=bound)


class Upper(OperatorSQLArgument):
  def __init__(self, field, bound):
    super().__init__(field, operator='>=', bound=bound)


class SQLArgumentFactory:
  @classmethod
  def between(self, field, lower_bound, upper_bound):
    return AND(Lower(field, upper_bound), Upper(field, lower_bound))
