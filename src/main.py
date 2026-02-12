from rpc import rpcClient
import time

def main():
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
    main()