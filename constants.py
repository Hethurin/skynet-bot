from collections import namedtuple

QuestionMetadata = namedtuple('QuestionMetadata','type, question, answers, code path')
QuestionTypes = namedtuple('QuestionTypes', 'text image')
qmeta = QuestionMetadata("type", "question", "answers", "code", "path")
qenum = QuestionMetadata(0, 1, 2, 3, 4)
qtypes = QuestionTypes("text", "image")

lvl_mapping = {'level0': 0, 'level1': 1, 'level2': 2,
               'level3': 3, 'level4': 4, 'level5': 5,
               'level6': 6, 'level7': 7, 'level8': 8}

config_path = "config.ini"

