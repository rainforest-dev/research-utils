import logging
from typing import Dict, List, Union
from numbers import Number
from itertools import chain
from tempfile import TemporaryFile
from pathlib import Path
import yaml
import numpy as np
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


def flatten(raw: List[Union[tuple, Number]]):
  # [reference](https://stackoverflow.com/a/22569169)
  return list(chain(*(i if isinstance(i, tuple) else (i, ) for i in raw)))


def npy2tmpfile(data: np.ndarray):
  # [reference](https://numpy.org/doc/stable/reference/generated/numpy.save.html)
  file = TemporaryFile()
  np.save(file, data)
  _ = file.seek(0)
  return file


def conditional_kwargs(*args, conditional: bool = True, **kwargs):
  """return custom kwargs while conditional is True

  Args:
      conditional (bool): if conditional is True, return kwargs

  Returns:
      dict: kwargs
  """
  if conditional:
    return kwargs
  return {}


def dict_union(*args):
  return dict(chain.from_iterable(d.items() for d in args))


def ensure_path_existed(*args) -> Path:
  path = Path(*args)
  path.mkdir(parents=True, exist_ok=True)
  return path
