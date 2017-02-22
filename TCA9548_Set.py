#!/usr/bin/env python

# SDL_Pi_TCA9548.py Python Driver Code
# SwitchDoc Labs April 1, 2015	 
# V 1.2


#encoding: utf-8
 
from datetime import datetime
import smbus

# constants

#/*=========================================================================
#    I2C ADDRESS/BITS
#    -----------------------------------------------------------------------*/
TCA9548_ADDRESS =                         (0x70)    # 1110000 (A0+A1=VDD)
#/*=========================================================================*/

#/*=========================================================================
#    CONFIG REGISTER (R/W)
#    -----------------------------------------------------------------------*/
TCA9548_REG_CONFIG            =          (0x00)
#    /*---------------------------------------------------------------------*/

TCA9548_CONFIG_BUS0  =                (0x01)  # 1 = enable, 0 = disable 
TCA9548_CONFIG_BUS1  =                (0x02)  # 1 = enable, 0 = disable 
TCA9548_CONFIG_BUS2  =                (0x04)  # 1 = enable, 0 = disable 
TCA9548_CONFIG_BUS3  =                (0x08)  # 1 = enable, 0 = disable 

#/*=========================================================================*/


class TCA9548_Set():



    ###########################
    # TCA9548 Code
    ###########################
    def __init__(self, twi=1, addr=TCA9548_ADDRESS, bus_enable =  TCA9548_CONFIG_BUS0 ):
        self._bus = smbus.SMBus(twi)
        self._addr = addr
	config = bus_enable
  	self._write(TCA9548_REG_CONFIG, config)


    def _write(self, register, data):
        #print "addr =0x%x register = 0x%x data = 0x%x " % (self._addr, register, data)
        self._bus.write_byte_data(self._addr, register, data)


    def _read(self ):

        returndata = self._bus.read_byte(self._addr)
        #print "addr = 0x%x returndata = 0x%x " % (self._addr, returndata)
        return returndata



    # public functions

    def read_control_register(self):
	# Reads Control Register 

	value = self._read()
	return value

    def write_control_register(self, config):
	# Writes Control Register 

  	self._write(TCA9548_REG_CONFIG, config)



