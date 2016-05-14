import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import bl

class Test(unittest.TestCase):
    def test_accessible(self):
        bl.get_matched_station_list
        bl.get_
        """ API not determined """


#unittest.main()
print(dir(bl))
