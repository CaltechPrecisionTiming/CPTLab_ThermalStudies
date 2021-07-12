# CPTLab_ThermalStudies
CPTLab Thermal Studies

This is a repository for code that was used to collect thermal dissipation data for the BTL SiPM module during summer 2021.


## Repository Descriptions
**BK_PS**
Contains scripts that control the power supply that runs current through the SiPM array to model dark current production. These were modified to be completely automatic and can be run remotely.

**MySQL_utilis**
This mainly contains a program that converts data read out from thermistors into an SQL database to csv files that can be analyzed and plotted using the programs within SiPM_Heating. 

**SiPM_Heating** 
Contains a script that plots thermistor readout data in a readable, easily customizable, fashion. Also contains copies of relavant csv datasets for ease of access. 

**thermistors**
Contains all programs used to read data out from the thermistors into an SQL database, which can then be accessed using MySQL_utilis.