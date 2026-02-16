import math
import logging

# 12th root 2: each semitone is this many times more than the one before it
semitone_step = 2**(1/12)
base_note = 440 # A4 is chosen as it is integer

# step up note by semitones
def step_up(freq, by):
  return freq * (semitone_step)**by

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
def base_to_chord(base):
  # so apparently sounds less worse when "base" is top note, not root note of chord?
  root = round_note(base * 4 / 6)

  # 4:5:6, except made to fit 12-tet
  return (
    root,
    step_up(root, 4),
    step_up(root, 7),
  )

# converts fomants into two major chords, where those formants are the base frequencies of the chords
def to_chord(formants):
  # sum here chains tuples together
  return sum((base_to_chord(form) for form in formants), ())
