#!/usr/bin/python
import MySQLdb
import csv
import datetime
import os

def string_to_date(time):
    return time[2:4]+time[5:7]+time[8:10]+time[11:13]+time[14:16]+time[17:19]
#parameters
START_TIME = '2019-07-22 10:27:00'
END_TIME = '2019-07-22 15:27:00'
TABLE_NAME = 'ThermalBoard16ch'
#OUTPUT_DIR ='/home/cptlab/Desktop/MySQLdb_python/output/' 
OUTPUT_DIR ='/home/cptlab/Desktop/MySQLdb_python/output/'+TABLE_NAME+'/' 
os.system('mkdir -p '+ OUTPUT_DIR)

#connect to database
#db = MySQLdb.connect(host="192.168.0.109",  # this PC    
db = MySQLdb.connect(host="localhost",  # this PC    
#db = MySQLdb.connect(  # this PC    
		     user="remote",         # this user only has access to CPTLAB database
                     passwd="Cptlab30ps!",  # your password
                     db="CPTLab")        # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

# Use all the SQL selections
#query = "describe ThermalBoard16ch"
#query = "SELECT * FROM ThermalBoard16ch WHERE datetime BETWEEN {ts %s} AND {ts %s}"
query = "SELECT * FROM "+TABLE_NAME+" WHERE datetime BETWEEN {ts %s} AND {ts %s}"
#print((query,(TABLE_NAME, START_TIME,END_TIME,)))
#cur.execute(query,)
#cur.execute(query,(TABLE_NAME, START_TIME,END_TIME,))
cur.execute(query,(START_TIME,END_TIME,))

# create new csv file
output_file = OUTPUT_DIR+string_to_date(START_TIME)+"_"+string_to_date(END_TIME)+".csv"
with open(output_file,'wb') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for row in cur.fetchall():
        filewriter.writerow(row)
csvfile.close()
db.close()
