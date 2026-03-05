import requests
import logging
from diskcache import Cache
from urllib.parse import urlparse
import tomllib
import os
import xxhash

class coverCacheHandler:
    def __init__(self):
        self.logger = logging.getLogger("pymprisence")
        with open(os.path.join(os.path.expanduser("~"), ".config/pymprisence/config.toml"), "rb") as f:
            self.cfg = tomllib.load(f)
        self.cache = Cache(os.path.join(os.path.expanduser("~"), ".pymprisence/cache/"))

        self.catbox_api = "https://catbox.moe/user/api.php"

    def fetchCover(self, path):
        if path is None:
            self.logger.info("Cover path was none. Skipping uploading and caching")
            return
        parsed_path = urlparse(path).path
        hash = self.hashImage(parsed_path)
        url = self.getCoverFromCache(hash)

        if url is None:
            self.logger.info("Cover URL was not found in the cache. Uploading and caching now.")
            url = self.uploadImage(parsed_path)
            self.cacheImage(hash, url)
            return url
        else:
            self.logger.info("Cover URL found in the cache.")
            return url

    def cacheImage(self, hash, url):
        if self.cfg["cover"]["provider"]["catbox"]["litterbox"] is True:
            expire_sec = self.cfg["cover"]["provider"]["catbox"]["litter_duration"] * 3600
        else:
            expire_sec = None

        with Cache(self.cache.directory) as reference:
            reference.set(hash, url, expire = expire_sec)

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
            self.logger.info("Uploaded cover to catbox.")
            return response.text.strip()
        else:
            return False

    def getCoverFromCache(self, hash):
        url = self.cache.get(hash)
        return url