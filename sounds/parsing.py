import requests
from pathlib import Path

cachefile = Path("./.dlcache/britfone.csv")

if not cachefile.exists():
  r = requests.get(
    "https://raw.githubusercontent.com/JoseLlarena/Britfone/refs/heads/master/britfone.main.3.0.1.csv",
  )

  cachefile.parent.mkdir(exist_ok=True, parents=True)
  with cachefile.open('w') as f:
    f.write(r.text)

# debug = True calculates all phones as a set, and prints everything
def get_table(debug=False):
  table = {}

  if debug:
    allphones = set()

  with open(cachefile, 'r', encoding="utf-8") as f:
    for line in f.readlines():
      s = line.split(',')
      phones = s[1].strip().split(' ')

      # deal with multiple pronunciations
      word = s[0].split('(', 1)
      if word[0] not in table: # if first one, or only one
        table[word[0]] = []

      if debug:
        print(word[0], s)
      table[word[0]].append(phones)

      if debug:
        allphones.update([ph.lstrip("ˈˌ") for ph in phones])

  if debug:
    print(table)
    print()
    print(allphones)

  return table
