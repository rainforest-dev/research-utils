from typing import Callable, List, Dict
from torch.utils.data.dataset import Dataset
from research_utils.sqlite.helper import Helper, FieldType
from research_utils.sqlite.sql import SQLArgument, SQLArgumentFactory

class DBFolder(Dataset):
  def __init__(
    self,
    db_path: str,
    table_name: str,
    fields: Dict[str, FieldType],
    argument: SQLArgument
  ) -> None:
    super().__init__()
    helper = Helper(
      db_path=db_path, 
      table_name=table_name,
      fields=fields
    )
    self.__rows = helper.query(
      fields=list(fields.keys()),
      argument=argument
    )
  
  def __len__(self):
    return len(self.__rows)
  
  def __getitem__(self, index):
    return self.__rows[index]