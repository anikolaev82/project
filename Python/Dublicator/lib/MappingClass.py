import os
import logging
import lib.ExecHash
from lib.CustomConfigParser import CustomConfigParser


class Tree(object):

    def __init__(self, p_full_path):
        self.path, self.name = os.path.split(p_full_path)
        self.size = os.path.getsize(p_full_path)
        self.max_file_size = CustomConfigParser().get_max_file_size()

    def exec_hash(self):
        logging.info("start exe_hash size = {0}".format(self.size))
        max_size = self.max_file_size
        if self.size < max_size or max_size <= 0:
            self.hash = lib.ExecHash.ExecHash.get_hash(self.full_name())
            logging.info("stop exe_hash = {0}".format(self.hash))
        return self.hash is not None

    def full_name(self):
        return os.path.join(self.path, self.name)
