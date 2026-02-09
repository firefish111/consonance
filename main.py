#! /usr/bin/python

# local import
import phones_list
from word import Word
import synth

# phonetic pangram
#sentence = "the quick brown fox jumps over the lazy dog"
#sentence = "The beige hue on the waters of the loch impressed all, including the French queen, before she heard that2 symphony again, just2 as2 young Arthur wanted."
#sentence = "trap strut lot the dress kit foot start nurse fleece north goose price face mouth goat square near choice cure"
#sentence = "According to all known laws of aviation, there is no way a bee should be able to fly. Its wings are too small to get its fat little body off the ground. The bee, of course, flies anyway because bees don't care what humans think is impossible. Yellow, black. Yellow, black. Yellow, black. Yellow, black. Black and yellow. Black and yellow. Black and yellow."
#sentence = "To be, or not to be. That is the question. Whether its noble in the mind to suffer the sling and arrow of outrageous fortune, or to take arms against a sea of troubles."
sentence = "In the beginning God created the heaven and the earth. And the earth was without form, and void; and darkness was upon the face of the deep. And the Spirit of God moved upon the face of the waters. And God said, Let there be light: and there was light. And God saw the light, that it was good: and God divided the light from the darkness. And God called the light Day, and the darkness he called Night. And the evening and the morning were the first day."

TIME_PER_SYLLABLE = .35
INTERWORD_PAUSE = .025
VOLUME = .1

filtered = sentence.replace(".", " !FULLSTOP ").replace(",", " !COMMA ").replace(";", " !COMMA ").replace(":", " !COMMA ")

tones = []
for word in filtered.split():
  if not word:
    continue

  if word == "!FULLSTOP":
    tones.append(synth.pause(TIME_PER_SYLLABLE * 1.5))
    continue
  elif word == "!COMMA":
    tones.append(synth.pause(TIME_PER_SYLLABLE * .75))
    continue

  w = Word(word.strip("., "))
  if not w.raw:
    continue

  print(w.vowels())
  for fm in (phones_list.vowels[phone] for phone in w.vowels()):
    # if there are (at least) two format sets, we pass the second one as interpolate_with
    if len(fm) >= 2:
      tones.append(synth.synth(TIME_PER_SYLLABLE, VOLUME, *fm[0], interpolate_with=fm[1]))
    else: # otherwise we pretend nothing's happened
      tones.append(synth.synth(TIME_PER_SYLLABLE, VOLUME, *fm[0]))

  tones.append(synth.pause(INTERWORD_PAUSE))

tones.append(synth.pause(TIME_PER_SYLLABLE))

synth.write("sentence.wav", *tones)
