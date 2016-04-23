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
        """ This function will setup an empty database with columns, but no rows"""
        self.connection = sqlite3.connect("bikedata.db")
        self.count = 0
        b.BikeScraper.create_database(self)

    def test_createdatabase(self):
        """ This will test if the command to create the database works by looking for the empty database """
        assert(os.path.isfile("bikedata.db"))

    def test_Station_Data_Empty(self):
        """ This will assert that there is no data within the database """
        c = self.connection.cursor()
        c.execute('SELECT Station_Number FROM Station_Data')
        test = c.fetchone()
        c.close()
        assert(test == None)

    def test_import_data(self):
        """ This will test if the import data function for getting info from the API is working """
        assert_false(b.BikeScraper.import_data(self) == None)

class TestSuite2(unittest.TestCase):

    def setUp(self):
        """ This will set up a database and actually read data into it """
        self.connection = sqlite3.connect("bikedata.db")
        self.count = 0
        b.BikeScraper.create_database(self)
        b.BikeScraper.read_data(self)

    def test_data_read(self):
        """ This test will see if the reading into the database worked """
        c = self.connection.cursor()
        c.execute("Select Station_Number FROM Station_Data WHERE Station_Number = 88")
        test = c.fetchone()[0]
        c.close()
        assert(test == 88)

    def tearDown(self):
        """ This final tear down will remove the new database created, and rename Data.txt to Completed.txt """
        os.remove("bikedata.db")
        os.rename("Completed.txt", "Data.txt")


if __name__ == '__main__':
    unittest.main()
