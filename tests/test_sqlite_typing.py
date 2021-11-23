import pytest
from research_utils.sqlite.typing.sql import FieldType

@pytest.mark.sqlite
def test_to_str():
  assert str(FieldType.FLOAT) == 'FLOAT'