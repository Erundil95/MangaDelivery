import os
import zipfile
import cloudsave
from io import BytesIO
from  requests.exceptions import HTTPError, Timeout, ConnectionError

class Image_saver:

    @staticmethod
    def save_images_as_cbz(images, chapter_dir, chapter_title, cloud_service=None):
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file_name, img_bytes in images:
                zip_file.writestr(file_name, img_bytes)

        zip_file_name = f"{chapter_title}.cbz"
        zip_buffer.seek(0)

        savefile_name = os.path.join(chapter_dir, zip_file_name)

        try:
            with open(savefile_name, "wb") as zip_file:
                zip_file.write(zip_buffer.read())
        except Exception as e:
            print(f"Error while saving {savefile_name}: {e}")
            return False

        if cloud_service:
            return Image_saver.save_on_cloud(savefile_name, cloud_service)

        
    @staticmethod
    def save_images_as_pdf(images, chapter_dir, chapter_title):
        return False
        #TODO: Copy this from the previous version of the program

    @staticmethod
    def save_on_cloud(savefile_name, cloud_service):
        max_retry_attempts = 5

        if(cloud_service == None):
            print(f"Cloud saving is disabled, saving only on local")
            return True
        
        else:
            cloud_instance = cloudsave.base_cloud.BaseCloud.get_cloud_service(cloud_service)

            for i in range(max_retry_attempts):
                try: 
                    cloud_instance.save_on_cloud(savefile_name)
                    return True
                except Exception as e:
                    print(f"Error while uploading {savefile_name}: {e}")
            
            #Reached max attempts
            print(f"Failed to upload {savefile_name} after {max_retry_attempts} attempts")
