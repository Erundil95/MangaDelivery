from abc import ABC, abstractclassmethod
import cloudsave

class BaseCloud(ABC):

    @abstractclassmethod
    def upload_file(self, local_file_path, remote_folder_info) -> dict:
        pass

    @abstractclassmethod
    def delete_file(self, remote_file_info):
        pass

    @abstractclassmethod
    def create_folder(self, title) -> dict:
        pass

    @abstractclassmethod
    def synch_files_with_local(self, local_foler_path, remote_folder_info):
        pass
    
    @abstractclassmethod
    def save_on_cloud(self, savefile_name):
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
            raise ValueError(f"Invalid cloud service name: {cloud_service_type}")