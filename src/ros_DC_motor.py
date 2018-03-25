#!/usr/bin/env python
"""
Created on Mon May 22 22:53:55 2017
TODO: make universal motor driver instead of relying on adafruit dc motor
@author: joell
"""
import rospy
rospy.loginfo("trying to import the twist message")
from geometry_msgs.msg import Twist
import math
import atexit
rospy.loginfo("trying to load motor hat stuff from adafruit")
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
rospy.loginfo("sucessfully loaded all of the adafruit libraries that I needed")

totalExit = False


def map(value,linput,uinput,loutput,uoutput):
    temp = ((value-linput)*(uoutput-loutput)/(uinput-linput)+loutput)
    if(temp>uoutput):
        temp = uoutput
    elif(temp<loutput):
        temp = loutput
    return temp

def ros_adjust_motors(new_message):
    global motors
    '''
    Vector3  linear
    x magnitude
    y
    z
    Vector3  angular
    x angle
    y
    z
    '''
    if new_message.linear.x > 0:
        for key in motors:
            motors[key].run(Adafruit_MotorHAT.FORWARD)
        adjustMotors(new_message.linear.x,new_message.angular.x)
    elif new_message.linear.x < 0:
        for key in motors:
            motors[key].run(Adafruit_MotorHAT.BACKWARD)
        adjustMotors(abs(new_message.linear.x),new_message.angular.x)
    else:
        adjustMotors(0,0)

def adjustMotors(mag,ang):
    global mh

#front left 2
#front right 4
#back left 1
#back right 3

    if(ang<0):
        mh.getMotor(1).setSpeed(int(mag-abs(ang)))
        mh.getMotor(2).setSpeed(int(mag-abs(ang)))
        mh.getMotor(3).setSpeed(int(mag))
        mh.getMotor(4).setSpeed(int(mag))
    else:
        mh.getMotor(1).setSpeed(int(mag))
        mh.getMotor(2).setSpeed(int(mag))
        mh.getMotor(3).setSpeed(int(mag-abs(ang)))
        mh.getMotor(4).setSpeed(int(mag-abs(ang)))


# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)


if(__name__=="__main__"):

    # create a default object, no changes to I2C address or frequency
    mh = Adafruit_MotorHAT(addr=0x60)
    atexit.register(turnOffMotors)
    motors = {"M1":mh.getMotor(1),"M2":mh.getMotor(2),"M3":mh.getMotor(3),"M4":mh.getMotor(4)}
    motorDirs = {"M1":0,"M2":0,"M3":0,"M4":0}
    for key in motors:
        motors[key].run(Adafruit_MotorHAT.FORWARD)
        motorDirs[key] = Adafruit_MotorHAT.FORWARD
    rospy.init_node('ada_motor_driver', anonymous=True)
    rospy.Subscriber("runt_rover/cmd_vel", Twist, ros_adjust_motors)
    rate = rospy.Rate(1)
    while not rospy.is_shutdown():
        rate.sleep()
    print "exiting safely"

    #while True:
    #    readStuff()
