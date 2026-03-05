from rpc import rpcClient
from pypresence.types import ActivityType
from logger import Logger
from mpris import MPRIS
from cover import coverCacheHandler
from urllib.parse import urlparse
import time
import tomllib
import os

def main():
    os.makedirs(os.path.join(os.path.expanduser("~"), ".pymprisence/logs/"), exist_ok=True)
    os.makedirs(os.path.join(os.path.expanduser("~"), ".pymprisence/cache/"), exist_ok=True)
    Logger().get()
    conn = MPRIS()
    cover = coverCacheHandler()

    with open(os.path.join(os.path.expanduser("~"), ".config/pymprisence/config.toml"), "rb") as f:
        cfg = tomllib.load(f)

    RPC = rpcClient()
    RPC.connectToRPC()
    while True:
        metadata = conn.getMetadata()
        position = conn.getPosition()

        RPC.updateRPC(
            details = metadata["xesam:title"][1],
            state = ', '.join(metadata["xesam:artist"][1]),
            name = cfg["presence"]["name"],
            activity_type = ActivityType.LISTENING,
            length = metadata["mpris:length"][1] / 1000000,
            position = position / 1000000,
            large_image = cover.uploadImage(urlparse(metadata["mpris:artUrl"][1]).path)
        )
        time.sleep(5)

if __name__ == "__main__":
    main()