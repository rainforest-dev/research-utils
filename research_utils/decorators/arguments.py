from typing import Callable
import inspect
import functools

def ignore_unknown_kwargs(func: Callable):
  """Ignore unknown kwargs

  Args:
    func (Callable): 

  If the function already has the catch all **kwargs, do nothing.
  """
  if any(param.kind == inspect.Parameter.VAR_KEYWORD for param in inspect.signature(func).parameters.values()):
    return func

  @functools.wraps(func)
  def inner(*args, **kwargs):
    filtered_kwargs = {
      name: kwargs[name]
      for name, param in inspect.signature(func).parameters.items() if (
        param.kind is inspect.Parameter.KEYWORD_ONLY or
        param.kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
      ) and name in kwargs
    }
    return func(*args, **filtered_kwargs)
  return inner