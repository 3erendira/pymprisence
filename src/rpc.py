import os
import time
from dotenv import load_dotenv
from pypresence import Presence, exceptions

load_dotenv()
client_id = os.getenv("APP_ID")

class rpcClient:
    def __init__(self, RPC = Presence(client_id)):
        self.RPC = RPC

    def waitForDiscord(self):
        print("Waiting for discord like a good boy")
        time.sleep(15)
        self.connectToRPC()

    def connectToRPC(self):
        try:
            self.RPC.connect()
            print("Connected to discord succesfully")
        except exceptions.DiscordNotFound:
            self.waitForDiscord()

    def updateRPC(self, state, details, name):
        self.RPC.update(
            state = state,
            details = details,
            name = name
        )
        print(f"Updated RPC (state: {state}, details: {details}, name: {name})")