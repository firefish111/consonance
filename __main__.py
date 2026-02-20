#! /usr/bin/python

import flask
import flask_sock
import math
import json
import logging

# local import
from sounds.chords import to_chord
from sounds.sentence import sentence_to_tones
from sounds.serialise import serialise

# __name__ is the package name.
# we use this so that we can hunt for templates, static files, etc
app = flask.Flask(__name__)

# TODO: heartbeat ping/pong
# app.config['SOCK_SERVER_OPTIONS'] = {'ping_interval': 25}

sock = flask_sock.Sock(app)

@app.route("/")
def root():
  return flask.render_template("index.html")

@sock.route("/soundify")
def soundify(ws):
  # TODO replace with config
  # TODO handle dictionary exceptions
  while True:
    # block until websocket
    data = ws.receive()
    logging.debug(f"got: {data}")


    tones = sentence_to_tones(
      .35, # time per syllable
      .1,  # volume
      "the quick brown fox, however, jumps over the lazy dog.",
      formant_filter=to_chord,
      stop_pause=1.5,
      break_pause=0.7,
      interword_pause=0.025,
      amplification_profile=(lambda x: math.sin(math.pi * x) ** .35) # TODO: change
    )

    ws.send(serialise({ "type": "initial", "n_packets": len(tones) }))

    # TODO implement pauses
    for tone in tones:
      logging.debug(f"going to send {tone}")
      ws.send(serialise(tone))

app.run()
