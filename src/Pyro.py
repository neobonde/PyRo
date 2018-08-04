# Main file

from HttpServer import HttpServer
from SpeedMotor import SpeedMotor
from DifferentialDrive import DifferentialDrive
from Parser import parseJoystick
import time
x = 0
y = 0

def main():
    
    networkSR_ms = 100 
    controllerSR_us = 5000

    #Setup
    server = HttpServer(networkSR_ms)
    # motorLeft = SpeedMotor(2,0)
    # motorRight = SpeedMotor(4,16)
    drive = DifferentialDrive (2,0,4,16)




    lastNetwork = time.ticks_ms()
    lastControl = time.ticks_us()
    #Main loop
    while(True):
        if(time.ticks_diff(time.ticks_ms(), lastNetwork) > networkSR_ms):
            lastNetwork = time.ticks_ms()
            handleNetworking(server)
            drive.setInput(x,y)
            # motorLeft.SetSpeed(x)
            # motorRight.SetSpeed(x)
        
        if(time.ticks_diff(time.ticks_us(),lastControl) > controllerSR_us):
            lastControl = time.ticks_us()
            # motorLeft.Update()
            # motorRight.Update()
            drive.Update()
            # print(motorLeft.GetActualSpeed())



def handleNetworking(server):
    server.acceptConn()
    response = server.getResponse()
    if response is not None:
        global x
        global y
        x, y =  parseJoystick(response)

