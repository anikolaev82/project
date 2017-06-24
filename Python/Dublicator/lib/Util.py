import logging
import os
import argparse


class Util:

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
        arg_parse.add_argument('-a', '--action', default='save')  # Сохранять, удалять, показать дубликаты
        return arg_parse

