from __future__ import print_function
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import pandas as pd

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def create_token():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)
    return service

def get_root_folders(service):
    result = []
    page_token = None
    while True:
        response = service.files().list(q="mimeType='application/vnd.google-apps.folder' and name contains 'Meet Recordings'",
                                          spaces='drive',
                                          fields='nextPageToken, files(id, name)',
                                          pageToken=page_token).execute()
        for file in response.get("files", []):
            result.append(file)
        page_token = response.get('nextPageToken', None)
        if not page_token:
            # no more files
            break
    return result

def search_subfolders(service, folder_id):
    result = []
    page_token = None
    while True:
        response = service.files().list(q=f"mimeType='application/vnd.google-apps.folder' and '{folder_id}' in parents",
                                          spaces='drive',
                                          fields='nextPageToken, files(id, name)',
                                          pageToken=page_token).execute()
        for file in response.get("files", []):
            result.append(file)
        page_token = response.get('nextPageToken', None)
        if not page_token:
            break
    return result

def search_recordings(service, folder_id, date):
    result = []
    page_token = None
    while True:
        response = service.files().list(q=f"mimeType='video/mp4' and '{folder_id}' in parents and createdTime > '{date}T00:00:00'",
                                          spaces='drive',
                                          fields='nextPageToken, files(id, name, webViewLink,createdTime,owners/emailAddress, videoMediaMetadata/durationMillis)',
                                          pageToken=page_token).execute()
        for file in response.get("files", []):
            result.append(file)
        page_token = response.get('nextPageToken', None)
        if not page_token:
            break
    return result

def get_subfolders(service, root_folders):
    subfolders = []
    for folder in root_folders:
        sub_folders = search_subfolders(service, folder["id"])
        subfolders += sub_folders
    root_folders += subfolders
    return root_folders

def get_recordings(service, sub_folders, date):
    all_recordings = []
    for folder in sub_folders:
        recordings = search_recordings(service, folder["id"], date)
        all_recordings += recordings
    for recording in all_recordings:
        recording["owners"] = recording["owners"][0]['emailAddress']
        recording["videoMediaMetadata"] = recording["videoMediaMetadata"]["durationMillis"] if "videoMediaMetadata" in recording else 0
    return all_recordings

