# Functions of this script
#	- Input 2 seperature versions of thermistors_time.py where two different data sets are analyzed
#	- Plots comparis

import numpy as np
import matplotlib.pyplot as plt
import csv
import datetime
import math
from scipy import optimize
#----------------------------------------------------------------------------------------------------------
import thermistors_time as t #first version of thrmistors_time.py
import ceramic as c #second version of thermistors_time.py with different data
#----------------------------------------------------------------------------------------------------------

# Plotting thermistor temprature vs time
# Plotting the raw data of the two data sets

def raw_plot(tx,shade,n): 
	plt.plot(t.time_s, tx, color = shade, label = 'Thermistor '+n,  linestyle = 'none', marker = '.', markersize = 2)

l = len(t.time_s)

raw_plot(t.t0[:l], '#EE8A31', '0, paste') 
raw_plot(c.t0[:l],'b','0, ceramic')
raw_plot(t.t1[:l], '#EE8A31', '1, paste') 
raw_plot(c.t1[:l],'b','1, ceramic')
raw_plot(t.t2[:l], '#EE8A31', '2, paste') 
raw_plot(c.t2[:l],'b','2, ceramic')
raw_plot(t.t3[:l], '#EE8A31', '3, paste') 
raw_plot(c.t3[:l],'b','3, ceramic')
raw_plot(t.t4[:l], '#EE8A31', '4, paste') 
raw_plot(c.t4[:l],'b','4, ceramic')
raw_plot(t.t5[:l], '#EE8A31', '5, paste')
raw_plot(c.t5[:l],'b','5, ceramic')
raw_plot(t.t6[:l], '#EE8A31', '6, paste') 
raw_plot(c.t6[:l],'b','6, ceramic')

# Plotting fitted functions of the two datasets
def fit_plot(shade,p,n, line):
	plt.plot(t.time_s, t.log(np.asarray(t.time_s),*p), color = shade, label = 'Thermistor '+n+' Fit',
	linestyle = line)

fit_plot('#EE8A31', t.params0[:l],'0, paste','-') 
fit_plot('#F30000', t.params1[:l],'1, paste','-') 
fit_plot('#09CB0C', t.params2[:l],'2, paste','-') 
fit_plot('#09C9CB', t.params3[:l],'3, paste','-') 
fit_plot('#0A5BE1', t.params4[:l],'4, paste','-')
fit_plot('#7F0AE1', t.params5[:l],'5, paste','-') 
fit_plot('#FFEA14', t.params6[:l],'6, paste','-')

fit_plot('#EE8A31', c.params0[:l],'0, ceramic','--') 
fit_plot('#F30000', c.params1[:l],'1, ceramic','--') 
fit_plot('#09CB0C', c.params2[:l],'2, ceramic','--') 
fit_plot('#09C9CB', c.params3[:l],'3, ceramic','--') 
fit_plot('#0A5BE1', c.params4[:l],'4, ceramic','--')
fit_plot('#7F0AE1', c.params5[:l],'5, ceramic','--') 
fit_plot('#FFEA14', c.params6[:l],'6, ceramic','--') 

plt.xlabel('Time / hrs', fontsize =16)
plt.ylabel('Thermistor temperature / $^\circ$C', fontsize =16)
plt.title('Comparison of 07_18 and 07_22', fontsize =16)
plt.legend(prop={'size':14})
plt.grid()

# Printing the difference between two curves at a certain time
def difference(time,p1,p2): 
	return str(abs(t.log(time,*p2) - t.log(time,*p1)))

print('1 Through plate ceramics: ' + difference(1,c.params0,c.params6))
print('1 Through plate paste: ' + difference(1,t.params0,t.params6))
print('1 Across plate ceramics: ' + difference(1,c.params5,c.params6))
print('1 Across plate paste: ' + difference(1,t.params5,t.params6))
print('3 Through plate ceramics: ' + difference(3,c.params0,c.params6))
print('3 Through plate paste: ' + difference(3,t.params0,t.params6))
print('3 Across plate ceramics: ' + difference(3,c.params5,c.params6))
print('3 Across plate paste: ' + difference(3,t.params5,t.params6))


#Plotting thermistor temperature vs distance for gradient across plate for both of the data sets
'''
def at_time(time, x):
	return [t.log(time,*x.params6),t.log(time,*x.params1),t.log(time,*x.params2),t.log(time,*x.params3),
	t.log(time,*x.params4),t.log(time,*x.params5)]

distances = [0,1,2,3,4,5]

plt.plot(distances,at_time(4,t), label = 'steady state paste', marker = '.')
plt.plot(distances,at_time(4,c), label = 'Steady state ceramics', marker ='.')
#plt.plot(distances,at_time(1), label = '1.0 hrs', marker = '.')
#plt.plot(distances,at_time(1.5), label = '1.5 hrs', marker = '.')
#plt.plot(distances,at_time(2), label = '2.0 hrs', marker = '.')
#plt.plot(distances,at_time(2.5), label = '2.5 hrs', marker = '.')
#plt.plot(distances,at_time(3), label = '3.0 hrs', marker = '.')
plt.xlabel('Distance from resistors / cm', fontsize=16)
plt.ylabel('Temperature / $^\circ$C', fontsize=16) 
plt.legend(prop={'size':10})
plt.title('Ceramic comparison, Gradient along plate', fontsize=16)
plt.xlim(left = 0, right = 5)
plt.grid()
'''
plt.show()
