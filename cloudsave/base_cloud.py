from abc import ABC, abstractclassmethod

class BaseCloud(ABC):

    @abstractclassmethod
    def upload_file(self, local_file_path, remote_folder_info):
        pass

    # @abstractclassmethod
    # def delete_file(self, remote_file_info):
    #     pass

    @abstractclassmethod
    def create_folder(self, title):
        pass

    # @abstractclassmethod
    # def synch_files_with_local(self):
    #     pass