#!/usr/bin/python

import falcon
import bjoern
import ujson

HOST = '0.0.0.0'
PORT = 7331

class IndexResource(object):
  def on_get(self, req, resp):
    resp.body = ujson.dumps({'Message': 'Hello friend!'})
    resp.status = falcon.HTTP_200

# instantiate a callable WSGI app
app = falcon.API()

# long-lived resource class instance
index_route = IndexResource()

# handle all requires to the '/' URL path
app.req_options.auto_parse_form_urlencoded = True
app.add_route('/', index_route)

print("Listening on {}:{}...".format(HOST, PORT))
bjoern.run(app, HOST, PORT, reuse_port=True)
