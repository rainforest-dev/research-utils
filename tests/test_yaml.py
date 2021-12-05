from argparse import ArgumentParser
from typing import Dict
import pytest
from research_utils.argparse.actions.yaml import YAMLAction
from research_utils.sqlite.yaml import parse_fields, parse_where
from research_utils.utils import load_yaml


@pytest.mark.yaml
def test_load_yaml():
  assert isinstance(load_yaml('tests/static/db01.yaml'), Dict)


@pytest.mark.yaml
def test_get_fields():
  data = load_yaml('tests/static/db01.yaml')
  parse_fields(data['nacre'])
  parse_where(data['nacre'])
  assert (data['nacre']['where'].sql == 'density <= 1 AND density >= 0 AND total_area <= 0.25')


@pytest.mark.yaml
def test_get_fields_02():
  data = load_yaml('tests/static/db02.yaml')
  parse_fields(data['nacre'])
  parse_where(data['nacre'])
  assert (data['nacre']['where'].sql == 'density <= 1 AND density >= 0')


@pytest.mark.argparse
def test_yaml_action_with_transform():
  def transform(path):
    data = load_yaml(path)
    table_name, data = list(data.items())[0]
    parse_fields(data)
    parse_where(data)
    return [('table_name', table_name), ('fields', data['fields']), ('argument', data['where'])]

  parser = ArgumentParser()
  parser.add_argument('--yaml', action=YAMLAction, transform=transform)
  args = parser.parse_args(['--yaml', 'tests/static/db01.yaml'])
  assert args.table_name == 'nacre'
  assert (args.fields is not None)
  assert (args.argument is not None)
  assert 'yaml' not in args


@pytest.mark.argparse
def test_yaml_action():
  parser = ArgumentParser()
  parser.add_argument('--yaml', action=YAMLAction)
  args = parser.parse_args(['--yaml', 'static/db01.yaml'])
  assert args.yaml == 'static/db01.yaml'
