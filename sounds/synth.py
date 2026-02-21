import math
import wave
import itertools
import logging

SAMPLE_RATE = 8000 # in Hz

def normalise(freqs, t, total):
  n = freqs[0] + (freqs[1] - freqs[0])*(t/total)
  n *= 2 * math.pi
  if freqs[1] > freqs[0]:
    n *= t
  else:
    n *= (total - t)
  return n

# generator
def synth(secs, *tones, volume_profile=(lambda progress: 1), interpolate_with=None):
  # if we want to interpolate it into another tone
  if interpolate_with is not None:
    # zip: so we end up with tuples of (start, end), like so => (a_1, b_1), (a_2, b_2), (a_3, b_3), etc
    data = list(zip(tones, interpolate_with))

  for sample in range(round(secs * SAMPLE_RATE)): # tick for that many samples
    # t: progresses by 1 every second
    # theta: progresses by 2pi every second, as that ensures that a base sin wave has frequency of 1
    t = sample / SAMPLE_RATE
    theta = t * 2 * math.pi

    # progress of the way through the sound, out of 1
    progress = t / secs

    # to make pitches less uniform and more natural
    noise = math.sin(theta * 2 + progress)

    if interpolate_with is not None:
      wave = sum(math.sin(normalise(freqs, t, secs) + noise) for freqs in data) * volume_profile(progress)
    else:
      wave = sum(math.sin(theta * freq + noise) for freq in tones) * volume_profile(progress)
    clamped = max(-1, min(wave, 1))

    yield min(255, math.floor((clamped + 1) * 128)) # map it onto 0-255

# pause: i.e. all samples are set to 0
def pause(secs):
  for sample in range(round(secs * SAMPLE_RATE)): # tick for that many samples
    yield 128 # zero

# takes list of generators
def write(name, *streams):
  logging.debug(f"writing {len(streams)} streams")
  with wave.open(name, mode="wb") as wv:
    wv.setnchannels(1)
    wv.setsampwidth(1)
    wv.setframerate(SAMPLE_RATE)
    wv.writeframes(bytes(itertools.chain.from_iterable(streams)))
