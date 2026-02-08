import math
import wave
import itertools

SAMPLE_RATE = 8000 # in Hz

# generator
def synth(secs, amplitude, *args):
  for sample in range(round(secs * SAMPLE_RATE)): # tick for that many samples
    # theta: progresses by 2pi every second
    t = sample / SAMPLE_RATE
    theta = t * 8 * math.atan(1) # *2pi
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
