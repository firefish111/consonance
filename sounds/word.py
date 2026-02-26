from .phones_list import *
from . import parsing

table = parsing.get_table()

def purify(phones):
  return [ph.lstrip("ˈˌ") for ph in phones]

class Word:
  def __init__(self, word):
    cleanword = word.upper().strip()

    self.raw = cleanword
    # bits of word, used for splitting it up on word-internal punctuation
    bits = self.raw.replace("'", " '").replace("-", " ").strip().split()

    try:
      if self.raw[-1].isdigit(): # last letter is a number
        self.phones = table[self.raw[0:-1]][int(self.raw[-1]) - 1]
      elif self.raw not in table and all(bit.strip("1234567890") in table for bit in bits):
        # if the word itself does not exist, but each of the pieces do
        # recursively get words (will only be one layer deep)
        words = [Word(subword) for subword in bits]
        self.raw = ' '.join([w.raw for w in words])
        self.phones = [ph for w in words for ph in w.phones]
      else:
        self.phones = table[self.raw][0]
    except KeyError:
      if len(bits) > 1:
        raise KeyError(f"Word \"{cleanword}\" (or some part thereof) not in dictionary")
      else:
        raise KeyError(f"Word \"{cleanword}\" not in dictionary")
    except IndexError:
      raise IndexError(f"Word \"{cleanword[0:-1]}\" does not have pronunciation {cleanword[-1]}")

  # without stresses
  def pure_phones(self):
    return purify(self.phones)

  def vowels(self):
    return list(filter(lambda ph: ph in vowels, self.pure_phones()))

