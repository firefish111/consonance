#! /usr/bin/python

import itertools

# local import
import phones_list
from word import Word
import synth

# phonetic pangram
#sentence = "the quick brown fox jumps over the lazy dog"
#sentence = "The beige hue on the waters of the loch impressed all, including the French queen, before she heard that2 symphony again, just2 as2 young Arthur wanted."
#sentence = "trap strut lot the dress kit foot start nurse fleece north goose price face mouth goat square near choice cure"
sentence = "According to all known laws of aviation, there is no way a bee should be able to fly. Its wings are too small to get its fat little body off the ground. The bee, of course, flies anyway because bees don't care what humans think is impossible. Yellow, black. Yellow, black. Yellow, black. Yellow, black."

tones = []
for word in sentence.split(" "):
  w = Word(word.strip('.,'))
  print(w.vowels())
  formants = itertools.chain.from_iterable(
    phones_list.vowels[phone] for phone in w.vowels()
  )

  for fm in formants:
    tones.append(synth.synth(.2, .1, *fm))

synth.write("sentence.wav", *tones)
