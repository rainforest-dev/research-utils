from enum import Enum
from typing import Dict, Sequence, Union
from research_utils.sqlite.typing.sql import FieldType
from research_utils.utils import str_to_class


class SQLArgumentEnum(Enum):
  AND = ('research_utils.sqlite.typing.operator', 'AND')
  BETWEEN = ('research_utils.sqlite.typing.operator', 'SQLArgumentFactory', 'between')
  LOWER = ('research_utils.sqlite.typing.operator', 'Lower')
  UPPER = ('research_utils.sqlite.typing.operator', 'Upper')
  IN = ('research_utils.sqlite.typing.operator', 'In')
  NOT_IN = ('research_utils.sqlite.typing.operator', 'NotIn')

  def __call__(self, *args, **kwargs):
    try:
      module_name, class_name, method_name = self.value
      c = str_to_class(module_name, class_name)
      c = getattr(c, method_name)
      return c(*args, **kwargs)
    except:
      module_name, class_name = self.value
      c = str_to_class(module_name, class_name)
      return c(*args, **kwargs)


def parse_fields(data: Dict):
  if 'fields' in data:
    data.update(fields={k: FieldType[v] for k, v in data['fields'].items()})


def parse_where(data: Dict):
  def parse_sql_argument(node: Dict[str, Union[Dict, Sequence]]):
    assert len(node) == 1
    node = list(node.items())[0]
    key, value = node
    # for AND,...
    if isinstance(value, Sequence):
      return SQLArgumentEnum[key](*[parse_sql_argument(item) for item in value])
    # for BETWEEN, LOWER, UPPER, IN, NOT_IN,...
    elif isinstance(value, Dict):
      args = value.get('args', [])
      kwargs = value.get('kwargs', {})
      return SQLArgumentEnum[key](*args, **kwargs)

  if 'where' in data:
    data.update(where=parse_sql_argument(data['where']))
