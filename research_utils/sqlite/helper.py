from typing import Dict, List
from enum import Enum
from functools import reduce
from sqlite_utils import Database
from .sql import SQLArgument

class FieldType(Enum):
  INTEGER = "INTEGER"
  FLOAT = "FLOAT"
  BOOL = "INTEGER"
  STRING = "TEXT"
  BLOB = "BLOB"


class Helper:
  def __init__(self, db_path, table_name, fields: Dict[str, FieldType], pk='id') -> None:
    self.__db = Database(db_path)
    self.__table_name = table_name
    self.__fields = fields

    if (not self.__db[self.__table_name].exists() and self.__fields is not None):
      self.__db[self.__table_name].create(self.__fields, pk=pk)
      print(f'created table: {self.__table_name}')
  
  @property
  def fields(self):
    return list(self.__fields.keys())
  @property
  def db(self):
    return self.__db

  def query(self, fields: List[str], argument: SQLArgument=None):
    select = reduce(lambda field1, field2: f'{field1}, {field2}', fields) if len(fields) > 0 else '*'
    sql = argument.sql if argument is not None else None
    print(select, sql)
    rows = self.__db[self.__table_name].rows_where(sql, select=select)
    return list(rows)