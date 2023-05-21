import os
import json
import re

def replace_special_numbers(string):
    pattern = r'[①-⑳]'  # match any circled number from 1 to 20
    char_map = {'①': '1', '②': '2', '③': '3', '④': '4', '⑤': '5',
                '⑥': '6', '⑦': '7', '⑧': '8', '⑨': '9', '⑩': '10',
                '⑪': '11', '⑫': '12', '⑬': '13', '⑭': '14', '⑮': '15',
                '⑯': '16', '⑰': '17', '⑱': '18', '⑲': '19', '⑳': '20'}
    return re.sub(pattern, lambda match: char_map[match.group()], string)


#TODO: Might wanna change this one, don't think it's very well done, figure out a better way to load settings maybe?
def create_default_config(config_file_path):
    default_config = {
        "save_folder": "MangaDeliveryTest",
        "base_url": "https://onepiecechapters.com",
        "mangalist_url": "https://onepiecechapters.com/projects",
        "titles_to_download": [],
        "save_format": "cbz"
    }

    print("Generating default one, please fill in the manga list")
    with open(config_file_path, 'w') as f:
        json.dump(default_config, f, indent=2)

def create_save_folder(save_folder):
# If main directory doens't exist then create it
    if not os.path.exists(save_folder):                   # TODO: add a folder icon for the luls
        os.makedirs(save_folder, 0o777)