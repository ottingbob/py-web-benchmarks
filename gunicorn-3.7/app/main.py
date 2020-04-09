#!/usr/bin/python

from flask import Flask, jsonify

import sys

VERSION = "{}.{}".format(sys.version_info.major, sys.version_info.minor)

app = Flask(__name__)

@app.route("/")
def index():
  return jsonify("Hello")

def test(num1: int = 0, num2: int = 0) -> int:
  return num1 + num2

if __name__ == '__main__':
  print("Listening on 0.0.0.0::{0}".format(7331))
  app.run(host='0.0.0.0', port=7331)
