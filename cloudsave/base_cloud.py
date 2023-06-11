from abc import ABC, abstractclassmethod

class BaseCloud(ABC):

    @abstractclassmethod
    def upload_file(self, local_file_path, remote_file_path):
        pass

    # @abstractclassmethod
    # def delete_file(self, remote_file_path):
    #     pass

