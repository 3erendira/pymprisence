import os

def createDirs():
    os.makedirs(os.path.join(os.path.expanduser("~"), ".pymprisence/logs/"), exist_ok=True)
    os.makedirs(os.path.join(os.path.expanduser("~"), ".pymprisence/cache/"), exist_ok=True)