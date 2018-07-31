# Main file

from HttpServer import HttpServer
from SpeedMotor import SpeedMotor
from Parser import parseJoystick
import time
x = 0
y = 0

def main():
    
    networkSR_ms = 100 
    controllerSR_us = 500

    #Setup
    server = HttpServer(networkSR_ms)
    motorLeft = SpeedMotor(2,0)


    lastNetwork = time.ticks_ms()
    lastControl = time.ticks_us()
    #Main loop
    while(True):
        if(time.ticks_diff(time.ticks_ms(), lastNetwork) > networkSR_ms):
            # print("network")
            lastNetwork = time.ticks_ms()
            handleNetworking(server)
            motorLeft.SetSpeed(x)
        
        if(time.ticks_diff(time.ticks_us(),lastControl) > controllerSR_us):
            # print("update")
            lastControl = time.ticks_us()
            motorLeft.Update()
            # print(motorLeft.GetActualSpeed())



def handleNetworking(server):
    server.acceptConn()
    response = server.getResponse()
    if response is not None:
        global x
        global y
        x, y =  parseJoystick(response)

