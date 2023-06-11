from .base_cloud import BaseCloud
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

class GdriveCloud(BaseCloud):

    def __init__(self):
        gauth = GoogleAuth(settings_file='settings.yml')

        gauth.LoadCredentialsFile("mycreds.txt")
        if(gauth.credentials is None):
            gauth.LocalWebserverAuth()
        elif(gauth.access_token_expired):
            gauth.Refresh()
        else:
            gauth.Authorize()

        gauth.SaveCredentialsFile("mycreds.txt")

        self.drive = GoogleDrive(gauth)

    def upload_file(self, local_file_path):
        title = os.path.basename(local_file_path)
        print("@@ Creating file: " + title)
        f = self.drive.CreateFile({'title': title})

        print("@@ Setting content file: " + local_file_path)
        f.SetContentFile(local_file_path)
        
        print("@@ UPLOADING FILE TO GDRIVE: " + local_file_path)
        f.Upload()