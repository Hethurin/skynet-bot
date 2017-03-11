import unittest
import constants as const
from config import SkynetConfig

class SkynetConfigTestCase(unittest.TestCase):

    def test_reading_text_level_information(self):
        conf = SkynetConfig()
        conf.read_config('testconfig.ini')

        expected_data = ('text', 'question0', 'answer0', '0')
        lvl_data = conf.get_level_info('level0')

        self.assertTupleEqual(expected_data, lvl_data)

    def test_reading_image_level_information(self):
        conf = SkynetConfig()
        conf.read_config('testconfig.ini')

        expected_data = ('image', 'question2', 'answer2', '2', 'question2.jpg')
        lvl_data = conf.get_level_info('level1')

        self.assertTupleEqual(expected_data, lvl_data)

    def test_getting_question_with_multiple_correct_answers(self):
        conf = SkynetConfig()
        conf.read_config('testconfig.ini')

        lvl_data = conf.get_level_info('level1')
        expected_answers = 'answer1 answer18'

        self.assertEqual(lvl_data[const.qenum.answers], expected_answers)

if __name__ == '__main__':
    unittest.main()


