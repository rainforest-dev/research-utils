def convertToBinaryData(filename):
  with open(filename, 'rb') as file:
    blob = file.read()
  return blob

def extractDictByKeys(dict: dict, fields):
  return [dict.get(field) for field in fields]