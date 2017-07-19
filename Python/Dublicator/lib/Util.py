import logging
import os
import argparse
import os.path
from shutil import move
from lib.CustomConfigParser import CustomConfigParser


class Util:

    @staticmethod
    def get_config():
        return CustomConfigParser()

    def __getattr__(self, item):
        print('Метода {0} не существует'.format(item))

    @staticmethod
    def recursion(p_path, ls=[]):
        logging.info("recursion path = {0}".format(p_path))
        for l_iter in os.listdir(p_path):
            full_path = os.path.join(p_path, l_iter)
            if os.path.isdir(full_path):
                Util.recursion(full_path, ls)
            logging.info("recursion full_path = {0}".format(full_path))
            ls.append(full_path)
            logging.info("recursion ls.size = {0}".format(len(ls)))
        return ls

    @staticmethod
    def create_parser():
        arg_parse = argparse.ArgumentParser()
        arg_parse.add_argument('-s', '--source')  # Путь для поиска дубликатов
        arg_parse.add_argument('-v', '--verbose', default=False)  # Нужно ли выводить лог
        arg_parse.add_argument('-a', '--action', default='save')  # Переместить, удалить, показать дубликаты
        return arg_parse

    @staticmethod
    def _get_path(p_struct):
        return os.path.join(p_struct.path, p_struct.name)

    @staticmethod
    def _get_list_dubl(p_conn):
        l_table = p_conn.get_view_dublicate()
        l_list = {}
        for l_iter in p_conn._session.query(l_table):
            if l_iter.hash in l_list.keys():
                l_list[l_iter.hash].add(Util._get_path(l_iter))
            else:
                l_ls = set()
                l_ls.add(Util._get_path(l_iter))
                l_list.setdefault(l_iter.hash, l_ls)
        return l_list

    @staticmethod
    def move(p_conn):
        l_list = Util._get_list_dubl(p_conn)
        l_dest = Util.get_config().get_path_arc()
        logging.debug("Путь для архива {0}".format(l_dest))
        if not os.path.isdir(l_dest):
            os.mkdir(l_dest)
            logging.debug("Создаем путь для архива {0}".format(l_dest))
        for l_key, l_ls in l_list.items():
            for l_elem in list(l_ls)[1:]:
                logging.debug("{1} Путь для перемещения {0}".format(l_elem, l_key))
                if os.path.isfile(l_elem):
                    logging.debug("src {0} dest {1}".format(l_elem, l_dest))
                    logging.debug("dest {0}".format(os.path.join(l_dest, os.path.split(l_elem)[1])))
                    if os.path.isfile(os.path.join(l_dest, os.path.split(l_elem)[1])):
                        os.remove(l_dest)
                    move(l_elem, l_dest)

    @staticmethod
    def delete(p_conn):
        l_list = Util._get_list_dubl(p_conn)
        for l_key, l_ls in l_list.items():
            for l_elem in list(l_ls)[1:]:
                logging.info("{1} Путь для перемещения {0}".format(l_elem, l_key))
                if os.path.isfile(l_elem):
                    os.remove(l_elem)

    @staticmethod
    def show(p_conn):
        l_list = Util._get_list_dubl(p_conn)
        logging.debug('Найдено всего {0} дубликатов'.format(len(l_list)))
        for l_key, l_val in l_list.items():
            print('Hash {0} файлов {1} имя {2}'.format(l_key, len(l_val), l_val))



