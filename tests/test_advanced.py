# -*- coding: utf-8 -*-

from .context import bike_scraper as b

import unittest
import os
import sqlite3
from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_false


class TestSuite(unittest.TestCase):
    """Advanced test cases. This will set up a test database and run a few tests
    based upon the actual commands we will use"""

    def setUp(self):
        self.connection = sqlite3.connect("bikedata.db")
        self.count = 0
        b.BikeScraper.create_database(self)

    def test_createdatabase(self):
        # This will test if the command to create the database works
        assert(os.path.isfile("bikedata.db"))

    def test_Station_Data_Empty(self):
        c = self.connection.cursor()
        c.execute('SELECT Station_Number FROM Station_Data')
        test = c.fetchone()
        c.close()
        assert(test == None)

    def test_Station_Details_Empty(self):
        c = self.connection.cursor()
        c.execute('SELECT Station_Number FROM Station_Details')
        test = c.fetchone()
        c.close()
        assert(test == None)

    def test_import_data(self):
        assert_false(b.BikeScraper.import_data(self) == None)

class TestSuite2(unittest.TestCase):

    def setUp(self):
        self.connection = sqlite3.connect("bikedata.db")
        self.count = 0
        b.BikeScraper.create_database(self)
        b.BikeScraper.read_data(self)

    def test_data_read(self):
        c = self.connection.cursor()
        c.execute("Select Station_Number FROM Station_Data WHERE Station_Number = 88")
        test = c.fetchone()[0]
        c.close()
        assert(test == 88)

    def tearDown(self):
        os.remove("bikedata.db")
        os.rename("Completed.txt", "Data.txt")


if __name__ == '__main__':
    unittest.main()
