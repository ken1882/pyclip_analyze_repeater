from flask import request, jsonify
import _G

app = _G.app

@app.route("/", methods=["GET","POST"])
def index():
  return "Hello World!"