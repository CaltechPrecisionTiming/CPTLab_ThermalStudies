''' Functions of this script:
	- Makes plots of raw thermistor temperature against time
	- Performs the calibration calculation
	- Calculated errors on each data point
	- Fits a function to the data and plots that function
	- This version can be easily adjustd with the variable tnum to be usd for any number of thermistors
	- Function to print the difference between two curves'''

import numpy as np
import matplotlib.pyplot as plt
import csv
import datetime
import math
from scipy import optimize

# Folder where data is
run = '08_01'
# Dataset in CSV format name 
csv_name = '190801150000_190801165500.csv'
# Calibration parameters for equation y = m*x+b [m, m_err, b, b_err] 
params = [-43.665458073158256,0.8768624135928127,2062.798170707191,20.195488554338798] #Old Calibration
pol = [-3.91522156e-09,2.81632590e-05,-8.46511612e-02,8.54732688e+01] #New Calibration
pol_t1 = [-3.89729037e-09,2.79790981e-05,-8.40525733e-02,8.48093235e+01] #Upper Error Curve (Thermistor 1 from calibration)
pol_t3 = [-3.97770921e-09,2.87241109e-05,-8.62962349e-02,8.70976157e+01] #Lower Error Curve (Thermistor 2 from calibration)

tnum = 24 

# Dictionaries for thermistor data
tdic,errdic,paramdic,covdic = {},{},{},{}
for i in range(tnum):
	for dic in [tdic,errdic,paramdic,covdic]: dic.update({i:[]})

# Time array
time_u = []

def polynomial(p,v):
	'''function to calculate a third-order polynomial'''
	return p[0]*float(v)**3 + p[1]*float(v)**2 + p[2]*float(v) + p[3]

def cal(v): 
	'''performs the calibration calculation with polynomial function'''
	return polynomial(pol,v)

def err(v): 
	'''find the upper annd lower limits of the data. Error is estimated as the
	difference between upper and lower / 2'''
	l = polynomial(pol_t1,v)
	s = polynomial(pol_t3,v)
	return abs(s-l)/2 

# Fill the dictionaries with calibrated data
with open(run + '/' + csv_name) as csvfile: 
	data = csv.reader(csvfile)
	for row in data:
		for key in tdic:tdic[key].append(cal(row[8-key]))
		for key in errdic:errdic[key].append(err(row[8-key]))
		time_u.append(row[23])

# Handling the time column
first_time = datetime.datetime.strptime(time_u[0],'%Y-%m-%d %H:%M:%S')
time_s = []

for i in time_u:
	'''function to convert yy-mm-dd h:m:s to elapsed time'''
	elapsed = datetime.datetime.strptime(i,'%Y-%m-%d %H:%M:%S') - first_time
	time_s.append((elapsed.total_seconds())/60)

# Fit function
def fit(x,a,b):
	'''function that data is being fit to'''
	return a*x+b 
	#return a - c * np.exp(-(x**d)/b)

# Loop to fit the fit fucntion to all data
for key in tdic:paramdic[key],covdic[key] = optimize.curve_fit(fit,time_s,tdic[key])

# Printing the difference between two curves at a certain time
def difference(time,n1,n2): 
	'''generates a statement that will print of the difference between to fitted curve at a spcific time'''
	print('Difference between {} and {}: {}'.format(n1,n2,abs(fit(time,*paramdic[n1]) - fit(time,*paramdic[n2]))))

difference(60,0,2)
difference(60,1,3)
difference(60,7,5)
difference(60,6,4)

def at_time(time,n):
	'''generates a statement that will print the value of a curve at a specific time'''
	print('At time {}, th {} = {}'.format(time,n,fit(time,*paramdic[n])))

for i in range(tnum):at_time(60,i)

# Plotting thermistor temprature vs time
# Raw Data plots
def raw_plot(n):
	'''generates a plot of the raw data'''
	plt.plot(time_s, np.asarray(tx), label = 'Thermistor '+n,  linestyle = 'none', marker = '.', markersize = 2)

def err_plot(n):
	'''generates a plot of the raw data with error bars'''
	plt.errorbar(time_s,np.asarray(tdic[n]),xerr = 0, yerr = errdic[n], linestyle = 'none', 
	marker = '.', markersize = 2, elinewidth = 0.5, capsize = 1, label = 'Thermistor '+str(n))

#for i in range(tnum): err_plot(i)

def fit_plot(n):
	'''generates the plot of a fit function'''
	plt.plot(time_s, fit(np.asarray(time_s),*paramdic[n]), label = 'Thermistor '+str(n)+' Fit')

for i in range(tnum): fit_plot(i)

# Lines to specify plot parameters
plt.xlabel('Time / min', fontsize =16)
plt.ylabel('Thermistor temperature / $^\circ$C', fontsize =16)
plt.title('Setup 2, '+ run, fontsize =16)
plt.legend(prop={'size':14})
plt.grid()
plt.show()
