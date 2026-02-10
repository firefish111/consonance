import phones_list
from word import Word
import synth
import logging

def sentence_to_tones(secs_per_syllable, volume, text, *, stop_pause=0, break_pause=0, interword_pause=0, f_filter=(lambda x: x), amplification_profile=(lambda _: 1)):
  filtered = text \
    .replace(".", " !FULLSTOP ") \
    .replace(",", " !COMMA ") \
    .replace(";", " !COMMA ") \
    .replace(":", " !COMMA ")

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
        tones.append(synth.synth(secs_per_syllable, *f_filter(fm[0]), interpolate_with=f_filter(fm[1]), volume_profile=volume_profile))
      else: # otherwise we pretend nothing's happened
        tones.append(synth.synth(secs_per_syllable, *f_filter(fm[0]), volume_profile=volume_profile))

    tones.append(synth.pause(interword_pause))

  tones.append(synth.pause(secs_per_syllable))

  return tones

