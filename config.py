from configparser import SafeConfigParser
import constants as const


class SkynetConfig:

    def __init__(self):
        self.__parser = SafeConfigParser()

    def read_config(self, config_path):
        self.__parser.read(config_path)
    
    def get_question_info(self, question):
        question_type = self.__get_string(question, const.qmeta.type)
        question = self.__get_string(question, const.qmeta.question)
        answers = self.__get_string(question, const.qmeta.answers)
        code = self.__get_string(questin, const.qmeta.code)

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
            print("[E] Exception on {}".format(parameter))

        return value

    def __get_bool(self, section, parameter):
        value = None

        try:
            value = self.__parser.getboolean(section, parameter)
        except:
            print("[E] Exception on {}".format(parameter))

        return value
