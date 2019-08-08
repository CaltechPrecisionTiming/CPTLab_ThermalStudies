'''Function of this script:
	- Reads the seperate files for each temperature
	- Sorts them by thermistor and includes the measured tempertaure of the RTD'''

import csv 
tnum = 8
for therm in range(tnum):
	temp_names = ['15','18','20','22','24','26','28','30','35','40']

	data = []
	data_err = [] 

	def extract(t):
		'''extracts the data from the files sorted by temperature'''
		for temp in temp_names:
			content = csv.reader(open('means_'+temp+'_deg.csv'))
			for r in content: 
				if r[0] == 't'+str(therm):
					data.append(r[1])
					data_err.append(r[2])

	def writer(rtd):
		'''writes new files sorted by thermistor'''
		with open('t'+ str(therm) +'_means.csv','a') as csvFile:
			writer = csv.writer(csvFile)
			row = [temp_values[rtd],data[rtd],data_err[rtd]]
			writer.writerow(row)
		csvFile.close()

	extract(therm)

	temp_values = [-14.9,-17.8,-19.0,-21.9,-23.8,-25.7,-27.6,-30.5,-35.1,-39.5]

	for i in range(len(temp_values)):
		writer(i)


