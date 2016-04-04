import json
import datetime
import time
import os
from urllib.request import urlopen
import sqlite3
import ast
import atexit

__author__ = 'devin'


class BikeScraper:

    count = 0
    connection = sqlite3.connect("bikedata.db")

    def create_database(self):
        try:
            c = self.connection.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS Station_Details(Station_Number INT PRIMARY KEY,
                    Station_Name CHAR(50), latitude REAL, longitude REAL, Total_Spaces INT,
                    Banking BOOLEAN, Bonus BOOLEAN)''')
            c.execute('''CREATE TABLE IF NOT EXISTS Station_Data(Time_Stamp CHAR(50), Station_Number INT,
                    Last_Updated INT, Available_Bike_Stands INT, Bikes_Available INT, Status BOOLEAN, PRIMARY KEY(Time_Stamp, Station_Number))''')
            self.connection.commit()
            c.close()
        except ConnectionError:
            return None

    def read_data(self):
        try:
            inputfile = open("Data.txt", "r")
            processeddata = open("Completed.txt", "a")
            inputfile = inputfile.read().splitlines()
            c = self.connection.cursor()
            for i in range(0, len(inputfile)):
                processeddata.write(str(inputfile[i])+"\n")
                if inputfile[i] != "":
                    if inputfile[i][:1] != "{":
                        datetime = inputfile[i]
                    else:
                        data = ast.literal_eval(inputfile[i])
                        if self.count % 288 == 0:
                            self.count = 0
                            c.execute("INSERT OR REPLACE INTO Station_Details VALUES(?, ?, ?, ?, ?, ?, ?)",
                                    (data["number"], data["address"], data["position"]["lat"], data["position"]["lng"],
                                    data["bike_stands"], data["banking"], data["bonus"]))
                        c.execute("INSERT INTO Station_Data VALUES(?, ?, ?, ?, ?, ?)",
                                    (datetime ,data["number"],data["last_update"],
                                    data["available_bike_stands"], data["available_bikes"], data["status"]))
                        self.connection.commit()
            c.close()
            self.count += 1
            os.remove("Data.txt")
            processeddata.close()
        except FileNotFoundError:
            return None
        except ConnectionError:
            return None

    def import_data(self):

        try:
            API = "https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=ecb685c01e04147581cfd3c43376765a5ca1098f"
            url = urlopen(API).read()
            result = url.decode("utf-8")
            station_data = json.loads(result)
        except ConnectionError:
            print("-Unexpected Failure-")
            return None
        return station_data

    def collect_data(self):
        while True:
            start_time = time.time()
            try:
                station_data = self.import_data()
                data = open("Data.txt", "a")
                data.write(str(datetime.datetime.now().date()) + " " + str(datetime.datetime.now().time())+"\n\n")
                for i in range(0, len(station_data)):
                    data.write(str(station_data[i])+"\n")
                data.write("\n")
                data.close()
                self.read_data()
            except ValueError:
                return None
            try:
                time.sleep(start_time + 300 - time.time())
            except:
                time.sleep(300)
