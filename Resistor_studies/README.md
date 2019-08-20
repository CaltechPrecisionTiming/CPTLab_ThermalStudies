#Documentation for resistor studies

##Purpose:
- Used to analyse data from studies where the dummy resistor loads were used to generate heat

##Description of included files:

**thermistors_time.py**
- Uses variables to convert th data in csv files to arrays
- Fills array one by one, not in loop good for when the thermistors are not neccesarily in a continues order
Use for: plotting the thermistors versus the time. Can also plot the gradient across the plate. 


**thermistors_timeerr.py**
- Stores data in csv files into dictionaries, this lend for a very clean code
- This only works for when you know the labels of the thermistors are correct and correpond to the column 
they are placed into. This is because the code runs a loop to fill the dictionary
Use for: plotting thermistors versus time with errors


**compare.py**
- Imports two different thermistors_time.py scripts and plots comparisons of them 
USe for: comparing the curves for with ceramics against those without 
