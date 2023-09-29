from .base_cloud import BaseCloud
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
from config.config_loader import ConfigLoader

# load at module import
config = ConfigLoader()
MAIN_FOLDER = 'MangaDelivery'

class GdriveCloud(BaseCloud):

    def __init__(self, drive):
        self.drive = drive

    @classmethod
    def create_with_authentication(cls):
        gauth = GoogleAuth(settings_file='settings.yml')

        if os.path.exists("mycreds.txt"):
            gauth.LoadCredentialsFile("mycreds.txt")

        if (gauth.credentials is None):
            gauth.LocalWebserverAuth()
        elif (gauth.access_token_expired):
            try:
                gauth.Refresh()
            except Exception as e:
                print("@@ WARNING: Your access token has expired and we couldn't refresh it.")
                print("@@ Deleting mycreds.txt")
                os.remove("mycreds.txt")
                gauth.LocalWebserverAuth()
        
        gauth.Authorize()

        gauth.SaveCredentialsFile("mycreds.txt")

        drive = GoogleDrive(gauth)
        return cls(drive)

    def save_on_cloud(self, savefile_name):                 #TODO: might wanna look at this, put everything into upload_file? 
        directory = os.path.dirname(savefile_name)
        manga_title = os.path.basename(directory)

        try:
            main_folder_info = self.get_or_create_folder("MangaDelivery")
            main_folder_id = main_folder_info['id']

            folder_info = self.get_or_create_folder(
                manga_title, main_folder_id)

            self.upload_file(savefile_name, folder_info)

        except Exception as e:
            print(e)

    def upload_file(self, local_file_path, remote_folder_info):
        filename = os.path.basename(local_file_path)
        file_info = self.get_file_info(filename)
        folder_id = remote_folder_info['id']

        file_id = file_info['id'] if file_info is not None else None

        if file_id:
            print("File already exists on Google Drive...")
        else:
            try:
                title = os.path.basename(local_file_path)

                print("@@ Creating file: " + title)
                f = self.drive.CreateFile({'title': title,
                                           'parents': [{'id': folder_id}]})

                print("@@ Setting content file: " + local_file_path)
                f.SetContentFile(local_file_path)

                print("@@ UPLOADING FILE TO GDRIVE: " + local_file_path)
                f.Upload()

                print("File uploaded successfully.")
                return f
            except Exception as e:
                print(e)
                raise Exception(f"Failed to upload {title} to Google Drive")

    def create_folder(self, title, parent_id=None):
        folder_metadata = {
            'title': title,
            'mimeType': 'application/vnd.google-apps.folder'
        }

        # If parent folded is provided then add to metadata
        if parent_id:
            folder_metadata['parents'] = [{'id': parent_id}]

        folder = self.drive.CreateFile(folder_metadata)
        folder.Upload()

        # Get folder info and print to console
        print(f"@@ Folder {title} created")
        return folder

    def get_folder_info(self, title, parent_id=None):
        query = f"title='{title}' and mimeType='application/vnd.google-apps.folder' and trashed=false"

        if parent_id:
            query += f" and '{parent_id}' in parents"

        file_list = self.drive.ListFile({'q': query}).GetList()

        if file_list:
            return file_list[0]
        else:
            return None

    def get_file_info(self, title, parent_id=None):
        query = f"title='{title}' and trashed=false"

        if parent_id:
            query += f" and '{parent_id}' in parents"

        file_list = self.drive.ListFile({'q': query}).GetList()

        if file_list:
            return file_list[0]
        else:
            return None
        
    def get_folder_contents(self, folder=MAIN_FOLDER):            #by default returns files in main foler
        query = f"'{self.get_folder_info(folder)['id']}' in parents and trashed=false"

        file_list = self.drive.ListFile({'q': query}).GetList()

        if file_list:
            return file_list
        else:
            return None        

    def get_or_create_folder(self, title, parent_id=None):
        folder_info = self.get_folder_info(title, parent_id)

        if folder_info is None:
            print(f"@@ Folder not found, creating folder named {title}")
            folder_info = self.create_folder(title, parent_id)

        return folder_info

    def delete_file(self, remote_file_name, parent_name):
        file_id = self.get_file_info(
            remote_file_name, self.get_folder_info(parent_name)['id'])['id']    #TODO: yeah this looks like shit ik

        try:
            file = self.drive.CreateFile({'id': file_id})
            file.Delete()
        except Exception as e:
            print('Error occured while deleting file %s' % e)