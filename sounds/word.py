from .phones_list import *
from . import parsing

table = parsing.get_table()

def purify(phones):
  return [ph.lstrip("ˈˌ") for ph in phones]

class Word:
  def __init__(self, word):
    cleanword = word.upper().strip()

    self.raw = cleanword
    try:
      if self.raw[-1].isdigit(): # last letter is a number
        self.phones = table[self.raw[0:-1]][int(self.raw[-1]) - 1]
      else:
        self.phones = table[self.raw][0]
    except KeyError:
      raise KeyError(f"Word \"{cleanword}\" not in dictionary")
    except IndexError:
      raise IndexError(f"Word \"{cleanword[0:-1]}\" does not have pronunciation {cleanword[-1]}")

  # without stresses
  def pure_phones(self):
    return purify(self.phones)

  def vowels(self):
    return list(filter(lambda ph: ph in vowels, self.pure_phones()))

