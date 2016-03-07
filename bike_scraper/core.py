import json
import threading
import datetime
from urllib.request import urlopen


def import_data():
    try:
        API = "https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=ecb685c01e04147581cfd3c43376765a5ca1098f"
        url = urlopen(API).read()
        result = url.decode("utf-8")
        station_data = json.loads(result)
    except ConnectionError:
        print("-Unexpected Failure-")
        return None
    return station_data


def collect_data():
    threading.Timer(300.0, collect_data).start()
    station_data = import_data()
    data = open("Data.txt", "a")
    data.write(str(datetime.datetime.now().date()) + " " + str(datetime.datetime.now().time())+"\n\n")
    for i in range(0, len(station_data)):
        data.write(str(station_data[i])+"\n")
    data.write("\n")
    data.close()
