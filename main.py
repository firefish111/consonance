#! /usr/bin/python

# local import
from chords import to_chord
from sentence import sentence_to_tones
import synth

# phonetic pangram
texts = {
  "pangram": "the quick brown fox jumps over the lazy dog",
  "phonopangram": "The beige hue on the waters of the loch impressed all, including the French queen, before she heard that2 symphony again, just2 as2 young Arthur wanted.",
  "panvowel": "trap strut lot the dress kit foot start nurse fleece north goose price face mouth goat square near choice cure",
  "beemovie": "According to all known laws of aviation, there is no way a bee should be able to fly. Its wings are too small to get its fat little body off the ground. The bee, of course, flies anyway because bees don't care what humans think is impossible. Yellow, black. Yellow, black. Yellow, black. Yellow, black. Black and yellow. Black and yellow. Black and yellow.",
  "shakespeare": "To be, or not to be. That is the question. Whether its noble in the mind to suffer the sling and arrow of outrageous fortune, or to take arms against a sea of troubles.",
  "bible": "In the beginning God created the heaven and the earth. And the earth was without form, and void; and darkness was upon the face of the deep. And the Spirit of God moved upon the face of the waters. And God said, Let there be light: and there was light. And God saw the light, that it was good: and God divided the light from the darkness. And God called the light Day, and the darkness he called Night. And the evening and the morning were the first day.",
  "paternoster": "Our Father, who art in heaven, shallow be thy name; thy kingdom come; thy will be done; on earth as it is in heaven. Give us this day our daily bread. And forgive us our trek pass 's, as we forgive those who trek pass against us. And lead us not into temptation; but deliver us from evil. For vine is the kingdom, the power and the glory, for ever and ever. Amen.",
}

TIME_PER_SYLLABLE = .35
VOLUME = .1

TEXT_ID = "beemovie"
print(f"Writing text '{TEXT_ID}'")

tones = sentence_to_tones(
  TIME_PER_SYLLABLE,
  VOLUME,
  texts[TEXT_ID],
  f_filter=to_chord,
  stop_pause=1.5,
  break_pause=0.7,
  interword_pause=0.025,
)

synth.write("out.wav", *tones)
