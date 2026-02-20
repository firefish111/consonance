#! /usr/bin/python

import flask
import flask_sock
import math
import json
import logging

# local import
from sounds.chords import to_chord
from sounds.sentence import sentence_to_tones
from sounds.serialise import serialise, to_ticket
from data import defaults, input_data, limited_keys

# __name__ is the package name.
# we use this so that we can hunt for templates, static files, etc
app = flask.Flask(__name__)

# TODO: heartbeat ping/pong
# app.config['SOCK_SERVER_OPTIONS'] = {'ping_interval': 25}

sock = flask_sock.Sock(app)

@app.route("/", methods=["GET"])
def root():
  return flask.render_template("index.html", defaults=defaults, input_data=input_data)

@app.route("/defaults", methods=["GET"])
def get_defaults():
  return flask.jsonify(defaults)

@sock.route("/soundify")
def soundify(ws):
  # TODO handle "word not in dictionary" exceptions
  while True:
    # block until websocket
    received = ws.receive()
    print("got", received)
    ticket = to_ticket(received)

    # if sentence does not exist or is empty
    if "sentence" not in ticket or not ticket["sentence"]:
      # no payload
      ws.send(serialise({ "type": "start", "n_packets": 0 }))
      ws.send(serialise({ "type": "end" }))
      continue

    # fill defaults
    for key in defaults:
      # if key is out of bounds: i.e. less than zero, or greater than one if that limit exists
      # or just not there at all (key not in ticket)
      if key not in ticket or \
         ticket[key] < 0 or \
         ((key in limited_keys) and ticket[key] > 1):
        ticket[key] = defaults[key]

    try:
      tones = sentence_to_tones(
        ticket["time_per_syllable"], # time per syllable
        ticket["volume"] * defaults["volume_scale"], # volume. we can't change volume scale, it's readonly
        ticket["sentence"],
        formant_filter=to_chord,
        stop_pause=ticket["stop_pause"],
        break_pause=ticket["comma_pause"],
        interword_pause=ticket["interword_pause"],
        amplification_profile=(lambda x: math.sin(math.pi * x) ** ticket["taper"]) # TODO: consonants
      )
    except Exception as e:
      ws.send(serialise({ "type": "error", "message": str(e) }))
      continue

    ws.send(serialise({ "type": "start", "n_packets": len(tones) }))

    for tone in tones:
      logging.debug(f"going to send {tone}")
      ws.send(serialise(tone))

    ws.send(serialise({ "type": "end" }))

app.run()
