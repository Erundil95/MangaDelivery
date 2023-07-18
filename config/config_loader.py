import json
import os
from utils.singleton import Singleton
from utils import utils

class ConfigLoader(metaclass = Singleton):
    
    def __init__(self):
        # Load JSON config file = current_dir path + going up one level with '..' + config + config.json
        try:
            self.config_file = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config.json'))
            self.config = self.load_config()
        except FileNotFoundError:
            print(f"@@ Config file not found at {self.config_file}")
            utils.create_default_config(self.config_file)

    def load_config(self):
        with open(self.config_file, 'r') as f:
            return json.load(f)
        
    def get_setting(self, key):
        return self.config[key]