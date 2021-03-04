from typing import Dict
from sqlite_utils import Database
from enum import Enum


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
