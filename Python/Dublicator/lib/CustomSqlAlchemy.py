#!/usr/bin/env python
# coding: utf8
# author: anikolaev82
from lib.base.CommonSqlAlchemy import CommonSqlAlchemy
from lib.CustomConfigParser import CustomConfigParser
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, ForeignKey


class CustomSqlAlchemy(CommonSqlAlchemy):
    _config = None
    _Base = declarative_base()

    def __init__(self):
        self._config = CustomConfigParser()
        self.create_engine(self._config.get_engine_db(), False)
        self.create_scheme(bind=True)
        self._metadata.reflect(self._engine)

    def preparing_db(self):
        self.drop_tables(self.get_list_tables())
        tbl_tree_dir = Table(
                            "tree",
                            self._metadata,
                            Column("id", Integer, primary_key=True),
                            Column("path", String, nullable=False),
                            Column("name", String, nullable=False),
                            Column("size", String, nullable=False),
                            Column("hash", String,  nullable=True)#,
                            #Column("property", Integer, ForeignKey('prop_file.id'))
                        )
        self._metadata.create_all(self._engine)
