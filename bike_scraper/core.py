import json
import datetime
import time
import os
from urllib.request import urlopen
import sqlite3
import ast
import atexit
import calendar

class BikeScraper:
    """ The class creates an object with all the functions required to update collected data to the database """
    
    count = 0
    connection = sqlite3.connect("bikedata.db")

    def create_database(self):
        """Input: None, Output: A created database, Function: This will create a database if one did not exist"""
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
        """Input: Self, Output: Data inserted into database, Function: This function inputs 
        data from a text file into the previously created database"""
        try:
            # These will open both Data and Completed text files
            inputfile = open("Data.txt", "r")
            processeddata = open("Completed.txt", "a")
            inputfile = inputfile.read().splitlines()
            c = self.connection.cursor()
            # This will go through each line in the data.txt file
            for i in range(0, len(inputfile)):
                # This will copy it across to Completed.txt
                processeddata.write(str(inputfile[i])+"\n")
                # This checks if the line is empty (For formatting reasons)
                if inputfile[i] != "":
                    # This if/else will check if it begins with {, EG: is part of the JSON.
                    if inputfile[i][:1] != "{":
                        datetime = inputfile[i]
                    else:
                        data = ast.literal_eval(inputfile[i])
                        # self.count increases at the end of the file, so if it is modulo 0, it should be a day of running, and will update the static data
                        if self.count % 288 == 0:
                            self.count = 0
                            c.execute("INSERT OR REPLACE INTO Station_Details VALUES(?, ?, ?, ?, ?, ?, ?)",
                                    (data["number"], data["address"], data["position"]["lat"], data["position"]["lng"],
                                    data["bike_stands"], data["banking"], data["bonus"]))
                        # This increases the dynamic data
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
        """Input: Self, Output: JSON file, Function: This functions pulls data from the JCDecaux API"""
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
        """ Input: self, Output: The combined features of the above functions, Function: This function calls every 5 minutes and links together all prior functions. """
        while True:
            # Start by getting a time
            start_time = time.time()
            try:
                station_data = self.import_data()
                data = open("Data.txt", "a")
                data.write(str(datetime.datetime.now().date()) + " " + str(datetime.datetime.now().time())+"\n\n")
                # This will write data to the data.txt file
                for i in range(0, len(station_data)):
                    data.write(str(station_data[i])+"\n")
                # Finish with a new line
                data.write("\n")
                data.close()
                # At the end, we call read_data to copy data across into the database. THis can be left out to just create a text file.
                self.read_data()
            except ValueError:
                return None
            try:
                # If the time at the start minus the time taken is above 0, wait that amount of time
                time.sleep(start_time + 300 - time.time())
            except:
                # Else, wait a full 5 minutes
                time.sleep(300)
