'''Function of this script: 
	- reads data from each thermistor file and stores as array
	- fits a function to each array
	- writes the fit parameters into a new csv file
	- computes mean parameters from all thermistors'''

import numpy as np
import matplotlib.pyplot as plt
import csv
import datetime
import math
from scipy import optimize

sum_params = [0,0,0,0] #sums of parameters will be added to calculate mean
grid = np.linspace(2500,3800,1500) #gridspace on which the fitted curves are plotted
tnum = 8 #number of thermistors used in calibration

for i in range(tnum):
	n = str(i)

	t = []
	terr = []
	rtd = []
	
	#read thermistor files into arrays
	with open('means/t'+n+'_means.csv') as csvfile: 
		data = csv.reader(csvfile)
		for row in data:
			rtd.append(float(row[0]))
			t.append(float(row[1]))
			terr.append(float(row[2]))

	def fit_func(x,a,b,c,d):
		'''the function to which data is fitted for each thermistor'''
		return a*x**3 + b*x**2 + c*x + d 

	params,pcov = optimize.curve_fit(fit_func,t,rtd)

	sum_params += params

	plt.errorbar(t, rtd,xerr = terr, yerr = 0.2, color = 'r', label = 'Thermistor '+n,  linestyle = 'none', markersize = 2, capsize = 2, marker = 'o')
	plt.plot(grid, fit_func(np.asarray(grid),*params), label = 'Thermistor '+n+' Fit')
	plt.title('Calibration Curve, Thermistor ' + n)
	plt.ylabel('RTD measured Celcius')
	plt.xlabel('Thermistor Values')
	plt.grid()

	#write calculated parameters into a file
	with open('all_fit_params.csv','a') as csvFile:
		writer = csv.writer(csvFile)
		row = [n,params]
		writer.writerow(row)
	csvFile.close()
	#plt.show() #uncomment to display graphs seperatly

#calulcate and plot mean curve
mean_params = sum_params/tnum
plt.plot(grid, fit_func(np.asarray(grid),*mean_params), label = 'Average Fit')

#write mean curve parameters into same csv file
with open('all_fit_params.csv','a') as csvFile:
	writer = csv.writer(csvFile)
	row = ['Average',mean_params]
	writer.writerow(row)
csvFile.close()

plt.legend()
plt.show()

