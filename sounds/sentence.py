from . import phones_list
from .word import Word
from . import synth

import logging
import re

# secs_per syllable = seconds per syllable
# volume = baseline volume. this is further affected by amplication_profile
# text = text to convert

# stop_pause = how long to pause after a full stop
# break_pause = how long to pause during a comma, semicolon, etc
# interword_pause = how long to pause between words

# formant_filter = if you wish to convert your formants into chords or other notes, this is called on them
# amplification_profile = amplification function that takes how far through out of 1 the tone is, returning a an amplication factor. used for fade in/out; this is separate from volume.
def sentence_to_tones(secs_per_syllable, volume, text, *, stop_pause=0, break_pause=0, interword_pause=0, formant_filter=(lambda x: x), amplification_profile=(lambda _: 1)):
  # replace punctuation marks with pseudo-word directives.
  # full stop, exclamation mark, and question mark all go to FULLSTOP (long pause).
  # comma, (semi-)colon, and parentheses all go to COMMA (short pause).
  filtered = re.sub("[.!?]", " !FULLSTOP ", text)
  filtered = re.sub("[,:;/()]", " !COMMA ", filtered)

  volume_profile = lambda progress: amplification_profile(progress) * volume

  tones = []
  for word in filtered.split():
    if not word: # if blank
      continue

    if word == "!FULLSTOP":
      tones.append(synth.pause(secs_per_syllable * stop_pause))
      continue
    elif word == "!COMMA":
      tones.append(synth.pause(secs_per_syllable * break_pause))
      continue

    w = Word(word.strip())
    if not w.raw:
      continue

    logging.debug(f"vowels: {w.vowels()}")
    for fm in (phones_list.vowels[phone] for phone in w.vowels()):
      # if there are (at least) two format sets, we pass the second one as interpolate_with
      if len(fm) >= 2:
        tones.append(synth.synth(secs_per_syllable, *formant_filter(fm[0]), interpolate_with=formant_filter(fm[1]), volume_profile=volume_profile))
      else: # otherwise we pretend nothing's happened
        tones.append(synth.synth(secs_per_syllable, *formant_filter(fm[0]), volume_profile=volume_profile))

    tones.append(synth.pause(interword_pause))

  return tones

