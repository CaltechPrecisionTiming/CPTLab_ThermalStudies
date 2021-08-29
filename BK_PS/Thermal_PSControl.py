
import pyvisa


#Retrieves the names of the devices (resources) connected to the computer. Prompts
#for resource to use and returns the selected resource.
def InitiateResource():
    VISAInstance=pyvisa.ResourceManager('@py')
    #VISAInstance=pyvisa.ResourceManager()
    ResourceList=VISAInstance.list_resources()
    #print(ResourceList)
#    for index in range(len(ResourceList)):
#        print("Device number " + str(index) + " - " + ResourceList[index])
#    DeviceNumber = input("Which device would you like to use? ")
#    resourceName=ResourceList[int(DeviceNumber)]
    resourceName='USB0::65535::37168::602361010736820007::0::INSTR'#ResourceList[0]
    #resourceName = 'ASRL/dev/ttyAMA0::INSTR'
    Resource = VISAInstance.open_resource(resourceName)#,write_termination='\n',read_termination='\r')
    print(Resource.query("*IDN?"))
    
    print("Set remote access")
    Resource.write("SYSTEM:REMOTE") #Set device to remote control
    return Resource

#Prompts and sets which channel of the device to communicate with
def SetChannel(Resource):
    Resource.write("outp on")
    ChannelNumber = input("Which channel? ")
    ChannelNumber=int(ChannelNumber)
    if ChannelNumber == 1:
        cmd1 = "inst CH1"
    elif ChannelNumber == 2:
        cmd1 = "inst CH2"
    elif ChannelNumber == 3:
        cmd1 = "inst CH3"
    Resource.write(cmd1)
    print("Set channel to "+str(ChannelNumber)+"\n")

#Takes a voltage and sets the channel to that voltage.
def SetVoltage(Resource, ChVoltage, safetyCheck=False):
    cmd2 = "volt " + str(ChVoltage) + "V"
    if ChVoltage <= 2 and ChVoltage >= 0 or not safetyCheck: #Safety check -- if true, then check that voltage doesn't exceed 2V.
        Resource.write(cmd2)
    else:
        print ('[WARNING] : The voltage is out of the bounds [0-2V], not changing the low voltage supply output')

ddef ChRead(Resource, safetyCheck=True):
    Resource.write('*IDN?')
    idn = Resource.read()

    V = float(Resource.query('MEASure:VOLTage:DC?'))
    I = float(Resource.query('MEASure:CURRent:DC?'))
    print("Current",I)
    print("Voltage",V)

    # open-pin prototype resistance correction values
    #R_s = 1.7
    #R_wires = 0.19

    # flex-cable prototype resistance correction values
    #R_s = 0.286
    R_wires = 0.19


    V_s = V - (R_wires * I)
    P = V_s*I
    print("Power",P)
    return V, I, P

def DisableLVOutput(Resource):
    Resource.write("outp off")
    #Resource.read()
    print("Disabled LV Output")
