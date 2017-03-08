from collections import namedtuple

QuestionMetadata = namedtuple('QuestionMetadata','type, question, answers, code')
qmeta = QuestionMetadata("type", "question", "answers", "code")
qenum = QuestionsMetadata(0, 1, 2, 3)

config_path = "config.ini"
