from flask import request, jsonify
from _G import HttpStatus
import _G

app = _G.app

@app.route("/", methods=["GET","POST"])
def index():
  return "Hello World!"

@app.route("/api/analyze/<id>", methods=["POST"])
def analyze(id):
  return "Received " + id, HttpStatus['ok']