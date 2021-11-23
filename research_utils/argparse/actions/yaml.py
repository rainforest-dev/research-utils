from argparse import Action, ArgumentParser, Namespace
from typing import Any, Callable, Sequence, Tuple, Union


class YAMLAction(Action):
  """Argparser Action for Handling YAML file
  """
  def __init__(self, transform: Callable[[str], Union[Tuple[str, Any], Sequence[Tuple[str, Any]]]]=None, **kwargs) -> None:
    super().__init__(**kwargs)
    self._transform = transform

  def __call__(self,
               parser: ArgumentParser,
               namespace: Namespace,
               values: Union[str, Sequence[Any]],
               option_string: str = None) -> None:
    assert isinstance(values, str)
    if self._transform:
      delattr(namespace, self.dest)
      values = self._transform(values)
      if isinstance(values, Tuple):
        k, v = values
        setattr(namespace, k, v)
      elif isinstance(values, Sequence):
        for value in values:
          k, v = value
          setattr(namespace, k, v)
    else:
      setattr(namespace, self.dest, values)
