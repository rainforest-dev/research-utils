import logging
from typing import Dict, Union
from pathlib import Path
import yaml
from research_utils.decorators.logging import logger

def str_to_class(module_name: str, class_name: str):
  import importlib
  module = importlib.import_module(module_name)
  return getattr(module, class_name)

@logger()
def load_yaml(path: Union[str, Path]) -> Dict:
  with open(path, "r") as stream:
    try:
      return yaml.safe_load(stream)
    except yaml.YAMLError as e:
      logging.error(e)