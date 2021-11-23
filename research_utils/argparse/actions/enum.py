from typing import Any, Sequence, Union
from argparse import Action, ArgumentParser, Namespace
from enum import Enum

class EnumAction(Action):
  """Argparser Action for Handling Enums
  References:
    [Support for Enum arguments in argparse](https://stackoverflow.com/a/60750535)
  """
  def __init__(self, **kwargs) -> None:
    # Pop off the type value
    enum_type = kwargs.pop('type', None)

    # Ensure an Enum subclass is provided
    if enum_type is None:
      raise ValueError('Type must be assigned an Enum when using EnumAction')
    if not issubclass(enum_type, Enum):
      raise TypeError('Type must be an Enum when using EnumAction')

    # Generate choices from the Enum
    kwargs.setdefault("choices", tuple(e.name for e in enum_type))
    super().__init__(**kwargs)

    self._enum = enum_type

  def __call__(self, parser: ArgumentParser, namespace: Namespace, values: Union[str, Sequence[Any]], option_string: str = None) -> None:
    # Convert value back into an Enum
    value = self._enum[values]
    setattr(namespace, self.dest, value)