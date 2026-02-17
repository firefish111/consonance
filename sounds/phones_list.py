"""
  Lookup table to a list of formant sets.
  Vowels can be exclusively defined by their first and second formant, so those are pairs.
  Stored as a list because diphthongs exist.

  Source is a melange of:
    https://home.cc.umanitoba.ca/~krussll/phonetics/acoustic/formants.html
    https://en.wikipedia.org/wiki/Formant#Phonetics
"""
vowels = {
  'æ': [(860, 1550)], # trap
  'ɐ': [(680, 1310)], # strut
  'ɒ': [(560,  820)], # lot
  'ə': [(500, 1500)], # comma
  'ɛ': [(600, 1930)], # dress
  'ɪ': [(370, 2090)], # kit
  'i': [(280, 2230)], # tidy - should merge with fleece
  'ʊ': [(400, 1100)], # foot

  # long vowels are just diphthongs that start and end in the same place
  'ɑː': [(830, 1170), (830, 1170)], # start
  'ɜː': [(400, 1310), (400, 1310)], # nurse
  'iː': [(280, 2230), (280, 2230)], # fleece
  'ɔː': [(430,  980), (430,  980)], # north
  'uː': [(330, 1260), (330, 1260)], # goose

  'aɪ': [(850, 1610), (370, 2090)], # price
  'eɪ': [(390, 2300), (370, 2090)], # face
  'aʊ': [(850, 1610), (400, 1100)], # mouth
  'əʊ': [(600, 1170), (400, 1100)], # goat
  'ɛə': [(600, 1930), (600, 1930)], # square (is diphthong in RP, not monophthong)
  'ɪə': [(370, 2090), (600, 1170)], # near
  'ɔɪ': [(500,  700), (370, 2090)], # choice
  'ʊə': [(585, 1710), (585, 1710)], # cure
}

consonants = [
  'b',
  'd',
  'dʒ',
  'ð',
  'f',
  'g',
  'h',
  'j',
  'k',
  'l',
  'm',
  'n',
  'ŋ',
  'p',
  'ɹ',
  's',
  'ʃ',
  't',
  'tʃ',
  'θ'
  'v',
  'w',
  'z',
  'ʒ',
]
