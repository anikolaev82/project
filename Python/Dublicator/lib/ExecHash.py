import os.path
import hashlib
import logging


class ExecHash:

    @staticmethod
    def get_hash(p_path):
        md5 = hashlib.md5()
        logging.info("get_hash path = {0}".format(p_path))
        if os.path.isfile(p_path):
            with open(p_path, "rb") as fd:
                logging.info("get_hash read_file = {0}".format(p_path))
                md5.update(fd.read())
                h = md5.digest()
                logging.info("get_hash return = {0}".format(h))
                return h
