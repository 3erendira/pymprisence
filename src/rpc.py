import os
import time
from dotenv import load_dotenv
from pypresence import Presence, exceptions
import logging

load_dotenv()
client_id = os.getenv("APP_ID")

class rpcClient:
    def __init__(self, RPC = Presence(client_id)):
        self.logger = logging.getLogger("pymprisence")
        self.RPC = RPC

    def waitForDiscord(self):
        self.logger.info("Waiting for discord like a good boy")
        time.sleep(15)
        self.connectToRPC()

    def connectToRPC(self):
        try:
            self.RPC.connect()
            self.logger.info("Connected to discord succesfully")
        except exceptions.DiscordNotFound:
            self.waitForDiscord()

    def updateRPC(self, state, details, name):
        self.RPC.update(
            state = state,
            details = details,
            name = name
        )
        self.logger.info(f"Updated RPC (state: {state}, details: {details}, name: {name})")