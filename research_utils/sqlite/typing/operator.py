from .sql import SQLArgument
from functools import reduce


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
      return f'{self.__field} {self.__operator} "{self.__bound}"'


class ConditionSQLArgument(SQLArgument):
  def __init__(self, *args, keyword=None):
    super().__init__()
    self.__keyword = keyword
    self.__args = args
    assert len(self.__args) > 0

  @property
  def sql(self):
    if self.__keyword is None:
      return
    elif len(self.__args) == 1:
      return self.__args[0].sql
    else:
      return reduce(lambda arg1, arg2: f'{arg1.sql} {self.__keyword} {arg2.sql}', self.__args)


class AND(ConditionSQLArgument):
  def __init__(self, *args):
    super().__init__(*args, keyword='AND')


class Equal(OperatorSQLArgument):
  def __init__(self, field, bound):
    super().__init__(field, operator='=', bound=bound)


class NotEqual(OperatorSQLArgument):
  def __init__(self, field, bound):
    super().__init__(field, operator='<>', bound=bound)


class Lower(OperatorSQLArgument):
  def __init__(self, field, bound):
    super().__init__(field, operator='<=', bound=bound)


class Upper(OperatorSQLArgument):
  def __init__(self, field, bound):
    super().__init__(field, operator='>=', bound=bound)


class In(OperatorSQLArgument):
  def __init__(self, field, bound=None):
    super().__init__(field, operator='IN', bound=tuple(bound))


class NotIn(OperatorSQLArgument):
  def __init__(self, field, bound=None):
    super().__init__(field, operator='NOT IN', bound=tuple(bound))


class SQLArgumentFactory:
  @classmethod
  def between(self, field, lower_bound, upper_bound):
    return AND(Lower(field, upper_bound), Upper(field, lower_bound))
