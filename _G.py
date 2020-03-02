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
GDriveCredCache = "secret/gdcredcache.dat"
GDriveService = None
DownloaderChunkSize = 1024 * 1024 * 16 # MB
MaxWorkerCount = 8

HttpStatus = {
  'ok': 200,
  'bad request': 400,
  'forbidden': 403,
  'not found': 404,
  'unprocessable': 422,
  'server overloaded': 503
}

ForbiddenFileChar = "\\\/:*<>\"?|"

app = Flask(AppName)