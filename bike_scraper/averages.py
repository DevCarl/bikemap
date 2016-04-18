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
        
        
    def calculate_freetime(self, cur, id, day):
        day = self.getDay(day)
        freetimedetails = []
        totalRequests = cur.execute('SELECT strftime("%H",Time_Stamp)/3, count(*) FROM Station_data WHERE Station_Number = ? AND strftime("%H",Time_Stamp) >= "06" AND strftime("%w",Time_Stamp) IN (?) GROUP BY strftime("%H",Time_Stamp)/3', (id, day))
        total = totalRequests.fetchall()
        empty_requests = cur.execute('SELECT strftime("%H",Time_Stamp)/3, count(*) FROM Station_data WHERE Bikes_Available = 0 AND Station_Number = ? AND strftime("%H",Time_Stamp) >= "06" AND strftime("%w",Time_Stamp) IN (?) GROUP BY strftime("%H",Time_Stamp)/3', (id, day))
        empty = empty_requests.fetchall()
        for detail in range(0, len(total)):
            full = total[detail][1]
            emptydata = [val[1] for val in empty if val[0] == total[detail][0]]
            emptydata = 0 if len(emptydata) == 0 else emptydata[0]
            average_wait_time = (emptydata/full)*180*emptydata/full
            average_wait_time_minutes = int(average_wait_time//1)
            if average_wait_time%1*100 >= 1:
                average_wait_time_minutes += 1
            freetimedetails.append(average_wait_time_minutes)
        print(freetimedetails)
        return freetimedetails
    
    def getHour(self, h):
        if h < 10:
            return "0" + str(h)
        else:
            return str(h)
        
    def getDay(self, d):
        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        return str(days.index(d))
    
