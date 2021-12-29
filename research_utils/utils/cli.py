def confirm(question: str) -> bool:
  """confirm in cli process

  Args:
      question (str): information of question

  Returns:
      bool: True to comfirm
  """
  answer = ''
  while answer not in ['y', 'yes', 'n', 'no']:
    answer = input(f'{question}[Y/N]').lower()
  return answer in ['y', 'yes']