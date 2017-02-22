#!/usr/bin/env python
#

from socket import *
import os
import struct
import sys,getopt
import time
import datetime
import random 
import TCA9548_Set
import MPU6050Read
import subprocess
import RPi.GPIO as GPIO
import threading
import numpy as np
import datetime
import time
import math
from pycomms import PyComms
import mpu6050
sensitive4g = 0x1c

#=========================================================================
# button control
GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.IN,pull_up_down=GPIO.PUD_UP)

#=========================================================================

#/*=========================================================================
#    I2C ADDRESS/BITS
#    -----------------------------------------------------------------------*/
TCA9548_ADDRESS =                         (0x70)    # 1110000 (A0+A1=VDD)

#/*=========================================================================*/

#/*=========================================================================
#    CONFIG REGISTER (R/W) ADDRESS WILL FOLLOW A READ/WRITE BIT
#    -----------------------------------------------------------------------*/
TCA9548_REG_CONFIG            =          (0x00)
#    /*---------------------------------------------------------------------*/

TCA9548_CONFIG_BUS0  =                (0x01)  # 1 = enable, 0 = disable 
TCA9548_CONFIG_BUS1  =                (0x02)  # 1 = enable, 0 = disable 
TCA9548_CONFIG_BUS2  =                (0x04)  # 1 = enable, 0 = disable 
TCA9548_CONFIG_BUS3  =                (0x08)  # 1 = enable, 0 = disable 
TCA9548_CONFIG_BUS4  =                (0x10)  # 1 = enable, 0 = disable 
TCA9548_CONFIG_BUS5  =                (0x20)  # 1 = enable, 0 = disable 
TCA9548_CONFIG_BUS6  =                (0x40)  # 1 = enable, 0 = disable 
TCA9548_CONFIG_BUS7  =                (0x80)  # 1 = enable, 0 = disable

BusChannel=[TCA9548_CONFIG_BUS0,TCA9548_CONFIG_BUS1,TCA9548_CONFIG_BUS2,
TCA9548_CONFIG_BUS3,TCA9548_CONFIG_BUS4,TCA9548_CONFIG_BUS5]



#BusChannel=[TCA9548_CONFIG_BUS0,TCA9548_CONFIG_BUS1,TCA9548_CONFIG_BUS2,
#TCA9548_CONFIG_BUS3,TCA9548_CONFIG_BUS4,TCA9548_CONFIG_BUS5,TCA9548_CONFIG_BUS6
#,TCA9548_CONFIG_BUS7]
#fileName=[subName+'sensor1.txt','sensor2.txt','sensor3.txt','sensor4.txt','sensor5.txt','sensor6.txt','sensor7.txt','sensor8.txt']

#accel=[[] for i in range(int(1))]  #create dynamic list
#gyro=[[] for i in range(int(1))]

timeArray=[None]*100000000
#/*=========================================================================*/

def findElement(list,key):
    for i in list:
        if i==key:
            return 1
    return 0


def writeFile(accel , gyro ,deviceNum,count):
    file0=open(fileName[0],'w')
    file1=open(fileName[1],'w')
    file2=open(fileName[2],'w')
    file3=open(fileName[3],'w')
    file4=open(fileName[4],'w')
    file5=open(fileName[5],'w')
    file6=open(fileName[6],'w')
    file7=open(fileName[7],'w')
    timeFile=open("dataTime.txt",'w')
    fileList=[file0,file1,file2,file3,file4,file5,file6,file7]
    for i in range (int(deviceNum)):
        for j in range(0,count*3,3):
            fileList[i].write("%f\t%f\t%f\n" %(accel[i][j],accel[i][j+1],accel[i][j+2]))
    for i in range(count):
    	timeFile.write("%s\n" %timeArray[i])
    print "Experimental done"
    for i in range(int(deviceNum)):
	fileList[i].close()
    timeFile.close()
    sys.exit(2)
            
            
            
        
    
    
# Main Program
def main(argv):
    try:
        opts,args=getopt.getopt(argv,"h:n:s:m:",["help=","deviceNumber"])
    except getopt.GetoptError:
        print 'usage:muti_accelerometer.py -n <deviceNumber> -s <subjectName> -m <mode>'
        sys.exit(2)
    if findElement(argv,'-n')==0:
        print 'usage:muti_accelerometer.py -n <deviceNumber> -s <subjectName> -m <mode>'
        sys.exit(2)
    if findElement(argv,'-s')==0:
        print 'usage:muti_accelerometer.py -n <deviceNumber> -s <subjectName> -m <mode>'
        sys.exit(2)
    if findElement(argv,'-m')==0:
        print 'usage:muti_accelerometer.py -n <deviceNumber> -s <subjectName> -m <mode>'
        sys.exit(2)
    for opt,arg in opts:
        if opts=='-h':
            print 'usage:muti_accelerometer.py -n <deviceNumber> -s <subjectName> -m <mode>'
        elif opt in ("-n","--deviceNumber"):
            deviceNum=arg
	elif opt in ("-s","--subjectName"):
            subName=arg
	elif opt in ("-m","--mode"):
            tmpm=arg
            mode=int(tmpm)
    
    accel=[[] for i in range(int(deviceNum))]  #create dynamic list
    gyro=[[] for i in range(int(deviceNum))]
    fileName=[subName+'_sensor1.txt',subName+'_sensor2.txt',subName+'_sensor3.txt',subName+'_sensor4.txt',subName+'_sensor5.txt',subName+'_sensor6.txt',subName+'_sensor7.txt',subName+'_sensor8.txt',subName+'_sensor9.txt',
subName+'_sensor10.txt',subName+'_sensor11.txt',subName+'_sensor12.txt',subName+'_sensor13.txt']
    
    print ""
    print "Sample uses 0x70" 
    print "Program Started at:"+ time.strftime("%Y-%m-%d %H:%M:%S")
    print ""
    #mode=raw_input("Please enter the mode you want")
    starttime = datetime.datetime.utcnow()
    startflag=0


    tca9548 = TCA9548_Set.TCA9548_Set(addr=TCA9548_ADDRESS, bus_enable = TCA9548_CONFIG_BUS1)

    file0=open(fileName[0],'w')
    file1=open(fileName[1],'w')
    file2=open(fileName[2],'w')
    file3=open(fileName[3],'w')
    file4=open(fileName[4],'w')
    file5=open(fileName[5],'w')
    fileList=[file0,file1,file2,file3,file4,file5]
        

    # rotates through all 4 I2C buses and prints out what is available on each
    accel_tmp=[0]*int(deviceNum)
    count=0
    flag=0
    addr = ('192.168.43.221',8000)
    bufsize = 1024
    filename = 'sensor1.txt'
    if mode==1:
        sendsock = socket(AF_INET,SOCK_STREAM)
        sendsock.bind(addr)
        sendsock.listen(5)
        print "waiting for client connect"
        conn,addr = sendsock.accept()
        print "server already connect client...->",addr
    while True:
        fflag=0
        fileIndex=0
        input_state=GPIO.input(4)   #get switch state
	if flag==0:
	    print "System initialize........"
	    flag+=1
        for channel in BusChannel:
#	    print channel
            if startflag==0 and count>1:
	        print "start getting data press button to stop"
                startflag=1
                start=time.time()
   	    mpu6050 = mpu6050.MPU6050(0x68)
            tca9548.write_control_register(BusChannel[fileIndex])
            mpu6050.dmpInitialize()
            mpu6050.setDMPEnable(True)
            mpuIntStatus=mpu6050.getIntStatus()
            packetSize=mpu6050.dmpGetFIFOPacketSize()
            if mpuIntStatus>=2:
                fifoCount=mpu6050.getFIFOCount()
                if fifoCount==1024:
                    mpu.resetFIFO()
                fifoCount=mpu6050.getFIFOCount()
                while fifoCount<packetSize:
                    fifoCount=mpu6050.getFIFOCount()
                
                result=mpu6050.getFIFOBytes(packetSize)
                #get quaternion
                q=mpu.dmpGetQuaternion(result)
                x="{0:.6f}".format(q['x'])
                y="{0:.6f}".format(q['y'])
                z="{0:.6f}".format(q['z'])
                w="{0:.6f}".format(q['w'])
                fifoCount-=packetSize
                
	    #print "-----------------BUS"+str(fileIndex)+"-------------"
            #get gyro and accelerometer value
            gyro_xout = mpu6050.read_word_2c(0x43)
            gyro_yout = mpu6050.read_word_2c(0x45)
            gyro_zout = mpu6050.read_word_2c(0x47)
            accel_xout = mpu6050.read_word_2c(0x3b)
            accel_yout = mpu6050.read_word_2c(0x3d)
            accel_zout = mpu6050.read_word_2c(0x3f)
            accel_xout=accel_xout/16384.0
            accel_yout=accel_yout/16384.0
            accel_zout=accel_zout/16384.0
            gyro_xout=gyro_xout/131.0
            gyro_yout=gyro_yout/131.0
            gyro_zout=gyro_zout/131.0
            if mode==0 and count>1:
                end=time.time()
                realtime=end-start
                if realtime<0:
                    realtime=0
                fileList[fileIndex].write("%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\n" %(accel_xout,accel_yout,accel_zout,gyro_xout,gyro_yout,gyro_zout,x,y,z,w,realtime))
            elif mode==1:
                val=math.sqrt(math.pow(int(accel_xout),2)+math.pow(int(accel_yout),2)+math.pow(int(accel_zout),2))
                val=int(val)
                val=round(val,4)
                conn.send("%5s"%(str(val)))
	    #conn.send("%2s\t%5s\t%5s\t%5s"%(str(fileIndex),str(accel_xout),str(accel_yout),str(accel_zout)))
            #print "accelx = %f accely = %f accelz = %f\n" %(accel_xout,accel_yout,accel_zout)
	    '''
            if fileIndex==0 or fileIndex==1 or fileIndex==2 or fileIndex==3 or fileIndex==7:
 	        mpu6050_sla=MPU6050Read.MPU6050Read(0x69,1)
                gyro_xout = mpu6050_sla.read_word_2c(0x43)
                gyro_yout = mpu6050_sla.read_word_2c(0x45)
                gyro_zout = mpu6050_sla.read_word_2c(0x47)
                accel_xout = mpu6050_sla.read_word_2c(0x3b)
                accel_yout = mpu6050_sla.read_word_2c(0x3d)
                accel_zout = mpu6050_sla.read_word_2c(0x3f)
                accel_xout=accel_xout/16384.0
                accel_yout=accel_yout/16384.0
                accel_zout=accel_zout/16384.0
                gyro_xout=gyro_xout/131.0
                gyro_yout=gyro_yout/131.0
                gyro_zout=gyro_zout/131.0
                if mode==0 and fileIndex==7:
                    end=time.time()
                    realtime=end-start
                    fileList[fileIndex+5].write("%f\t%f\t%f\t%f\t%f\t%f\t%f\n" %(accel_xout,accel_yout,accel_zout,gyro_xout,gyro_yout,gyro_zout,realtime))
                elif mode==0:
                    end=time.time()
                    realtime=end-start
                    fileList[fileIndex+8].write("%f\t%f\t%f\t%f\t%f\t%f\t%f\n" %(accel_xout,accel_yout,accel_zout,gyro_xout,gyro_yout,gyro_zout,realtime))
                if mode==1:
                    val=math.sqrt(math.pow(int(accel_xout),2)+math.pow(int(accel_yout),2)+math.pow(int(accel_zout),2))
                    val=int(val)
                    val=round(val,4)
                    conn.send("%5s"%(str(val)))
            '''
	    #timeTmp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    	    #timeFile.write("%s\n" %(timeTmp))
	    #timeArray[count]=timeTmp 
            fileIndex+=1
            '''
            if fileIndex>int(deviceNum):
		fileIndex=0
                break
            '''
        '''
        for i in range(int(deviceNum)):
            conn.send("%5s" %(accel_tmp[i]))
        '''
        count+=1

        '''
        if input_state==False:
            print "Button Pressed experimental stop"
            print "count Num = %d" %count
            if mode==1:
                sendsock.close()
                conn.close()
                print "Close socket"
            sys.exit()
            break
        ''' 
    #writeFile(accel,gyro,deviceNum,count)
        



if __name__=="__main__":
    sub_name=None
    main(sys.argv[1:])
        


