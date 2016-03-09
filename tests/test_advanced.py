# -*- coding: utf-8 -*-

from .context import bike_scraper as s

import unittest
from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_false


class TestSuite(unittest.TestCase):
    """Advanced test cases."""


if __name__ == '__main__':
    unittest.main()
