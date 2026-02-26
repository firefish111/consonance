# default settings
defaults = {
  "time_per_syllable": .35,

  # 10% is still very loud, but we make that 50%
  "volume": .5,
  "volume_scale": .2,
  # a lower taper means taper period is shorter.
  # a very very small taper ends in basically a step function 0 -> 1 -> 0
  "taper": .35,

  # pause lengths in seconds
  "stop_pause": 1.5,
  "comma_pause": 0.7,
  "interword_pause": 0.025,
}

# what data (like label, limits) the input sliders should have
input_data = {
  "volume": {
    "name": "Volume",
    "type": "range",
    "bounds": (0.01, 0.01, 1), # min, step, max
    "percentage": True,
  },
  "taper": {
    "name": "Fade in/out (higher means more fading)",
    "type": "range",
    "bounds": (0.01, 0.01, 1), # min, step, max
    "percentage": True,
  },
  "time_per_syllable": {
    "name": "Time per syllable (seconds)",
    "type": "number",
    "bounds": (0.05, 0.05, 0.5), # min, step, max
    "percentage": False,
  },
  "stop_pause": {
    "name": "Pause per full stop (seconds)",
    "type": "number",
    "bounds": (0, 0.05, None), # min, step, max
    "percentage": False,
  },
  "comma_pause": {
    "name": "Pause per comma (seconds)",
    "type": "number",
    "bounds": (0, 0.05, None), # min, step, max
    "percentage": False,
  },
  "interword_pause": {
    "name": "Pause between words (seconds)",
    "type": "number",
    "bounds": (0, 0.005, None), # min, step, max
    "percentage": False,
  },
}

# keys that have [0,1] limit
limited_keys = ["volume", "volume_scale", "taper"]
