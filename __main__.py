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

# websocket ping/pong.
# pings the browser every 25s: if no response, then client has died.
# the browser automatically does this, and client-code doesn't need to care
app.config['SOCK_SERVER_OPTIONS'] = { 'ping_interval': 25 }

sock = flask_sock.Sock(app)

@app.route("/", methods=["GET"])
def root():
  return flask.render_template("index.html", defaults=defaults, input_data=input_data)

@app.route("/defaults", methods=["GET"])
def get_defaults():
  return flask.jsonify(defaults)

@sock.route("/soundify")
def soundify(ws):
  while True:
    # block until websocket pakcet received
    received = ws.receive()
    logging.debug(f"got ${received}")

    # try if failed to serialise
    try:
      ticket = to_ticket(received)
    except Exception as e:
      ws.send(serialise({ "type": "error", "message": "Malformed input: " + str(e) }))
      continue # ignore this current message, wait for next

    # if sentence does not exist or is empty
    if "sentence" not in ticket or not ticket["sentence"]:
      # no payloaad, so just a start and end packet in quick succession
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
        amplification_profile=synth.taper_by(ticket["taper"]) # TODO: consonants
      )
    except Exception as e:
      # broadcast error, such as word not in dictionary
      ws.send(serialise({ "type": "error", "message": str(e) }))
      continue

    # start message
    ws.send(serialise({ "type": "start", "n_packets": len(tones) }))

    # broadcast each tone as a packet
    for tone in tones:
      logging.debug(f"going to send {tone}")
      ws.send(serialise(tone))

    # end message
    ws.send(serialise({ "type": "end" }))

app.run()
