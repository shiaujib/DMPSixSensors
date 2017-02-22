#!/usr/bin/python

import smbus
import math
import time
import subprocess


# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
sensitive4g = 0x1c

class MPU6050Read():
    
    def __init__(self,address,bus=1):
        self._address=address
        self._bus=smbus.SMBus(bus)
        self._bus.write_byte_data(self._address, power_mgmt_1, 0)
        '''
        try:
            self._bus.write_byte_data(self._address, power_mgmt_1, 0)
        except IOError:
            subprocess.call(['i2cdetect','-y','1'])
        '''        

    def _read_byte(self,adr):
        return self._bus.read_byte_data(self._address, adr)


    def _read_word(self,adr):
        high = self._bus.read_byte_data(self._address, adr)
        low = self._bus.read_byte_data(self._address, adr+1)
        val = (high << 8) + low
        return val

    def read_word_2c(self,adr):
        val = self._read_word(adr)
        if (val >= 0x8000):               #MPU6050 16bits register data range +32768~-32768 value larger than 32768 transfer it to negative
            return -((65535 - val) + 1)
        else:
            return val
    def dist(a,b):
        return math.sqrt((a*a)+(b*b))

    def get_y_rotation(x,y,z):
        radians = math.atan2(x, dist(y,z))
        return -math.degrees(radians)

    def get_x_rotation(x,y,z):
        radians = math.atan2(y, dist(x,z))
        return math.degrees(radians)

    def print_value(gyro_xout,gyro_yout,gyro_zout,accel_xout,accel_yout,accel_zout):
        print "gyro_xout : ", gyro_xout, " scaled: ", (gyro_xout / 131)
        print "gyro_yout : ", gyro_yout, " scaled: ", (gyro_yout / 131)
        print "gyro_zout : ", gyro_zout, " scaled: ", (gyro_zout / 131)
        print "accel_xout: ", accel_xout, " scaled: ", accel_xout_scaled
        print "accel_yout: ", accel_yout, " scaled: ", accel_yout_scaled
        print "accel_zout: ", accel_zout, " scaled: ", accel_zout_scaled

