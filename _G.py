import os
from flask import Flask

def loadfile_with_resuce(filename, mode):
  try:
    with open(filename, mode) as file:
      return file.read()
  except FileNotFoundError:
    return None

HttpStatus = {
  200: 'ok',
  400: 'bad request',
  403: 'forbidden',
  404: 'not found',
  422: 'unprocessable entity',
  503: 'server overloaded'
}

def http_response(code, ret=None):
  ret = HttpStatus[code] if not ret else ""
  return ret, code

AppName = "ClipperRepeater"
APIKEY  = loadfile_with_resuce("secret/master.key", 'r') or os.environ['CLIPPER_SECRET']

GDriveScopes = ['https://www.googleapis.com/auth/drive']
GDriveCredFilename = "secret/credentials.json"
GDriveCredCache = "secret/gdcredcache.dat"
GDriveService = None
DownloaderChunkSize = 1024 * 1024 * 16 # MB
MaxWorkerCount = 8

ForbiddenFileChar = "\\\/:*<>\"?|"

app = Flask(AppName)