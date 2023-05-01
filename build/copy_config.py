import shutil
import os

src = '..\\config\\config.json'
dst = 'dist\\config\\config.json'

os.makedirs(os.path.dirname(dst), exist_ok=True)
shutil.copyfile(src, dst)