from __future__ import annotations
import abc
from enum import Enum
from typing import Union


class SQLArgument:
  @property
  @abc.abstractmethod
  def sql(self):
    return NotImplemented


class FieldType(SQLArgument, Enum):
  @property
  def sql(self):
    return self.value

  INTEGER = "INTEGER"
  FLOAT = "FLOAT"
  BOOL = "INTEGER"
  STRING = "TEXT"
  BLOB = "BLOB"


class FieldOption(SQLArgument):
  def __init__(self, field: Union[FieldType, FieldOption], keyword: str = None):
    super().__init__()
    self.__field = field
    self.__keyword = keyword

  @property
  def sql(self):
    if self.__keyword is None:
      return
    else:
      return f'{self.__field.sql} {self.__keyword}'


class PrimaryKey(FieldOption):
  def __init__(self, field: Union[FieldType, FieldOption], keyword: str = 'PRIMARY KEY'):
    super().__init__(field, keyword=keyword)


class NotNull(FieldOption):
  def __init__(self, field: Union[FieldType, FieldOption], keyword: str = 'NOT NULL'):
    super().__init__(field, keyword=keyword)
