import sqlite3
import datetime

class averager(object):
    def getHourAverage(self, cur, id, day):
        #This function will take in a day of the week as a string and return the average
        #available bikes for that DAY
        hourlyData = []
        selected_day = self.getDay(day)
        data = cur.execute('SELECT round(avg(Bikes_Available)) FROM Station_data WHERE Station_Number = ? AND strftime("%H",Time_Stamp) >= "06" AND strftime("%w",Time_Stamp) IN (?) GROUP BY strftime("%H",Time_Stamp)', (id, selected_day))  
        reading = data.fetchall()
        
        for i in reading:
            hourlyData.append(str(i[0]))
        
        return hourlyData
        
    def getDayAverage(self, cur, id):
        
        dailyData = []
        
        
        data = cur.execute('SELECT round(avg(Bikes_Available)) FROM Station_data WHERE Station_Number = ? GROUP BY strftime("%w",Time_Stamp)', [id])  
        
        reading = data.fetchall()
        
        for i in reading:
            dailyData.append(str(i[0]))
        
        return dailyData
        
    
    def getHour(self, h):
        if h < 10:
            return "0" + str(h)
        else:
            return str(h)
        
    def getDay(self, d):
        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        return str(days.index(d))
    
