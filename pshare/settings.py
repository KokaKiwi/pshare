import os
import json
from . import utils

SETTINGS_FILENAME = 'settings.json'
DEFAULT_SETTINGS = {
    'debug': True,

    'host': '127.0.0.1',
    'port': 5000,

    'site_name': 'P\'Share',

    'database_filename': 'pshare.db',

    'private_id_length': 16,
    'public_id_length': 8,
    'password_length': 8
}

class Settings:
    settings = DEFAULT_SETTINGS.copy()

    def __init__(self):
        if os.path.exists(SETTINGS_FILENAME):
            self.load(SETTINGS_FILENAME)

        if not self.secret:
            self.gen_secret()

        self.save(SETTINGS_FILENAME)

    def load(self, filename):
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                self.settings.update(json.loads(f.read()))

    def save(self, filename):
        with open(filename, 'w+') as f:
            f.write(json.dumps(self.settings, sort_keys = True, indent = 4, separators = (',', ': ')))

    def gen_secret(self):
        self.secret = utils.random.generate_secure(length = 32)

    def __getattr__(self, name):
        return self.settings.get(name, None)

    def __setattr__(self, name, value):
        self.settings[name] = value

    def __delattr__(self, name):
        del self.settings[name]

settings = Settings()
