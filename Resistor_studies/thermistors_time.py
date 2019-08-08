# Functions of this script: 
# 	- Makes plots of raw thermistor temperature against time 
#	- Performs the calibration calculation
#	- Fits a function to the data and plots that function
#	- Generates a plot of the gradient across the plate
#	- This version is for 16 thermistors
#	- Function to print the difference between two curves
#---------------------------------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
import csv
import datetime
import math
from scipy import optimize

# Folder where data is
run = '07_22'
# Dataset in CSV format name 
csv_name = '190722102700_190722152700.csv'
# Calibration parameters for equation y = m*x+b [m, m_err, b, b_err] 
params = [-43.665458073158256, 0.8768624135928127,2062.798170707191,20.195488554338798]
#Re-calibration parameters for equation y = a*x**3 + b*x**2 +c*x + d [a,b,c,d]
pol = [-6.67833463e-09,5.48792561e-05,-1.70161500e-01,1.75982323e+02]
# Arrays for thermistor data
t0,t1,t2,t3,t4,t5,t6,t7 = [],[],[],[],[],[],[],[]
t8,t9,ta,tb,tc,td,te,tf = [],[],[],[],[],[],[],[]
# Arrays for thermistor data errors
t0err,t4err= [],[]
# Time array
time_u = []

# Calibration function
def cal(v):
	#return (float(v)-params[2])/params[0]
	return pol[0]*float(v)**3 + pol[1]*float(v)**2 + pol[2]*float(v) + pol[3]
def err(v): 
	l = (float(v)-params[2]-params[3])/(params[0]-params[1])
	s = (float(v)-params[2]+params[3])/(params[0]+params[1])
	return abs(s-l)/2 

with open(run + '/' + csv_name) as csvfile: 
	data = csv.reader(csvfile)
	for row in data:
		t0.append(cal(row[1]))
		t0err.append(err(row[1]))
		t1.append(cal(row[2]))
		t2.append(cal(row[3]))
		t3.append(cal(row[4]))
		t4.append(cal(row[5]))
		t4err.append(err(row[5]))
		t5.append(cal(row[6]))
		t6.append(cal(row[7]))
		t7.append(cal(row[8]))
		t8.append(cal(row[16]))
		t9.append(cal(row[15]))
		ta.append(cal(row[14]))
		tb.append(cal(row[13]))
		tc.append(cal(row[12]))
		td.append(cal(row[11]))
		te.append(cal(row[10]))
		tf.append(cal(row[9]))
		time_u.append(row[23])

first_time = datetime.datetime.strptime(time_u[0],'%Y-%m-%d %H:%M:%S')

time_s = []

for i in time_u: #converts the hours time stamp to time elapsed
	elapsed = datetime.datetime.strptime(i,'%Y-%m-%d %H:%M:%S') - first_time
	time_s.append((elapsed.total_seconds())/60)

# Fit function
def fit(x,a,b):
	return a*x+b 
	#return a + c * np.exp(-(x**d)/b)
	#return a*np.log(x)+b	
	#return (1/((a*x)**(1/2)))*np.exp(-b/x)+c

# Fitting the data to the above fit function 
params0,paramscov0 = optimize.curve_fit(fit,time_s,t0)
params1,paramscov1 = optimize.curve_fit(fit,time_s,t1)
params2,paramscov2 = optimize.curve_fit(fit,time_s,t2)
params3,paramscov3 = optimize.curve_fit(fit,time_s,t3)
params4,paramscov4 = optimize.curve_fit(fit,time_s,t4)
params5,paramscov5 = optimize.curve_fit(fit,time_s,t5)
params6,paramscov6 = optimize.curve_fit(fit,time_s,t6)
params7,paramscov7 = optimize.curve_fit(fit,time_s,t7)

params8,paramscov8 = optimize.curve_fit(fit,time_s,t8)
params9,paramscov9 = optimize.curve_fit(fit,time_s,t9)
paramsa,paramscova = optimize.curve_fit(fit,time_s,ta)
paramsb,paramscovb = optimize.curve_fit(fit,time_s,tb)
paramsc,paramscovc = optimize.curve_fit(fit,time_s,tc)
paramsd,paramscovd = optimize.curve_fit(fit,time_s,td)
paramse,paramscove = optimize.curve_fit(fit,time_s,te)
paramsf,paramscovf = optimize.curve_fit(fit,time_s,tf)

# Printing the difference between two curves at a certain time
def difference(time,p1,p2): 
	return abs(fit(time,*p2) - fit(time,*p1))

print('Difference between 1 and 7: {}'.format(difference(20,params1,params7)))
print('Difference between 0 and 4: {}'.format(difference(20,params0,params4)))
print('Difference between 2 and 6: {}'.format(difference(20,params2,params5)))
print('Difference between 3 and 5: {}'.format(difference(20,params3,params6)))

print('Th 0: {}'.format(fit(20,*params0)))
print('Th 1: {}'.format(fit(20,*params1)))
print('Th 2: {}'.format(fit(20,*params2)))
print('Th 3: {}'.format(fit(20,*params3)))
print('Th 4: {}'.format(fit(20,*params4)))
print('Th 5: {}'.format(fit(20,*params5)))
print('Th 6: {}'.format(fit(20,*params6)))
print('Th 7: {}'.format(fit(20,*params7)))

# Plotting thermistor temprature vs time
# Raw Data plots
def raw_plot(tx,c,n): 
	plt.plot(time_s, np.asarray(tx), color = c, label = 'Thermistor '+n,  linestyle = 'none', marker = '.', markersize = 2)

raw_plot(t0, '#EE8A31', '0') #On resistor
raw_plot(t1, '#F30000', '1') #Plate
raw_plot(t2, '#09CB0C', '2') #Plate
raw_plot(t3, '#09C9CB', '3') #Plate
raw_plot(t4, '#0A5BE1', '4') #Plate
raw_plot(t5, '#7F0AE1', '5') #Plate
raw_plot(t6, '#FFEA14', '6') #Top of T
raw_plot(t7, '#007A18', '7') #Bottom of T
raw_plot(t8, '#EE8A31', '8') #On Resistor 
raw_plot(t9, '#F974FF', '9') #On top of c
raw_plot(ta, '#F30000', 'a') #Plate
raw_plot(tb, '#09CB0C', 'b') #Plate
raw_plot(tc, '#09C9CB', 'c') #Plate
raw_plot(td, '#0A5BE1', 'd') #Plate
raw_plot(te, '#7F0AE1', 'e') #Plate
raw_plot(tf, '#4800A5', 'f') #Floor

#Plotting the graph of the fitted function
def fit_plot(c,p,n):
	plt.plot(time_s, fit(np.asarray(time_s),*p), color = c, label = 'Thermistor '+n+' Fit')

fit_plot('#EE8A31',params0,'0')
fit_plot('#F30000',params1,'1')
fit_plot('#09CB0C',params2,'2')
fit_plot('#09C9CB',params3,'3')
fit_plot('#0A5BE1',params4,'4')
fit_plot('#7F0AE1',params5,'5')
fit_plot('#FFEA14',params6,'6')
fit_plot('#007A18',params7,'7')
fit_plot('#EE8A31',params8,'8')
fit_plot('#F974FF',params9,'9')
fit_plot('#F30000',paramsa,'a')
fit_plot('#09CB0C',paramsb,'b')
fit_plot('#09C9CB',paramsc,'c')
fit_plot('#0A5BE1',paramsd,'d')
fit_plot('#7F0AE1',paramse,'e')
fit_plot('#4800A5',paramsf,'f')

plt.xlabel('Time / min', fontsize =16)
plt.ylabel('Thermistor temperature / $^\circ$C', fontsize =16)
plt.title('Setup 2, '+ run, fontsize =16)
plt.legend(prop={'size':14})
plt.grid()
#----------------------------------------------------------------------------------------------------
#Plotting thermistor temperature vs distance for gradient across plate
def at_time(time):
	return [fit(time,*params6),fit(time,*params1),fit(time,*params2),fit(time,*params3),
	fit(time,*params4),fit(time,*params5)]

distances = [0,1,2,3,4,5]
'''
plt.plot(distances,at_time(0.5), label = '0.5 hrs', marker = '.')
plt.plot(distances,at_time(1), label = '1.0 hrs', marker = '.')
plt.plot(distances,at_time(1.5), label = '1.5 hrs', marker = '.')
plt.plot(distances,at_time(2), label = '2.0 hrs', marker = '.')
plt.plot(distances,at_time(2.5), label = '2.5 hrs', marker = '.')
plt.plot(distances,at_time(3), label = '3.0 hrs', marker = '.')
plt.plot(distances,at_time(3.5), label = '3.5 hrs', marker = '.')
plt.plot(distances,at_time(4), label = '4.0 hrs', marker = '.')
plt.xlabel('Distance from resistors / cm', fontsize=16)
plt.ylabel('Temperature / $^\circ$C', fontsize=16) 
plt.legend(prop={'size':10})
plt.title('Setup 2, Gradient along plate', fontsize=16)
plt.xlim(left = 0, right = 5)
'''
#----------------------------------------------------------------------------------------------------

plt.show()
