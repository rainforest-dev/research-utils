import pytest

from research_utils.sqlite.utils import dict_to_values_sql


@pytest.mark.utils
def test_dict_to_values_sql():
  data = {'field1': 'value1', 'field2': 2}
  assert dict_to_values_sql(data) == 'field1="value1", field2="2"'
