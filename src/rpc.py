import os
import time
from pypresence import exceptions
from pypresence.presence import Presence
import logging
import tomllib

class rpcClient:
    def __init__(self):
        with open(os.path.join(os.path.expanduser("~"), ".config/pymprisence/config.toml"), "rb") as f:
            self.cfg = tomllib.load(f)
        self.logger = logging.getLogger("pymprisence")
        self.RPC = Presence(self.cfg["discord"]["app_id"])

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

    def updateRPC(self, state, details, name, activity_type, length, position, large_image):
        self.RPC.update(
            state = state,
            details = details,
            name = name,
            activity_type = activity_type,
            start = int(time.time()) - position,
            end = int(time.time()) + int(length - position),
            large_image = large_image
        )
        self.logger.info(f"Updated RPC (state: {state}, details: {details}, name: {name})")