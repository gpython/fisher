#encoding:utf-8

def is_isbn_or_key(word):
  """

  :param word:
  :return:
  """
  isbn_or_key = 'key'
  if len(word) == 13 and word.isdidit():
    isbn_or_key = 'isbn'

  short_q = q.replace('-', '')
  if '-' in q and len(short_q) == 10 and short_q.isdigit:
    isbn_or_key = 'isbn'

  return  isbn_or_key