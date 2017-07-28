from Kalman_py import Kalman_py
import math
import Doll
from mpu6050 import mpu6050
from time import sleep,time
import os


d = Doll.doll()
d.set()
sensor = mpu6050(0x68)

RESTRICT_PITCH = 1
kalmanX = Kalman_py()
kalmanY = Kalman_py()


sleep(0.1)
acc = sensor.get_accel_data()
gyro = sensor.get_gyro_data()
temp = sensor.get_temp()
kalAngleX = 0.0
kalAngleY = 0.0



if RESTRICT_PITCH == 1:
    roll = math.degrees(math.atan2(acc['y'], acc['z']))
    pitch = math.degrees(math.atan(-acc['x'] / math.sqrt(acc['y']**2 + acc['z']**2)))
else:
    roll=math.atan(acc['y']/math.sqrt(acc['x']**2 + acc['z']**2))
    pitch=math.atan2(-acc['x'],acc['z'])

kalmanX.setAngle(roll)
kalmanY.setAngle(pitch)
gyroXangle = roll
gyroYangle = pitch
compAngleX = roll
compAngleY = pitch
micros = lambda: int(time())
timer = micros()
t = micros()
while(1):
    acc = sensor.get_accel_data()
    gyro = sensor.get_gyro_data()
    temp = sensor.get_temp()
    dt = micros() - timer
    timer = micros()
    if RESTRICT_PITCH == 1:
        roll = math.degrees(math.atan2(acc['y'], acc['z']))
        pitch = math.degrees(math.atan(-acc['x'] / math.sqrt(acc['y'] ** 2 + acc['z'] ** 2)))
    else:
        roll = math.atan(acc['y'] / math.sqrt(acc['x'] ** 2 + acc['z'] ** 2))
        pitch = math.atan2(-acc['x'], acc['z'])

    gyroXrate = gyro['x'] / 131
    gyroYrate = gyro['y'] / 131

    if RESTRICT_PITCH == 1:
        if (roll < -90 and kalAngleX > 90) or (roll > 90 and kalAngleX < -90):
            kalmanX.setAngle(roll)
            compAngleX = roll
            kalAngleX = roll
            gyroXangle = roll
        else:
            kalAngleX = kalmanX.getAngle(roll, gyroXrate, dt)

        if abs(kalAngleX)>90:
            gyroYrate = -gyroYrate

        kalAngleY = kalmanY.getAngle(pitch, gyroYrate, dt)
    else:
        if (pitch < -90 and kalAngleY > 90) or (pitch > 90 and kalAngleY < -90):
            kalmanY.setAngle(pitch)
            compAngleY = pitch
            kalAngleY = pitch
            gyroYangle = pitch
        else:
            kalAngleY = kalmanY.getAngle(pitch, gyroYrate, dt)

        if abs(kalAngleY) > 90:
            gyroXrate = -gyroXrate
        kalAngleX = kalmanX.getAngle(roll, gyroXrate, dt)

    gyroXangle += gyroXrate * dt
    gyroYangle += gyroYrate * dt
    compAngleX = 0.93 * (compAngleX + gyroXrate * dt) + 0.07 * roll
    compAngleY = 0.93 * (compAngleY + gyroYrate * dt) + 0.07 * pitch

    if gyroXangle < -180 or gyroXangle > 180 :
        gyroXangle = kalAngleX
    if gyroYangle < -180 or gyroYangle > 180 :
        gyroYangle = kalAngleY

    os.system("clear")

    print("roll         %f"%roll)
    print("gyroXangle   %f"%gyroXangle)
    print("compAngleX   %f"%compAngleX)
    print("kalAngleX    %f"%kalAngleX)

    print("pitch        %f"%pitch)
    print("gyroYangle   %f"%gyroYangle)
    print("compAngleY   %f"%compAngleY)
    print("kalAngleY    %f"%kalAngleY)
    print("")
    # if (micros()-t) > 20*10**(-3):
    #     t=micros()
    #     if abs(roll)<30:
    #         d.l_ear.angle = roll
    #     if abs(pitch)<30:
    #         d.r_ear.angle = pitch
    #     d.set()
