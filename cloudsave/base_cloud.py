from abc import ABC, abstractclassmethod
from config.config_loader import ConfigLoader
import cloudsave
import os

import sys


class BaseCloud(ABC):

    @abstractclassmethod
    def upload_file(self, local_file_path, remote_folder_info) -> dict:
        pass

    @abstractclassmethod
    def delete_file(self, remote_file):
        pass

    @abstractclassmethod
    def create_folder(self, title) -> dict:
        pass

    @abstractclassmethod
    def save_on_cloud(self, savefile_name):
        pass

    @abstractclassmethod
    def get_folder_contents(self, folder_name):
        pass

    @staticmethod
    def get_cloud_service(cloud_service_type):
        cloud_classes = {
            "gdrive": cloudsave.gdrive_cloud.GdriveCloud,
            # "icloud": cloudsave.icloud_cloud.IcloudCloud,       # not implemented yet
            # "dropbox": cloudsave.dropbox_cloud.DropboxCloud,    # not implemented yet
            # "onedrive": cloudsave.onedrive_cloud.OnedriveCloud  # not implemented yet
        }

        try:
            return cloud_classes[cloud_service_type]()
        except:
            raise ValueError(
                f"Invalid cloud service name: {cloud_service_type}")

    def synch_files_with_local(self, manga_name):
        config_loader = ConfigLoader()
        local_folder_path = os.path.join(
            config_loader.get_setting('save_folder'), manga_name)
        max_files_on_cloud = config_loader.get_setting(
            'titles_to_download')[manga_name]

        local_file_list = sorted(os.listdir(local_folder_path), reverse=True)[
            :max_files_on_cloud]
        local_file_set = set(local_file_list)

        try:
            remote_file_list = sorted(
                [elem['title'] for elem in self.get_folder_contents(manga_name)], reverse=True)
            remote_file_set = set(remote_file_list)
        except Exception as e:
            print(e)
            raise Exception(f"Failed to retrieve file list from cloud")
        
        print(f'Syncronizing files with cloud storage for {manga_name}...')

        for file in local_file_set - remote_file_set:
            print(f'Sync Uploading file: {file}')
            filepath = os.path.join(local_folder_path, file)
            self.save_on_cloud(filepath)
            
        for file in remote_file_set - local_file_set:
            print(f'Sync Deleting remote file: {file}')
            self.delete_file(file, manga_name)

        print(f'Syncronization completed!')
