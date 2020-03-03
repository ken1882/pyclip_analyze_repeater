from flask import request, jsonify
from _G import http_response
import _G

app = _G.app

active_worker_cnt = 0

def params(*args):
  return {key: request.args.get(key) for key in args}

@app.route("/", methods=["GET","POST"])
def index():
  return "Hello World!"

@app.route("/api/analyze", methods=["POST"])
def analyze():
  global active_worker_cnt
  if active_worker_cnt < _G.MaxWorkerCount:
    id, token = params('id', 'token')
    return http_response(200)
  else:
    return http_response(503)
    