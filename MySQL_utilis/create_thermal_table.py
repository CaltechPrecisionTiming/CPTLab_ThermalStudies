#!/usr/bin/python
import MySQLdb
import csv
import datetime

#parameters

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

NCh =16
q_str ="create table ThermalBoard"+str(NCh)+"ch (id int(11) NOT NULL PRIMARY KEY auto_increment, "
print(q_str)
# Use all the SQL selections
#query = "describe ThermalBoard8ch"
for iCh in range(NCh):
	#print(iCh)
	q_str +="temp"+str(iCh)+" decimal(8,4), "
	#print(q_str)
q_str += " Humidity_in decimal(6,4), Temp_in decimal(6,4), Humidity_HIH6130 decimal(6,4), Temp_HIH6130 decimal(6,4), Humidity_Si7021 decimal(6,4), Temp_Si7021 decimal(6,4), datetime datetime )"
print(q_str)
query = q_str
#query = "create table ThermalBoard32ch (id int(11) NOT NULL PRIMARY KEY auto_increment, temp0 decimal(8,4), Humidity decimal(6,4), Temp decimal(6,4), datetime datetime )"
cur.execute(query,)
#cur.execute(query,(START_TIME,END_TIME,))

