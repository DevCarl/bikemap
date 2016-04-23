# -*- coding: utf-8 -*-

from .context import bike_scraper as b

import unittest


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_absolute_truth_and_meaning(self):
        """ This is a test to make sure the tests are working as expected """
        assert True

if __name__ == '__main__':
    unittest.main()
