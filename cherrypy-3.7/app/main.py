#!/usr/bin/python

import bottle
import json

app = bottle.app()

@app.get('/')
def index():
  # return json.dumps({ 'message': 'hey friend!' })
  return "Hello"

# import logging
# import sys
# import requestlogger

# logged_app = requestlogger.WSGILogger(
#     app,
#     [logging.StreamHandler(stream=sys.stdout)],
#     requestlogger.ApacheFormatter())
