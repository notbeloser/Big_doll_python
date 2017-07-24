import Adafruit_PCA9685
import math
eye_center=1500
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(100)
class eye:
    def __init__(self,channel_x,channel_y,r,angle,rev):
        self.channel_x=channel_x
        self.channel_y=channel_y
        self.r=r
        self.angle=angle
        self.rev=rev
    def set(self):
        if self.rev:
            x=self.r * math.cos(math.radians(self.angle))+1350
            y=self.r * math.sin(math.radians(self.angle)) * 1.2+eye_center-50
        else:
            x=self.r * math.cos(math.radians(self.angle))+1500
            y=(-self.r) * math.sin(math.radians(self.angle)) * 1.2+eye_center-130
        pwm.set_pwm(self.channel_y,0,int(y*0.4096))
        pwm.set_pwm(self.channel_x,0,int(x*0.4096))

class bow:
    def __init__(self,channel_angle,channel_y,angle,y,rev):
        self.channel_angle=channel_angle
        self.channel_y=channel_y
        self.angle=angle
        self.y=y
        self.rev=rev
    def set(self):
        if self.rev:
            duty=(1500-self.y * 50 / 3) * 0.4096
            angle_duty=(self.angle * 50 / 3+1500) * 0.4096
        
        else:
            duty=(self.y * 50 / 3+1500-60) * 0.4096
            angle_duty=(1500-(self.angle-6) * 50 / 3) * 0.4096

        pwm.set_pwm(self.channel_y,0,int(duty))
        pwm.set_pwm(self.channel_angle,0,int(angle_duty))

class ear:
    def __init__(self,channel,angle,rev):
        self.channel=channel
        self.angle=angle
        self.rev=rev
    def set(self):
        if self.rev:
            duty =  (1650-self.angle * 50 / 3) * 0.4096
        else:
            duty =  (1350+self.angle * 50 / 3) * 0.4096
        
        pwm.set_pwm(self.channel,0,int(duty))

class mouth:
    def __init__(self,side,rev,channel,angle):
        self.side=side
        self.rev=rev
        self.channel=channel
        self.angle=angle
    def set(self):
        if self.side != 1:
            duty = (1670-self.angle * 92 / 9) * 0.4096
        else:
            if self.rev:
                duty = (1400-self.angle * 92 / 9) * 0.4096
            else:
                duty = (1520+self.angle * 92 / 9) * 0.4096
        pwm.set_pwm(self.channel, 0, int(duty))

class doll:
    def __init__(self,l_eye=eye(0,1,0,0,0),r_eye=eye(2,3,0,0,1),
                 l_ear=ear(4,20,0),r_ear=ear(5,0,1),
                 l_bow=bow(6,7,0,0,1),r_bow=bow(8,9,0,0,0),
                 c_mouth=mouth(0,0,10,0),l_mouth=mouth(1,0,11,0),r_mouth=mouth(1,1,12,0)):
        self.l_eye=l_eye
        self.r_eye=r_eye
        self.l_ear=l_ear
        self.r_ear=r_ear
        self.l_bow=l_bow
        self.r_bow=r_bow
        self.c_mouth=c_mouth
        self.l_mouth=l_mouth
        self.r_mouth=r_mouth
    def set(self):
        self.l_eye.set()
        self.r_eye.set()
        self.l_ear.set()
        self.r_ear.set()
        self.l_bow.set()
        self.r_bow.set()
        self.c_mouth.set()
        self.l_mouth.set()
        self.r_mouth.set()
