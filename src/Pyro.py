# Main file

from HttpServer import HttpServer
from SpeedMotor import SpeedMotor
from DifferentialDrive import DifferentialDrive
from Parser import parseJoystick
import time
import uasyncio as asyncio
x = 0
y = 0



def main():
    #Setup
    server = HttpServer("192.168.87.110",debug=False)
    drive = DifferentialDrive (2,0,4,16)

    def mainLoop():
        while True:
            x,y = server.getJoystick()
            drive.setInput(x,y)
            drive.Update()
            yield int(10)


    loop = asyncio.get_event_loop()
    loop.create_task(mainLoop())
    server.start()