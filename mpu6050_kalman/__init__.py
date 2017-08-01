import threading
from Kalman_py import Kalman_py
import math
from mpu6050 import mpu6050
from time import sleep,time


class mpu6050_kalman(threading.Thread):
    def init(self):
        threading.Thread.__init__(self)
        self.sensor = mpu6050(0x68)
        self.kalmanX = Kalman_py()
        self.kalmanY = Kalman_py()

        sleep(0.1)
        self.acc = self.sensor.get_accel_data()
        self.gyro = self.sensor.get_gyro_data()
        self.temp = self.sensor.get_temp()
        self.kalAngleX = 0.0
        self.kalAngleY = 0.0

        self.roll = math.degrees(math.atan2(self.acc['y'], self.acc['z']))
        self.pitch = math.degrees(math.atan(-self.acc['x'] / math.sqrt(self.acc['y'] ** 2 + self.acc['z'] ** 2)))

        self.kalmanX.setAngle(self.roll)
        self.kalmanY.setAngle(self.pitch)
        self.gyroXangle = self.roll
        self.gyroYangle = self.pitch
        self.compAngleX = self.roll
        self.compAngleY = self.pitch
        self.micros = lambda: int(time())
        self.timer = self.micros()
        self.t = self.micros()
    def run(self):
        while(1):
            self.acc = self.sensor.get_accel_data()
            self.gyro = self.sensor.get_gyro_data()
            self.temp = self.sensor.get_temp()
            self.dt = self.micros() - self.timer
            self.timer = self.micros()
            self.roll = math.degrees(math.atan2(self.acc['y'], self.acc['z']))
            self.pitch = math.degrees(math.atan(-self.acc['x'] / math.sqrt(self.acc['y'] ** 2 + self.acc['z'] ** 2)))

            self.gyroXrate = self.gyro['x'] / 131
            self.gyroYrate = self.gyro['y'] / 131

            if (self.roll < -90 and self.kalAngleX > 90) or (self.roll > 90 and self.kalAngleX < -90):
                self.KalmanX.setAngle(self.roll)
                self.compAngleX = self.roll
                self.kalAngleX = self.roll
                self.gyroXangle = self.roll
            else:
                self.kalAngleX = self.KalmanX.getAngle(self.roll, self.gyroXrate, self.dt)

            if abs(self.kalAngleX) > 90:
                self.gyroYrate = -self.gyroYrate

            self.kalAngleY = self.kalmanY.getAngle(self.pitch, self.gyroYrate, self.dt)

            self.gyroXangle += self.gyroXrate * self.dt
            self.gyroYangle += self.gyroYrate * self.dt
            self.compAngleX = 0.93 * (self.compAngleX + self.gyroXrate * self.dt) + 0.07 * self.roll
            self.compAngleY = 0.93 * (self.compAngleY + self.gyroYrate * self.dt) + 0.07 * self.pitch

            if self.gyroXangle < -180 or self.gyroXangle > 180:
                self.gyroXangle = self.kalAngleX
            if self.gyroYangle < -180 or self.gyroYangle > 180:
                self.gyroYangle = self.kalAngleY