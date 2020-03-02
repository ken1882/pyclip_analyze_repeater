import os.path
import pickle
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import _G

def get_auth_creds():
  if os.path.exists(_G.GDriveCredCache):
    with open(_G.GDriveCredCache, 'rb') as token:
      return pickle.load(token)
  return None

def load_creds_json(path):
  raw = _G.loadfile_with_resuce(_G.GDriveCredFilename, 'r')
  if not raw:
    raw = os.environ['CLIPPER_GDRIVE_CRED']
  return json.load(raw)

def start_auth_session(creds):
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      # TODO
      flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', _G.GDRIVE_SCOPES)
      creds = flow.run_local_server(port=0)
    with open('token.pickle', 'wb') as token:
      pickle.dump(creds, token)
  
  _G.GDriveService = build('drive', 'v3', credentials=creds)

def init():
  creds = get_auth_creds()
  start_auth_session(creds)

def download_data():

  

  results = service.files().list().execute()
  items = results.get('files', [])

  if not items:
    print('No files found.')
  else:
    print('Files:')
    for item in items:
      print("{} {}".format(item['name'], item['id']))

if __name__ == '__main__':
  download_data()