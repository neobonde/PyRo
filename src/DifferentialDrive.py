from SpeedMotor import SpeedMotor


class DifferentialDrive():
    def __init__(self,lPf,lPb,rPf,rPb):
        self.MotorLeft = SpeedMotor(lPf,lPb)
        self.MotorRight = SpeedMotor(rPf,rPb)

        self.joystickX = 0
        self.joystickY = 0

    def setInput(self, X,Y):
        self.joystickX = X
        self.joystickY = Y

        
        #TODO Change from 128 to 100 
        #TODO Add smoothing, maybe this should happen in the set function and not update?

        # CONFIG
        # - fPivYLimt  : The threshold at which the pivot action starts
        #                This threshold is measured in units on the Y-axis
        #                away from the X-axis (Y=0). A greater value will assign
        #                more of the joystick's range to pivot actions.
        #                Allowable range: (0..+127)
        fPivYLimit = 32
			

        nMotPremixL = 0
        nMotPremixR = 0
        nPivSpeed = 0 
        fPivScale = 0

        # if (nJoyY >= 0){
        if self.joystickY >= 0 :
        # Forward
            # nMotPremixL = (nJoyX>=0)? 127.0 : (127.0 + nJoyX);
            nMotPremixL = 100 if self.joystickX >= 0 else 100 + self.joystickX
            # nMotPremixR = (nJoyX>=0)? (127.0 - nJoyX) : 127.0;
            nMotPremixR = 100 - self.joystickX if self.joystickX >= 0 else 100
        else: 
        # Reverse
            # nMotPremixL = (nJoyX>=0)? (127.0 - nJoyX) : 127.0;
            nMotPremixL = 100 - self.joystickX if self.joystickX >= 0 else 100 
            # nMotPremixR = (nJoyX>=0)? 127.0 : (127.0 + nJoyX);
            nMotPremixR = 100 if self.joystickX >= 0 else 100 + self.joystickX

        # Scale Drive output due to Joystick Y input (throttle)
        # nMotPremixL = nMotPremixL * nJoyY/128.0;
        nMotPremixL = nMotPremixL * self.joystickY/100
        # nMotPremixR = nMotPremixR * nJoyY/128.0;
        nMotPremixR = nMotPremixR * self.joystickY/100


        # Now calculate pivot amount
        # - Strength of pivot (nPivSpeed) based on Joystick X input
        # - Blending of pivot vs drive (fPivScale) based on Joystick Y input
        # nPivSpeed = nJoyX;
        nPivSpeed = self.joystickX
        # fPivScale = (abs(nJoyY)>fPivYLimit)? 0.0 : (1.0 - abs(nJoyY)/fPivYLimit);
        fPivScale = 0.0 if (abs(self.joystickY)>fPivYLimit) else (1.0 - abs(self.joystickY)/fPivYLimit)

        # Calculate final mix of Drive and Pivot
        nMotMixL = (1.0-fPivScale)*nMotPremixL + fPivScale*( nPivSpeed)
        nMotMixR = (1.0-fPivScale)*nMotPremixR + fPivScale*(-nPivSpeed)


        self.MotorLeft.SetSpeed(nMotMixL)
        self.MotorRight.SetSpeed(nMotMixR)
    

    def Update(self):
        self.MotorLeft.Update()
        self.MotorRight.Update()





  