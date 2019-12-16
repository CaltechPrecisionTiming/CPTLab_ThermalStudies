import mysql.connector
import numpy as np
import os

def getData(time_frame):
    N_thermistor = 8
    TABLE_NAME = 'ThermalBoard{}ch'.format(N_thermistor)

    hostip = 'localhost' if os.uname()[1] == 'dhcp-112-216.caltech.edu' else '192.168.0.109'

    mydb = mysql.connector.connect(
        host=hostip,
        user='remote',
        passwd='Cptlab30ps!',
        database='CPTLab',
        auth_plugin='mysql_native_password'
    )
    cursor = mydb.cursor()

    query = 'SELECT * FROM '+TABLE_NAME+' WHERE datetime BETWEEN {ts %s} AND {ts %s}'
    cursor.execute(query,(time_frame[0],time_frame[1],))
    out = []
    for row in cursor.fetchall():
        th_raw = [row[-1]]
        for i in range(1, len(row)-1):
            th_raw.append(float(row[i]))
        out.append(th_raw)

    return out
