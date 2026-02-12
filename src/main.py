from rpc import rpcClient
import time
import os
from logger import Logger

def main():
    os.makedirs(os.path.join(os.path.expanduser("~"), ".pymprisence/logs/"), exist_ok=True)

    RPC = rpcClient()
    RPC.connectToRPC()
    while True:
        RPC.updateRPC(
            state = "test_state",
            details = "test_details",
            name = "test_name"
        )
        time.sleep(5)

if __name__ == "__main__":
    logger = Logger().get()
    main()