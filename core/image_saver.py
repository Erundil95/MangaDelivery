from io import BytesIO
import os
import zipfile
from  requests.exceptions import HTTPError, Timeout, ConnectionError
import cloudsave

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

        # Switch dictionary with savefile methods
        switch_dict = {
            'gdrive': Image_saver.save_on_gdrive,
            'icloud': Image_saver.save_on_icloud,
            'dropbox': Image_saver.save_on_dropbox,
            'onedrive': Image_saver.save_on_onedrive
        }

        if(cloud_service == None):
            print(f"Cloud saving disabled...")
            return True
        
        else:
            save_function = switch_dict.get(cloud_service)
            for i in range(max_retry_attempts):
                try: 
                    if(save_function is None):
                        print(f"Invalid cloud service {cloud_service}")
                    save_function(savefile_name)
                    return True
                except Exception as e:
                    print(f"Error while uploading {savefile_name}: {e}")
            
            #Reached max attempts
            print(f"Failed to upload {savefile_name} after {max_retry_attempts} attempts")

    # def sync_checker(chapter_path, ...)
 
    @staticmethod
    def save_on_gdrive(savefile_name):
        gdrive = cloudsave.gdrive_cloud.GdriveCloud()
        directory = os.path.dirname(savefile_name)
        manga_title = os.path.basename(directory)

        try:
            main_folder_id = gdrive.get_or_create_folder("MangaDelivery")

            folder_id = gdrive.get_or_create_folder(manga_title, main_folder_id)

            result = gdrive.upload_file(savefile_name, folder_id)
            print(result)
        except Exception as e:
            print(e)

    
    @staticmethod
    def save_on_icloud(savefile_name):
        pass
    
    @staticmethod
    def save_on_dropbox(savefile_name):
        pass

    @staticmethod
    def save_on_onedrive(savefile_name):
        pass
