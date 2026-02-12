import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
from typing import Optional, TextIO

class Logger:
    def __init__(
            self,
            name = "pymprisence",
            logpath = os.path.join(os.path.expanduser("~"), ".pymprisence/logs/"),
            logfile = f"{datetime.now().strftime("%H-%M-%d-%m-%Y")}.log",
            *,
            file_level: int = logging.DEBUG,
            console_level: int = logging.INFO,
            max_filesize: int = 64 * 1024,
            backup_count: int = 5,
            stream: Optional[TextIO] = None,
            date_format: str = "%d-%m-%Y %H:%M:%S"
    ):
        self.name = name
        self.logpath = logpath
        self.logfile = logfile
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(min(file_level, console_level))

        if any(isinstance(handler, (RotatingFileHandler, logging.StreamHandler)) for handler in self.logger.handlers):
            return
        
        fmt = logging.Formatter("[{asctime}] [{levelname}] {name}: {message}", date_format, style="{")

        file_handler = RotatingFileHandler(os.path.join(logpath, logfile), encoding="utf-8", maxBytes=max_filesize, backupCount=backup_count)
        file_handler.setFormatter(fmt)
        file_handler.setLevel(file_level)
        self.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler(stream)
        console_handler.setFormatter(fmt)
        console_handler.setLevel(console_level)
        self.logger.addHandler(console_handler)

    def get(self):
        return self.logger