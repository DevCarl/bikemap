import sqlite3
import datetime

class averager(object):
    def getDayAverage(self, cur, id, day):
        #This function will take in a day of the week as a string and return the average
        #available bikes for that DAY
        dailyData = []
        selected_day = self.getDay(day)
        
        for x in range(6,24):
            selected_hour = self.getHour(x)
            data = cur.execute('SELECT round(avg(Bikes_Available)) FROM Station_data WHERE Station_number = ? AND strftime("%H",Time_Stamp) IN (?) AND strftime("%w",Time_Stamp) IN (?)', (id, selected_hour,selected_day))
            reading = data.fetchall()
            
            dailyData.append(str(reading[0][0]))
        
        return dailyData
        
    def getHour(self, h):
        if h < 10:
            return "0" + str(h)
        else:
            return str(h)
        
    def getDay(self, d):
        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        return str(days.index(d))
    
