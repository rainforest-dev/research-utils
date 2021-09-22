from .typing.sql import FieldOption
from .typing.operator import ConditionSQLArgument, OperatorSQLArgument
from typing import Dict, List, Tuple, Union
import logging
from pathlib import Path
import sqlite3
from sqlite3 import Error, Connection
from ..decorators.logging import logger


def create_db_if_not_exist(database) -> None:
  file = Path(database)
  file.parents[0].mkdir(parents=True, exist_ok=True)
  file.touch(exist_ok=True)
  logging.debug(f'{file} is created')


@logger()
def create_connection(database=':memory:', *args, **kwargs) -> Connection:
  """Create a Database Connection
  Args:
      database: {StrOrBytesPath} -- use ":memory:" to open a database 
          connection to a database that resides in RAM instead of on disk
      check_same_thread: {bool} -- If set False, the returned connection 
          may be shared across multiple threads {default: {True}}
  Returns:
      Connection: ...
  """

  if database != ':memory:':
    create_db_if_not_exist(database)

  conn = None
  try:
    conn = sqlite3.connect(database, *args, **kwargs)
  except Error as e:
    logging.error(e)
  return conn


def create_table(conn: Connection, table_name: str, fields: Dict[str, FieldOption]):
  """Create Table

  Args:
      conn (Connection): The Connection object
      table_name (str): Name of table
      fields (Dict[str, FieldOption]): Dictionary describing information of the fields
  """
  sql = ''.join((f'CREATE TABLE IF NOT EXISTS {table_name} (',
                 *(f'{key} {value.sql}{"," if index != len(fields) - 1 else ""}\n'
                   for index, (key, value) in enumerate(fields.items())), ');'))
  logging.info(sql)
  try:
    cur = conn.cursor()
    cur.execute(sql)
  except Error as e:
    logging.error(e)


def insert(conn: Connection, table_name: str, fields: Union[List[str], Tuple[str]],
           values: Union[List[Tuple], Tuple]):
  """Create Row or Rows into Custom Table

  Args:
      conn (Connection): The Connection object
      table_name (str): Name of table
      fields (Union[List[str], Tuple[str]]): 
      values (Union[List[Tuple], Tuple]): 
  """
  sql = f"""INSERT INTO {table_name} ({', '.join(map(str, fields))})
  VALUES
  ({', '.join(['?' for _ in fields])})
  """
  logging.info(sql)
  try:
    cur = conn.cursor()
    if isinstance(values, tuple):
      cur.execute(sql, values)
    else:
      cur.executemany(sql, values)
    conn.commit()
  except Error as e:
    logging.error(e)


@logger()
def query(conn: Connection,
          table_name: str,
          fields: Union[List[str], Tuple[str]] = None,
          where: Union[OperatorSQLArgument, ConditionSQLArgument] = None) -> List:
  """Query All Rows from Custom Table

  Args:
      conn (Connection): The Connection object
      table_name (str): Name of table
      fields (Union[List[str], Tuple[str]], optional): Defaults to None.
      where (Union[OperatorSQLArgument, ConditionSQLArgument], optional): Defaults to None.

  Returns:
      List: List of rows
  """

  sql = f"""SELECT {', '.join(map(str, fields)) if fields is not None and len(fields) > 0 else '*'} FROM {table_name}
  {f'WHERE {where.sql}' if where is not None else ''}
  """
  logging.info(sql)
  try:
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    return rows
  except Error as e:
    logging.error(e)
