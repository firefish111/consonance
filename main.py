#! /usr/bin/python

# local import
from word import Word

# phonetic pangram
sentence = "The beige hue on the waters of the loch impressed all, including the French queen, before she heard that2 symphony again, just2 as2 young Arthur wanted."

for word in sentence.split(" "):
  w = Word(word.strip('.,'))
  print(w.pure_phones(), w.vowels())
