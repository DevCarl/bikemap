import json
import datetime
import time
import os
from urllib.request import urlopen
import sqlite3
import ast
import atexit
import calendar

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

    def archive_data_now(self):
        try:
            c = self.connection.cursor()
            string = time.strftime("%Y-%m-%d %H:%M")
            minute = int(string[-2].replace(":", ""))
            count = int(minute)
            while count > minute-5:
                try:
                    string = string[0:-1] + "0"*(count < 10) + str(count)
                    row_search = c.execute("SELECT * FROM Station_Data WHERE instr(Time_Stamp, ?) > 0", [string])
                    for row in row_search:
                        print(row)
                    break
                except:
                    if count - 1 < 0:
                        count = count + 60
                        minute = minute + 60
                    count -= 1
            self.connection.commit()
            c.close()
        except ConnectionError:
            return None

    def archive_data_average(self):
        try:
            c = self.connection.cursor()
            monthrange = calendar.monthrange(datetime.datetime.now().year, datetime.datetime.now().month-1)[1]
            year, month, day, hour = datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day, datetime.datetime.now().hour
            countday = day
            while countday > day-14:
                daystring = str(year) + "-" + "0"*(month < 10) + str(month) + "-" + "0"*(countday < 10) + str(countday)
                day_search = c.execute("SELECT Time_Stamp, Station_Number, avg(Bikes_Available) FROM Station_Data WHERE instr(Time_Stamp, ?) > 0 GROUP BY Station_Number", [daystring])
                for row in day_search:
                    print(row)
                while hour >= 0:
                    try:
                        hourstring = str(year) + "-" + "0"*(month < 10) + str(month) + "-" + "0"*(countday < 10) + str(countday) + " " + "0"*(hour < 10) + str(hour)
                        hour_search = c.execute("SELECT Time_Stamp, Station_Number, avg(Bikes_Available) FROM Station_Data WHERE instr(Time_Stamp, ?) > 0 GROUP BY Station_Number", [hourstring])
                        for row in hour_search:
                            print(row)
                    except:
                        "NO RESULTS"
                    hour = hour-1
                hour = 24
                if countday - 1 < 1:
                    countday = countday + monthrange
                    day = day + monthrange
                    if month - 1 < 1:
                        month = month + 12
                        year -= 1
                    month = month-1
                countday = countday-1
            self.connection.commit()
            c.close()
        except ConnectionError:
            return None

    def calculate_freetime(self):
        c = self.connection.cursor()
        timeframe = time.time() - 14*24*60*60*1000
        c.execute("SELECT COUNT(Station_Number) FROM Station_Details")
        station_range = c.fetchone()[0]
        for row in range(0, station_range+1):
            misscount, totalmisscount, totalemptyblocks = 0, 0, 0
            time_search = c.execute("SELECT * FROM Station_Data WHERE Last_Updated > ? AND Station_Number = ?", (timeframe, row))
            for row2 in time_search:
                if row2[4] == 0:
                    misscount += 1
                elif row2[4] != 0 and misscount > 0:
                    totalmisscount += misscount
                    misscount = 0
                    totalemptyblocks += 1
            if misscount > 0:
                totalmisscount += misscount
                totalemptyblocks += 1
            maximumaveragewaitingtime = (totalmisscount/totalemptyblocks)*5 if totalemptyblocks > 0 else 0
            print(maximumaveragewaitingtime)

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
