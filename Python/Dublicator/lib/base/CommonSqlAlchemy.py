#!/usr/bin/env python
# coding: utf8
# author: anikolaev82
from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy.orm import Mapper, sessionmaker
import logging


class CommonSqlAlchemy:
    """Общий класс для работы с SQLAlchemy"""
    _engine = None
    _metadata = None
    _connect = None
    _transaction = None
    _session = None

    def create_scheme(self, **kwargs):
        """Создание схемы базы данных"""
        logging.info(__doc__)
        self._metadata = MetaData(**kwargs)

    def create_engine(self, p_connect_db, p_debug=False):
        """Создание соединения и связывание соединения с сессией"""
        logging.info(__doc__)
        self._engine = create_engine(p_connect_db, echo=p_debug)
        session = sessionmaker(bind=self._engine)
        self._session = session()

    def get_connect(self):
        """Возвращаем созданное соединение"""
        logging.info(__doc__)
        if self._connect is None:
            logging.info("Соединение не создано, создаем")
            self._connect = self._engine.connect()
        return self._connect

    def start_transaction(self):
        logging.info("Начинаем транзакцию")
        if self._connect is None:
            logging.info("Соединение не создано, создаем")
            self.get_connect()
        self._transaction = self._connect.begin()
        return self._transaction

    def commit(self):
        logging.info("Производим commit")
        if self._transaction is not None:
            self._transaction.commit()
            self._session.commit()
            self._transaction = None
        else:
            logging.error("Производим commit")

    def create_tables_ddl(self, p_list_ddl):
        logging.info("Создаем таблицы через Data Definition Language")
        try:
            for ddl in p_list_ddl:
                logging.debug("Выполняем команду {0}".format(ddl))
                self._engine.execute(ddl)
        except Exception as e:
            logging.error("Произошла ошибка {0}, проверьте выполняемый код {1}".format(e, p_list_ddl))

    def get_list_tables(self):
        logging.info("Возвращаем список объектов схемы")
        inspector = inspect(self._engine)
        return inspector.get_table_names()

    def drop_tables(self, p_tables_names):
        logging.info("Удаляем таблицы через Drop table")
        try:
            for table in p_tables_names:
                self._engine.execute("DROP TABLE IF EXISTS {0}".format(table))
        except Exception as e:
            logging.error("Произошла ошибка {0}, проверьте выполняемый код {1}".format(e, p_tables_names))

    def add(self, p_object):
        logging.info("Добавляем объект в сессию")
        if self._transaction is None:
            self.start_transaction()
        self._session.add(p_object)

    def mapping_exists_table(self, p_class, p_table):
        logging.info("Отображаем таблицу {0} на класс".format(p_table))
        Mapper(p_class, self._metadata.tables[p_table])
        return p_class
