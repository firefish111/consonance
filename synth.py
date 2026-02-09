import math
import wave
import itertools

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
def synth(secs, amplitude, *args, **kwargs):
  # if we want to interpolate it into another tone
  if "interpolate_with" in kwargs:
    # zip: so we end up with tuples of (start, end), like so => (a_1, b_1), (a_2, b_2), (a_3, b_3), etc
    data = list(zip(args, kwargs["interpolate_with"]))

  for sample in range(round(secs * SAMPLE_RATE)): # tick for that many samples
    # t: progresses by 1 every second
    # theta: progresses by 2pi every second, as that ensures that a base sin wave has frequency of 1
    t = sample / SAMPLE_RATE
    theta = t * 2 * math.pi
    if "interpolate_with" in kwargs:
      wave = sum(math.sin(normalise(freqs, t, secs)) for freqs in data) * amplitude
    else:
      wave = sum(math.sin(theta * freq) for freq in args) * amplitude
    clamped = max(-1, min(wave, 1))

    yield min(255, math.floor((clamped + 1) * 128)) # map it onto 0-255

# pause: i.e. all samples are set to 0
def pause(secs):
  for sample in range(round(secs * SAMPLE_RATE)): # tick for that many samples
    yield 128 # zero

# takes list of generators
def write(name, *args):
  print(len(args))
  with wave.open(name, mode="wb") as wv:
    wv.setnchannels(1)
    wv.setsampwidth(1)
    wv.setframerate(SAMPLE_RATE)
    wv.writeframes(bytes(itertools.chain.from_iterable(args)))
