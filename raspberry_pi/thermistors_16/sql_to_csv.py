#!/usr/bin/python
import MySQLdb
import csv
csv_filename = 'test.csv'
HOST = "192.168.0.109"
USER = "root"
PW = "Cptlab30ps!"
DB = "CPTLab"
START_TIME = '2008-12-20 00:00:00'
END_TIME = '2008-12-20 23:59:59'






db = MySQLdb.connect(host=HOST,    # your host, usually localhost
                     user=USER,         # your username
                     passwd=PW,  # your password
                     db=DB)        # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()
print("connected")
# Use all the SQL you like
cur.execute("SELECT * FROM 16chanboard WHERE DateField BETWEEN {ts START_TIME} AND {ts END_TIME}")
#with open(csv_filename,'wb') as csvfile:
#    csvwriter = csv.writer(csvfile, delimiter=' ',
#                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
#    for row in cur.fetchall():
#	csvwriter.writerow(row)
db.close()
