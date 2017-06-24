#!/usr/bin/env python
# coding: utf8
# author: anikolaev82
from lib.base.CommonConfigParser import CommonConfigParser


class CustomConfigParser(CommonConfigParser):
    def get_engine_db(self):
        return self.get_param("database", "connection_string")