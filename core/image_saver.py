from io import BytesIO
import os
import zipfile
from  requests.exceptions import HTTPError, Timeout, ConnectionError

class Image_saver:
    @staticmethod
    def save_images_as_cbz(images, chapter_dir, chapter_title):
        zip_buffer = BytesIO()

        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file_name, img_bytes in images:
                zip_file.writestr(file_name, img_bytes)

        zip_file_name = f"{chapter_title}.cbz"
        zip_buffer.seek(0)

        with open(os.path.join(chapter_dir, zip_file_name), "wb") as zip_file:
            zip_file.write(zip_buffer.read())

        
    @staticmethod
    def save_images_as_pdf(images, chapter_dir, chapter_title):
        return False
        #TODO: Copy this from the previous version of the program