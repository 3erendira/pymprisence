import tomllib
import os

class Config:
    def __init__(self):
        self.path = os.path.join(os.path.expanduser("~"), ".config/pymprisence/config.toml")

    def get_config(self):
        with open(self.path, "rb") as f:
            data = tomllib.load(f)

        return data