import sys
import os

sys.path.insert(0, os.path.abspath('..'))
import bike_scraper
from bike_scraper.core import BikeScraper


if __name__ == '__main__':
    name = BikeScraper()
    name.create_database()
    name.collect_data()




