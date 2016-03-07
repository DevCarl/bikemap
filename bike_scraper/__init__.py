import sys
import os

sys.path.insert(0, os.path.abspath('..'))
import bike_scraper
from bike_scraper.core import collect_data


if __name__ == '__main__':
    collect_data()




