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
  print(args, len(args), kwargs)
  if "interpolate_with" in kwargs:
    mid = len(args) // 2
    data = list(zip(args, kwargs["interpolate_with"]))
    print(data, kwargs)

  for sample in range(round(secs * SAMPLE_RATE)): # tick for that many samples
    # theta: progresses by 2pi every second
    t = sample / SAMPLE_RATE
    theta = t * 2 * math.pi
    if "interpolate_with" in kwargs:
      wave = sum(math.sin(normalise(freqs, t, secs)) for freqs in data) * amplitude
    else:
      wave = sum(math.sin(theta * freq) for freq in args) * amplitude
    clamped = max(-1, min(wave, 1))

    yield math.floor((clamped + 1) * 127.5) # map it onto 0-255

# takes list of generators
def write(name, *args):
  print(len(args))
  with wave.open(name, mode="wb") as wv:
    wv.setnchannels(1)
    wv.setsampwidth(1)
    wv.setframerate(SAMPLE_RATE)
    wv.writeframes(bytes(itertools.chain.from_iterable(args)))
