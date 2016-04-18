
import json
import sqlite3
import collections

__author__ = 'patrick'

''' 
The aim of this module is to import data from the sqlite3 database of logged bike data.
Process and analyse the data.
Export to a JSON accessible from the web page
'''

class GatherData:
    
    connection = sqlite3.connect("bike_scraper/bikedata.db")
    
    def read_sql_data(self, time_date = '2016-03-07 14:23:25.130891'):
        try:
            cur = self.connection.cursor()
            
            # Simple Test Query
            cur.execute("Select * from Station_Details where Total_Spaces=40 order by Station_Number")
            rows = cur.fetchall()
            for row in rows:
                print(row)
            
            # Complex recombination of data from sample time and date
            cur.execute("Select * from Station_Details join Station_Data on Station_Details.Station_Number=Station_Data.Station_Number where Time_Stamp='%s'" % time_date)
            rows = cur.fetchall()
            for row in rows:
                print(row)
            
            cur.close()
            return rows
            
        except FileNotFoundError:
            print("File Not Found!")
            return None
        except ConnectionError:
            print("Database Connection Failure!")
            return None 
        
    def generate_json(self, hourly, daily, free_time):
        
        
        
        output_list = []
        
    
        d = collections.OrderedDict()
        d['Daily'] = daily
        d['Times'] = hourly
        d['Free_Time'] = free_time

            
            
            
 
        output_list.append(d) 
        
        j = json.dumps(output_list)
        #output_file = 'bikeattime.json'
        #f = open(output_file, 'w')
        #print(j,file=f)
        #f.close()
        return j

