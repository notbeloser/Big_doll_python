from Kalman_py import Kalman_py
import math
from mpu6050 import mpu6050
from time import sleep,time



sensor = mpu6050(0x68)
kalmanX = Kalman_py()
kalmanY = Kalman_py()


sleep(0.1)
acc = sensor.get_accel_data()
gyro = sensor.get_gyro_data()
temp = sensor.get_temp()
kalAngleX = 0.0
kalAngleY = 0.0



roll = math.degrees(math.atan2(acc['y'], acc['z']))
pitch = math.degrees(math.atan(-acc['x'] / math.sqrt(acc['y']**2 + acc['z']**2)))

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
    roll = math.degrees(math.atan2(acc['y'], acc['z']))
    pitch = math.degrees(math.atan(-acc['x'] / math.sqrt(acc['y'] ** 2 + acc['z'] ** 2)))


    gyroXrate = gyro['x'] / 131
    gyroYrate = gyro['y'] / 131


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

    gyroXangle += gyroXrate * dt
    gyroYangle += gyroYrate * dt
    compAngleX = 0.93 * (compAngleX + gyroXrate * dt) + 0.07 * roll
    compAngleY = 0.93 * (compAngleY + gyroYrate * dt) + 0.07 * pitch

    if gyroXangle < -180 or gyroXangle > 180 :
        gyroXangle = kalAngleX
    if gyroYangle < -180 or gyroYangle > 180 :
        gyroYangle = kalAngleY

