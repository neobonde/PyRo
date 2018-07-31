import machine
from Util import Lerp

class SpeedMotor:
    def __init__(self, forwardPin, backwardPin):
        self.forwardPWM = machine.PWM(machine.Pin(forwardPin,1000))
        self.backwardPWM = machine.PWM(machine.Pin(backwardPin,1000))
        
        self.prevSpeed = 0
        self.actSpeed = 0
        self.speed = 0
        self.lerpStep = 0

        self.lerpSpeed = 1/50

    
    # Pass a speed between -100 and 100
    def SetSpeed(self, speed):
        self.prevSpeed = self.actSpeed
        # Range check passed speed
        self.speed = 100 if speed > 100 else speed
        self.speed = -100 if speed < -100 else speed

        self.lerpStep = 0


    def GetActualSpeed(self):
        return self.actSpeed

    def Update(self):
        
        self.lerpStep += self.lerpSpeed
        if self.lerpStep >= 1:
            self.lerpStep == 1
        self.actSpeed = int(Lerp(self.lerpStep,self.prevSpeed,self.speed))
        
        # If speed is positive we are moving forward
        if self.actSpeed >= 0:
            # Make sure the backward pwm is stopped first
            self.backwardPWM.duty(0) 

            # Start the forward PWM
            self.forwardPWM.duty(self.Percent2Duty(self.actSpeed))

        if self.actSpeed < 0:
            # Make sure the forward pwm is stopped first
            self.forwardPWM.duty(0)

            # Start the backward PWM
            self.backwardPWM.duty(self.Percent2Duty(-self.actSpeed))


    def Stop(self,force_break=False):
        # Stop the motor 
        self.actSpeed = 0

        #Potentially set both pwm signals to 100% this to hold the motor in a stopped postion?
        if not force_break:
            self.forwardPWM.duty(0)
            self.backwardPWM.duty(0)
        else:
            self.forwardPWM.duty(1024)
            self.backwardPWM.duty(1024)

    def Percent2Duty(self,percent):
        return int(percent * 10.24)
