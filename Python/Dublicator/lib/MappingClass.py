import os
import logging
import lib.ExecHash


class Tree(object):

    def __init__(self, p_full_path):
        self.path, self.name = os.path.split(p_full_path)
        self.size = os.path.getsize(p_full_path)

    def exec_hash(self):
        logging.info("start exe_hash size = {0}".format(self.size))
        if self.size < 10000000:
            self.hash = lib.ExecHash.ExecHash.get_hash(self.full_name())
            logging.info("stop exe_hash = {0}".format(self.hash))
        return self.hash is not None

    def full_name(self):
        return os.path.join(self.path, self.name)
