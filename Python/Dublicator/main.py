#!/usr/bin/env python
# coding: utf8
# create project Сб апр 29 21:40:07 EET 2017 by user anikolaev82
from lib.CustomSqlAlchemy import CustomSqlAlchemy
from lib.Util import Util
from lib.MappingClass import Tree
import logging
from multiprocessing import Queue, Pool
import time
import sys


def thread(p_obj):
    obj = uTree(p_obj)
    obj.exec_hash()
    conn_db.add(obj)
    conn_db.commit()


if __name__ == "__main__":

    parse = Util.create_parser()
    param = parse.parse_args(sys.argv[1:])

    queue = Queue()
    start_time = time.time()
    logging.basicConfig(level=logging.INFO)
                        #format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                        #filename="dublicator.log")
    logging.info("Запущен {0}".format(__name__))

    conn_db = CustomSqlAlchemy()

    conn_db.start_transaction()
    logging.info(conn_db.get_list_tables())

    uTree = conn_db.mapping_exists_table(Tree, 'tree')

    pool = Pool()
    list_file = Util.recursion(p_path=param.source)
    logging.info(list_file)
    pool.map(thread, list_file)
    pool.close()
    pool.join()
    end_time = time.time()
    logging.info("the end time = {0}".format(end_time - start_time))

    logging.debug(param.action)
    if param.action == 'move':
        Util.move(conn_db)
    elif param.action == 'delete':
        Util.delete(conn_db)
    elif param.action == 'show':
        Util.show(conn_db)
