
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

