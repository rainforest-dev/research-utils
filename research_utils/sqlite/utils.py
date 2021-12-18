def convertToBinaryData(filename):
  with open(filename, 'rb') as file:
    blob = file.read()
  return blob


def extractDictByKeys(dict: dict, fields):
  return [dict.get(field) for field in fields]


def dict_to_values_sql(data: dict):
  return ', '.join(map(lambda item: f'{item[0]}="{str(item[1])}"', data.items()))