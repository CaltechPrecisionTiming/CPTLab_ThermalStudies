# Documentation for Raspberry Pi scripts

## Purpose: 
- Configure ADC 
- Communicate with ADC and readout the thermistor data as well as temperatures and humidities from the enviromental sensors

## Repository Description: 
All of the repositories contain the same files, they are just configured for a different number of thermistors

**thermistors_8**
- 1 ADC, 8 channels

**thermistors_16** 
- 2 ADCs, 16 channels

**thermistors_24**
- 3 ADCs, 24 channels

## Description of the files included:

### configuration 

**config.conf** 
- ?? 

**configuration.h**

**configuration.c** 

### gpiointerf

**gpiointerf.h**
- header file for gpiointerf.cpp

**gpiointerf.cpp** 
- constructor: calls initialize on all ADCs 
- initialize: ??
- TH: function to read from ChipCap 2-SIP temperature and humidity sensor 
- TH2: function to read from Adafruit HTU21D-F temperature and humidity sensor
- TH_HIH6130: function to read from Sparkfun HIH6130 temperature and humidity sensor
- TH_Si7021: function to read from Sparkfun Si7021 temperature and humidity sensor
- Temp: reads temperature of a specified thermistor channel 
- activate: if statements for each ADC to be started
- desconnect: disconnects from all? 

### databasesectr 
**databasesectr.h**
- header file for databasesectr.cpp

**databasesectr.cpp** 
- constructor: ? 
- DBconfig: connects to MySQL database 
- mysql_diconnect: closes connection to dtabase
- set_Dat: produces string command for MySQL with data
- set_Im: ?
- set_T: ? 

### cratecontrol

**cratecontrol.cpp** 
- Defines: number of ADCs, channels
- main function: starts BTL monitoring system, initializes ADCs that need to be used, reads thermistors temperatures and enviromental sensors, connects to database and inserts the data

