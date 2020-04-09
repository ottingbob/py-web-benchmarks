#!/usr/bin/python

import hug
import bjoern
import ujson

HOST = '0.0.0.0'
PORT = 7331

@hug.get('/', versions=1)
def index():
  return ujson.dumps({'Message': 'Hello friend!'})

app = __hug_wsgi__
print("Listening on {}:{}...".format(HOST, PORT))
bjoern.run(app, HOST, PORT, reuse_port=True)
