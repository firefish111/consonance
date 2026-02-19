#! /usr/bin/python

import flask
import sounds

# __name__ is the package name.
# we use this so that we can hunt for templates, static files, etc
app = flask.Flask(__name__)

@app.route("/")
def root():
  return flask.render_template("index.html")

app.run()
