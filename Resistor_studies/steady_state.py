import numpy as np
import csv
import math
import sys
import datetime

# Dataset in CSV format name
csv_name = sys.argv[1]
therm = int(sys.argv[2])

# Calibration parameters for a cubic fit
pol = [-3.91522156e-09,2.81632590e-05,-8.46511612e-02,8.54732688e+01] #New Calibration
pol_t1 = [-3.89729037e-09,2.79790981e-05,-8.40525733e-02,8.48093235e+01]
pol_t3 = [-3.97770921e-09,2.87241109e-05,-8.62962349e-02,8.70976157e+01]

# Output time
tunit = [["min", 60], ["hrs",60*60]]
index = 1
# Arrays for thermistor data
t0,t1,t2,t3,t4,t5,t6,t7 = [],[],[],[],[],[],[],[]
t8,t9,t10,t11,t12,t13,t14,t15 = [],[],[],[],[],[],[],[]
t16,t17,t18,t19,t20,t21,t22,t23 = [],[],[],[],[],[],[],[]
te0,te1,te2,te3,te4,te5,te6,te7 = [],[],[],[],[],[],[],[]
te8,te9,te10,te11,te12,te13,te14,te15 = [],[],[],[],[],[],[],[]
te16,te17,te18,te19,te20,te21,te22,te23 = [],[],[],[],[],[],[],[]
# Time array
time_u = []
tempSens = []
# Calibration function
def cal(v):
	#return (float(v)-params[2])/params[0]
	return pol[0]*float(v)**3 + pol[1]*float(v)**2 + pol[2]*float(v) + pol[3]
def err(v):
	l = pol_t1[0]*float(v)**3 + pol_t1[1]*float(v)**2 + pol_t1[2]*float(v) + pol_t1[3]
	s = pol_t3[0]*float(v)**3 + pol_t3[1]*float(v)**2 + pol_t3[2]*float(v) + pol_t3[3]
	return abs(s-l)/2
def split_data(t,te,value):
	t.append(cal(value))
	te.append(err(value))
if therm == 8:
	cols = [1,2,3,4,5,6,7,8]
	tim = 13
elif therm == 16:
	cols = [1,2,3,4,5,6,7,8,16,15,14,13,12,11,10,9]
	tim = 23
elif therm == 24:
	cols = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
	tim = 31
tss = [t0,t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15,t16,t17,t18,t19,t20,t21,t22,t23]
tes = [te0,te1,te2,te3,te4,te5,te6,te7,te8,te9,te10,te11,te12,te13,te14,te15,te16,te17,te18,te19,te20,te21,te22,te23]

with open(csv_name) as csvfile:
	data = csv.reader(csvfile)
	for row in data:
		if not float(row[tim-1]) == 0:
			for i in range(0,therm):
				split_data(tss[i],tes[i],row[cols[i]])
			time_u.append(row[tim])
		else:
			print("Too much data, but will calculate without the extra.  New Endtime:",time_u[-1])
			break
first_time = datetime.datetime.strptime(time_u[0],'%Y-%m-%d %H:%M:%S')
if len(sys.argv) >= 5:
	str = sys.argv[3] + ' ' + sys.argv[4]
	las = datetime.datetime.strptime(str,'%Y-%m-%d %H:%M:%S') - first_time
	total = (las.total_seconds())/tunit[index][1]
else:
	total = 10**10
if len(sys.argv) >= 7:
	str = sys.argv[5] + ' ' + sys.argv[6]
	fir = datetime.datetime.strptime(str,'%Y-%m-%d %H:%M:%S') - first_time
	first = (fir.total_seconds())/tunit[index][1]
else:
	first = 0
time_s = []

for i in time_u:
	elapsed = datetime.datetime.strptime(i,'%Y-%m-%d %H:%M:%S') - first_time
	time_s.append((elapsed.total_seconds())/tunit[index][1])
tbefore = 0
printed = False
for time in enumerate(time_s):
	if time[1]-tbefore>.005 and first <= time[1] or time[1]>=total-0.001:
		print("Too much data, but will calculate without the extra.  New Endtime:",time_u[time[0]])
		for t in range(therm):
			tss[t] = tss[t][:(time[0]-1)]
			tes[t] = tes[t][:(time[0]-1)]
		printed = True
		break
	tbefore = time[1]
if not printed:
	print(time_u[-1])

print (csv_name,'\nNumber of data points:', len(tss[0]))
def steady_state(ts,te,size):
	ts = ts[-size:]
	te = te[-size:]
	nts = np.array(ts)
	avg = np.mean(nts)
	std = np.std(nts)
	err = np.mean(te)
	return avg,std,err
def atPoint(n):
	st = []
	stdd=[]
	err=[]
	for i in range(0,therm):
		steady = steady_state(tss[i],tes[i],n)
		st.append(steady[0])
		stdd.append(steady[1])
		err.append(steady[2])
	return np.round(st,2),np.round(stdd,2),np.round(err,2)
def printAtPoint(n):
	print('Number of data points averaged over:', n)
	p = atPoint(n)
	print(p[0],round(np.mean(p[0]),2))
	print(p[1],round(np.mean(p[1]),2))
	print(p[2],round(np.mean(p[2]),2))
def stdAtPoint(n):
	p = atPoint(n)
	return np.mean(p[1]),np.mean(p[2])

theThings = stdAtPoint(20)
if theThings[0]<=theThings[1]:
	print("Below error of calibration.")
else:
	print("Not below error of calibration.")
size=len(tss[0])
bav = stdAtPoint(20)[0]
notyet = False
prevStep = 0
for step in [1000,100,10,1]:
	size += prevStep
	done = False
	while not done:
		av = stdAtPoint(size)[0]
		if abs(bav-av)<= 0.001 or size <=step:
			done = True
			break
		size-=step
	prevStep = step
if size >200:
	print("Reached equilibrium.")
	printAtPoint(size)
else:
	print("Failed to reach equilibrium by 200 points before end of data.")
	printAtPoint(200)
