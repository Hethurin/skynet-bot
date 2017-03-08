import unittest
import constants as const
from config import SkynetConfig

class SkynetConfigTestCase(unittest.TestCase):

    def test_reading_level_information(self):
        conf = SkynetConfig()
        conf.read_config('testconfig.ini')

        expected_data = ('text', 'question0', 'answer0', '0')
        lvl_data = conf.get_level_info('level0')

        self.assertTupleEqual(expected_data, lvl_data)

if __name__ == '__main__':
    unittest.main()


