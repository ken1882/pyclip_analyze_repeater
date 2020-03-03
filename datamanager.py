import io
import os.path
import pickle
import json
import time
from threading import Thread
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import _G

# Goole Drive File Downloader
class Downloader:
  def __init__(self, id):
    self.id = id
    self.filename   = ""
    self.downloader = None
    self.progress   = 0
    self.thread     = None
    self.flag_complete = False
  
  # setup before the download
  def setup(self):
    self.header = _G.GDriveService.files().get(fileId=self.id).execute()
    self.request = _G.GDriveService.files().get_media(fileId=self.id)

  # start download
  def start(self):
    self.filename = self.header['name'].replace(_G.ForbiddenFileChar, '')
    stream = io.FileIO(self.filename, 'wb')
    self.downloader = MediaIoBaseDownload(stream, self.request)
    self.downloader._chunksize = _G.DownloaderChunkSize
    self.thread = Thread(target=self.download)
    self.thread.start()

  # async download the file
  def download(self):
    while self.flag_complete is False:
      stat, self.flag_complete = self.downloader.next_chunk()
      self.progress = int(stat.progress() * 100)
  
  def is_completed(self):
    return self.flag_complete

def get_auth_creds():
  if not os.path.exists('secret/'):
    os.mkdir('secret')
  if os.path.exists(_G.GDriveCredCache):
    with open(_G.GDriveCredCache, 'rb') as token:
      return pickle.load(token)
  return None
 
def load_creds_json():
  raw = _G.loadfile_with_resuce(_G.GDriveCredFilename, 'r')
  if not raw:
    raw = os.environ['CLIPPER_GDRIVE_CREDS']
  return json.loads(raw)
 
def start_auth_session(creds):
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_config(load_creds_json(), _G.GDriveScopes)
      creds = flow.run_local_server(port=0)
    with open(_G.GDriveCredCache, 'wb') as file:
      pickle.dump(creds, file)
 
  _G.GDriveService = build('drive', 'v3', credentials=creds)
 
def download_data_async(id):
  worker = Downloader(id)
  worker.setup()
  worker.start()
  return worker

def init():
  creds = get_auth_creds()
  start_auth_session(creds)