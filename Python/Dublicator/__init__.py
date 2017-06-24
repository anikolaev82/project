import sys, os, logging
if __name__ != "__main__":

    logging.info("Запущен {0} путь к файлу {1}".format(__name__))
    sys.path.append(os.getcwd())

