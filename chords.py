import math
import logging

# 12th root 2: each semitone is this many times more than the one before it
semitone_step = 2**(1/12)
base_note = 440 # A4 is chosen as it is integer

# round a frequency to nearest semitone the semitone
def round_note(freq):
  # number of semitones we are away from A4
  semitones = math.log(freq/base_note, semitone_step)
  semitones = round(semitones) # round to integer

  # get exact frequency of that many semitones away from A4
  ret = (semitone_step ** semitones)*base_note
  logging.debug(f"rounding {freq}, which is {semitones} away from A4, to {ret}")
  return ret

# to make it not sound awful, we take the (f_1, f_2) tuple and convert it to a major cord
def to_chord(formants):
  # difference in formants. we use this as our top note in a major scale
  delta = formants[1] - formants[0]

  part = delta / 6

  # 4:5:6
  return (
    round_note(part * 4),
    round_note(part * 5),
    round_note(part * 6)
  )
