import logging
from typing import List
import pytest
import random
from research_utils.decorators.logging import Logging_Level, config_logger
from research_utils.sqlite.typing.sql import FieldType, NotNull, PrimaryKey
from research_utils.sqlite.typing.operator import Lower
from research_utils.sqlite.functional import create_connection, create_table, insert, query

table_name = 'test'
fields = {
    'id': PrimaryKey(FieldType.INTEGER),
    'name': NotNull(FieldType.STRING),
    'value': FieldType.FLOAT
}

logging.getLogger().setLevel(Logging_Level.DEBUG.value)


@pytest.mark.sqlite
def test_db_file():
  conn = create_connection('static/db.sqlite')

  assert conn is not None


@pytest.mark.sqlite
def test_db_memory():
  conn = create_connection()

  assert conn is not None


@pytest.mark.sqlite
def test_create_table():
  conn = create_connection('static/db.sqlite')
  create_table(conn, table_name=table_name, fields=fields)


@pytest.mark.sqlite
def test_insert_one():
  conn = create_connection('static/db.sqlite')
  insert(conn,
         table_name=table_name,
         fields=[key for key in fields.keys() if key != 'id'],
         values=('Rainforest', 'rainforest'))


@pytest.mark.sqlite
def test_insert_all():
  conn = create_connection('static/db.sqlite')
  insert(conn,
         table_name=table_name,
         fields=[key for key in fields.keys() if key != 'id'],
         values=[(f'Rainforest_{random.random()}', random.random())] * 10)


@pytest.mark.sqlite
def test_query_all():
  conn = create_connection('static/db.sqlite')
  rows = query(conn, table_name)

  assert rows is not None


@pytest.mark.sqlite
def test_query_fields():
  conn = create_connection('static/db.sqlite')
  rows = query(conn, table_name, [key for key in fields.keys() if key != 'id'])

  assert rows is not None


@pytest.mark.sqlite
def test_query_where():
  conn = create_connection('static/db.sqlite')
  rows = query(conn,
               table_name=table_name,
               fields=[key for key in fields.keys()],
               where=Lower('value', 0.5))

  assert rows is not None


import threading


@pytest.mark.sqlite
def test_multithreading():
  threads: List[threading.Thread] = []
  threads.append(threading.Thread(target=test_query_all))
  threads.append(threading.Thread(target=test_query_fields))
  threads.append(threading.Thread(target=test_query_where))

  for thread in threads:
    thread.start()