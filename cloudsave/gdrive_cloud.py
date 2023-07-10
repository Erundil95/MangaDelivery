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
            try:
                gauth.Refresh()
            except Exception as e:
                #TODO: make this automatic, delete txt and relaunch program
                print("Your access token has expired and we couldn't refresh it.")
                print("Delete mycreds.txt to refresh.")

                print(f"Error: {e}")
                gauth.LocalWebserverAuth()
        else:
            gauth.Authorize()

        gauth.SaveCredentialsFile("mycreds.txt")

        self.drive = GoogleDrive(gauth)

    def upload_file(self, local_file_path, folder_id):
        filename = os.path.basename(local_file_path)
        file_id = self.get_file_id(filename)

        if file_id:
            try:
                title = os.path.basename(local_file_path)

                print("@@ Creating file: " + title)
                f = self.drive.CreateFile({'title': title, 
                                           'parents': [{'id' : folder_id}]})

                print("@@ Setting content file: " + local_file_path)
                f.SetContentFile(local_file_path)
        
                print("@@ UPLOADING FILE TO GDRIVE: " + local_file_path)
                f.Upload()

                return "File uploaded successfully."
            except Exception as e:
                print(e)
                raise Exception(f"Failed to upload {title} to Google Drive")
        
    def create_folder(self, title, parent_id = None):
        folder_metadata = {
            'title' : title,
            'mimeType' : 'application/vnd.google-apps.folder'
        }

        # If parent folded is provided then add to metadata
        if parent_id:
            folder_metadata['parents'] = [{'id' : parent_id}]

        folder = self.drive.CreateFile(folder_metadata)
        folder.Upload()

        # Get folder info and print to console
        print(f"@@ Folder {title} created")
        return folder['id']
    
    def get_folder_id(self, title, parent_id = None):
        query = f"title='{title}' and mimeType='application/vnd.google-apps.folder' and trashed=false"

        if parent_id:
            query += f" and '{parent_id}' in parents"

        file_list = self.drive.ListFile({'q': query}).GetList()

        if file_list:
            return file_list[0]['id']
        else:
            return None
        
    def get_file_id(self, title, parent_id = None):
        query = f"title='{title}' and trashed=false"

        if parent_id:
            query += f" and '{parent_id}' in parents"

        file_list = self.drive.ListFile({'q': query}).GetList()

        if file_list:
            return file_list[0]['id']
        else:
            return None
        
    def get_or_create_folder(self, title, parent_id = None):
        folder_id = self.get_folder_id(title, parent_id)

        if folder_id is None:
            print(f"@@ Folder not found, creating folder named {title}")
            folder_id = self.create_folder(title, parent_id)

        return folder_id