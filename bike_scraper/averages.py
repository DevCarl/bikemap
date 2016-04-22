import sqlite3
import datetime

class averager(object):
    def getHourAverage(self, cur, id, day):
        '''THe function takes in as parameters a cursor to a database, the day of the week to be queried and the station id and returns the average
        available bikes available in the station for an hourly basis'''
        hourlyData = []
        selected_day = self.getDay(day)
        data = cur.execute('SELECT round(avg(Bikes_Available)) FROM Station_data WHERE Station_Number = ? AND strftime("%H",Time_Stamp) >= "06" AND strftime("%w",Time_Stamp) IN (?) GROUP BY strftime("%H",Time_Stamp)', (id, selected_day))  
        reading = data.fetchall()
        
        for i in reading:
            hourlyData.append(str(i[0]))
        
        return hourlyData
        
    def getDayAverage(self, cur, id):
        '''This function just takes in as parameters a cursor to a database and the station ID to be queried and returns the overall average
        available bike count for each day of the week'''
        dailyData = []
        
        
        data = cur.execute('SELECT round(avg(Bikes_Available)) FROM Station_data WHERE Station_Number = ? GROUP BY strftime("%w",Time_Stamp)', [id])  
        
        reading = data.fetchall()
        
        for i in reading:
            dailyData.append(str(i[0]))
        
        return dailyData
        
        
    def calculate_freetime(self, cur, id, day):
        day = self.getDay(day)
        # First we start with an empty array
        freetimedetails = []
        # This will pull data regarding stations overall
        totalRequests = cur.execute('SELECT strftime("%H",Time_Stamp)/3, count(*) FROM Station_data WHERE Station_Number = ? AND strftime("%H",Time_Stamp) >= "06" AND strftime("%w",Time_Stamp) IN (?) GROUP BY strftime("%H",Time_Stamp)/3', (id, day))
        total = totalRequests.fetchall()
        # This will pull data regarding stations if a stop is empty at one point during a three hour period
        empty_requests = cur.execute('SELECT strftime("%H",Time_Stamp)/3, count(*) FROM Station_data WHERE Bikes_Available = 0 AND Station_Number = ? AND strftime("%H",Time_Stamp) >= "06" AND strftime("%w",Time_Stamp) IN (?) GROUP BY strftime("%H",Time_Stamp)/3', (id, day))
        empty = empty_requests.fetchall()
        for detail in range(0, len(total)):
            full = total[detail][1]
            # This will pull the relevant empty data from the query, if it matches a station number found in total.
            emptydata = [val[1] for val in empty if val[0] == total[detail][0]]
            # This will set the value of empty data to 0 if a station number is never empty
            emptydata = 0 if len(emptydata) == 0 else emptydata[0]
            # This is the weighted calculation, where we get the percentage of emptyness during a three hour period, then get the average of that.
            average_wait_time = (emptydata/full)*180*emptydata/full
            # The next three lines gets it to the closest minute, averaged upwards.
            average_wait_time_minutes = int(average_wait_time//1)
            if average_wait_time%1*100 >= 1:
                average_wait_time_minutes += 1
            freetimedetails.append(average_wait_time_minutes)
        # print(freetimedetails)
        return freetimedetails
    
    def getHour(self, h):
        '''Returns the hour of the day used in an SQL query as a string'''
        if h < 10:
            return "0" + str(h)
        else:
            return str(h)
        
    def getDay(self, d):
        '''Returns the day of the week as it is represented in SQLite as a string that can be used for comparison'''
        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        return str(days.index(d))
    
