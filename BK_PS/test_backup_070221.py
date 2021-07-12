#import pyvisa-py
import Thermal_PSControl as PS
import keyboard
import time
R = PS.InitiateResource()

PS.SetChannel(R)
PS.SetVoltage(R,0.0)
#PS.ChRead(R)
Pmax = 1.04
Imax = 3
V =0.00
P = 0.0

PS.SetVoltage(R,V)
while (1):
    PS.SetVoltage(R,V)
#    if(keyboard.read_key()=="q"):
 #       print("Key Press : Exit")
  #      PS.SetVoltage(R, 0)
   #     break
    #keyboard.on_press_key("p", lambda _:print("lo"))
    V, I, P = PS.ChRead(R)
    #time.sleep(1)
    
    if(P<= (Pmax-0.01) ):
        if(I>Imax):
            print("Current is too high, switching off")
            PS.SetVoltage(R,0)
            break
        print("increasing V")
        V+=0.005
        #PS.SetVoltage(R,V)
        
    elif(P>= (Pmax+0.01)):
        print("decreasing V")
        V-=0.005
        #PS.SetVoltage(R,V)
        
   
PS.DisableLVOutput(R)
