from research_utils.decorators.arguments import ignore_unknown_kwargs


def test_ignore_unknown_kwargs():
  @ignore_unknown_kwargs
  def positional_or_keywords(x, y):
    return x, y

  @ignore_unknown_kwargs
  def keyword_with_default(x, y, z=True):
    return x, y, z

  @ignore_unknown_kwargs
  def variable_length(x, y, *args, **kwargs):
    return x, y, args, kwargs

  @ignore_unknown_kwargs
  def keyword_only(x, *, y):
    return x, y

  assert (positional_or_keywords(x=3, y=5, z=10))
  assert (positional_or_keywords(3, y=5))
  assert (positional_or_keywords(3, 5))
  assert (positional_or_keywords(3, 5, z=10))
  assert (keyword_with_default(2, 2))
  assert (keyword_with_default(2, 2, z=False))
  assert (keyword_with_default(2, 2, False))
  assert (variable_length(2, 3, 5, 6, z=3))
  assert (keyword_only(1, y=3))
