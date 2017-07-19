#!/usr/bin/env python
# coding: utf8
# author: anikolaev82
from lib.base.CommonConfigParser import CommonConfigParser


class CustomConfigParser(CommonConfigParser):

    def get_engine_db(self):
        return self.get_param("database", "connection_string")

    def get_path_arc(self):
        return self.get_param("backup", "path")

    def get_max_file_size(self):
        try:
            return int(self.get_param("other", "MAX_SIZE_FILE"))
        except TypeError:
            return 0