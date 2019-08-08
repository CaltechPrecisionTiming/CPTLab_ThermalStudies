''' Functions of this script: 
	- Produces a historgam for ach thermistor
	- Plots histograms using root
	- Writes the mean and standard deviation of the histograms into a csv file'''

import csv 
import numpy as np 
import ROOT as rt 
import math 
from glob import glob 

# Folder where data is found, names after the temperature
temp = '28_deg'
# Open and read file
f = open(temp+'/190726194500_190727131600.csv')
content = csv.reader(f)
tnum = 8 # Number of thermistors being calibrated

# Dictionaries used
tdic,hdic,cdic = {},{},{}
for i in range(tnum): 
	for dic in [tdic,hdic,cdic]: dic.update({i:[]})

# Fill the thermistor arrays
for r in content: 
	for key in tdic: tdic[key].append(float(r[key+1]))

def hist_fill(n):
	'''create histogram for each thermistor, maximum binning is used'''
	hdic[n] = rt.TH1F('h'+str(n),'Thermistor '+str(n),int(max(tdic[n])-min(tdic[n])),min(tdic[n]),max(tdic[n]))
	for i in range(len(tdic[n])): hdic[n].Fill(tdic[n][i])


def draw_hist(n):
	'''function that draws the created historgams with appropriate axis labels'''
	cdic[n] = rt.TCanvas('c'+str(n),'c'+str(n), 800, 600)
	hdic[n].GetXaxis().SetTitle('Thermistor '+str(n)+' Value')
	hdic[n].GetYaxis().SetTitle('Frequency')
	hdic[n].Draw()

def param_writer(n):
	'''writes a csv file with each line being: thermistor, mean, standard deviation'''
	with open('means_'+temp+'.csv','a') as csvFile:
		writer = csv.writer(csvFile)
		row = ['t'+str(n),hdic[n].GetMean(),hdic[n].GetRMS()]
		writer.writerow(row)
	csvFile.close()

# Function calls
for i in range(tnum):
	hist_fill(i)
	draw_hist(i)
	param_writer(i)

raw_input("Press enter to continue...")
