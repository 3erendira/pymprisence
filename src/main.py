from rpc import rpcClient
from pypresence.types import ActivityType
from logger import Logger
from mpris import MPRIS
import time
import os

def main():
    os.makedirs(os.path.join(os.path.expanduser("~"), ".pymprisence/logs/"), exist_ok=True)
    Logger().get()
    conn = MPRIS()

    metadata = conn.get_metadata()
    position = conn.get_position()

    RPC = rpcClient()
    RPC.connectToRPC()
    while True:
        RPC.updateRPC(
            details = metadata["xesam:title"][1],
            state = ', '.join(metadata["xesam:artist"][1]),
            name = "music",
            activity_type = ActivityType.LISTENING,
            length = metadata["mpris:length"][1] / 1000000,
            position = position / 1000000
        )
        time.sleep(5)

if __name__ == "__main__":
    main()