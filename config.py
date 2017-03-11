from configparser import ConfigParser
import constants as const
import sys


class SkynetConfig:

    def __init__(self):
        self.__parser = ConfigParser()

    def read_config(self, config_path):
        self.__parser.read(config_path)
    
    def get_level_info(self, level):
        question_type = self.__get_string(level, const.qmeta.type)
        question = self.__get_string(level, const.qmeta.question)
        answers = self.__get_string(level, const.qmeta.answers)
        code = self.__get_string(level, const.qmeta.code)

        if question_type not const.qtypes.text:
            path = self.__get_string(level, const.qmeta.path)
            return (question_type, question, answers, code, path)

        return (question_type, question, answers, code)
    
    def __get_items(self, section):
        value = None

        try:
            value = self.__parser.items(section)
        except:
            print("[E] Exception on {}".format(parameter))

        return value
    
    def __get_string(self, section, parameter):
        value = None

        try:
            value = self.__parser.get(section, parameter)
        except:
            print("[E] Exception on {}".format(parameter), sys.exc_info()[0])

        return value

    def __get_bool(self, section, parameter):
        value = None

        try:
            value = self.__parser.getboolean(section, parameter)
        except:
            print("[E] Exception on {}".format(parameter))

        return value
