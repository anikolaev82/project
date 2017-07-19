#!/usr/bin/env python
# coding: utf8
# author: anikolaev82
import os
from configparser import ConfigParser, ParsingError
import logging


class CommonConfigParser:
    """Базовый класс для чтения записи файла настроек"""
    # Классовые переменные, доступны всем экземплярам
    _config = None
    _config_name = "etc/settings.config"
    _config_file = None

    def __init__(self, settings_config=None):
        if settings_config is not None:
            if os.path.exists(settings_config):
                self._config_name = settings_config
            else:
                raise FileNotFoundError
        self._config = ConfigParser()

        try:
            self._config.read(self._config_name)
        except OSError:
            logging.error("Файл {0} не найден".format(self._config_name))
            raise OSError
        except ParsingError:
            print("Файл настроек {0} содержит ошибки".format(self._config_name))
            raise ParsingError()

    def get_param(self, p_section, p_elem):
        p_section = p_section.upper()
        p_elem = p_elem.upper()
        try:
            return self._config.get(p_section, p_elem)
        except Exception:
            logging.error("Секции {0} с настройкой {1} не найдено".format(p_section, p_elem))

    def _safe_config(self):
        try:
            self._config_file = open(self._config_name, "w")
            self._config.write(self._config_file)
            self._config_file.flush()
            self._config_file.close()
        except OSError:
            logging.error("Ошибка записи файла {0}".format(self._config_name))

    def set_param(self, p_section, p_elem, p_value):
        p_section = p_section.upper()
        p_elem = p_elem.upper()
        if p_section not in [sect.upper() for sect in self._config.sections()]:
            self._config.add_section(p_section)
        self._config.set(p_section, p_elem, p_value)
        self._safe_config()

    def __repr__(self):
        return "Файл настроек {0} секции файла настроек {1}".format(self._config_name, self._config.sections())
