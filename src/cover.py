import requests
from diskcache import Cache
from urllib.parse import urlparse
import tomllib
import os
import xxhash

class coverCacheHandler:
    def __init__(self):
        with open(os.path.join(os.path.expanduser("~"), ".config/pymprisence/config.toml"), "rb") as f:
            self.cfg = tomllib.load(f)
        self.cache = Cache(os.path.join(os.path.expanduser("~"), ".pymprisence/cache/"))

        self.catbox_api = "https://catbox.moe/user/api.php"

    def cacheCover(self, path):
        parsed_path = urlparse(path).path
        hash = self.hashImage(parsed_path)
        url = self.uploadImage(parsed_path)

        with Cache(self.cache.directory) as reference:
            reference.set(hash, url)

    def hashImage(self, path):
        algo = xxhash.xxh64()

        with open(path, "rb") as f:
            data = f.read()
            algo.update(data)

        return algo.hexdigest()
    
    def uploadImage(self, path):
        data = {
            "reqtype": "fileupload"
        }

        with open(path, "rb") as f:
            files = { "fileToUpload": f }
            response = requests.post(self.catbox_api, data=data, files=files)

        if response.status_code == 200:
            return response.text.strip()
        else:
            return False

    def getCoverFromCache(self):
        pass