import logging
from pathlib import Path


class Logger(object):
    def __init__(self, name, level=logging.DEBUG):
        self._logger = logging.getLogger(name)
        self._logger.setLevel(level)

        fh = logging.FileHandler(f"%s.log" % name, "w")
        self.logger.addHandler(fh)

        sh = logging.StreamHandler()
        self.logger.addHandler(sh)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)
