__author__ = 'devin'
import sqlite3

connection = sqlite3.connect("bikedata.db")
try:
    c = connection.cursor()
    c.execute('''ALTER TABLE Station_Details RENAME TO Station_Details_Temp ''')
    c.execute('''CREATE TABLE Station_Details(Station_Number INT PRIMARY KEY,
                Station_Name CHAR(50), latitude REAL, longitude REAL, Total_Spaces INT,
                Banking BOOLEAN, Bonus BOOLEAN)''')
    c.execute('''INSERT INTO Station_Details(Station_Number, Station_Name, 
            latitude, longitude, Total_Spaces, Banking, Bonus)
            SELECT Station_Number, Station_Name, longtitude, latitude, 
            Total_Spaces, Banking, Bonus FROM Station_Details_Temp''')
    c.execute('''DROP TABLE Station_Details_Temp''')
    connection.commit()
    c.close()
except ConnectionError:
    print("Error")
