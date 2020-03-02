import os
from flask import Flask

def loadfile_with_resuce(filename, mode):
  try:
    with open(filename, mode) as file:
      return file.read()
  except FileNotFoundError:
    return None

AppName = "ClipperRepeater"
APIKEY  = loadfile_with_resuce("secret/master.key", 'r') or os.environ['CLIPPER_SECRET']

GDriveScopes = ['https://www.googleapis.com/auth/drive']
GDriveCredFilename = "secret/credentials.json"
GDriveCredCache = "secret/gdrivecache.dat"
GDriveService = None

app = Flask(AppName)