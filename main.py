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
sentence = "According to all known laws of aviation, there is no way a bee should be able to fly. Its wings are too small to get its fat little body off the ground. The bee, of course, flies anyway because bees don't care what humans think is impossible. Yellow, black. Yellow, black. Yellow, black. Yellow, black. Black and yellow. Black and yellow. Black and yellow."

TIME_PER_SYLLABLE = .3
VOLUME = .1

tones = []
for word in sentence.split(" "):
  w = Word(word.strip('.,'))
  print(w.vowels())
  for fm in (phones_list.vowels[phone] for phone in w.vowels()):
    if len(fm) >= 2:
      tones.append(synth.synth(TIME_PER_SYLLABLE, VOLUME, *fm[0], interpolate_with=fm[1]))
    else:
      tones.append(synth.synth(TIME_PER_SYLLABLE, VOLUME, *fm[0]))

synth.write("sentence.wav", *tones)
