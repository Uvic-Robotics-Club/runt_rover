#!/usr/bin/env python
"""
Created on Mon May 22 22:53:55 2017
TODO: make universal motor driver instead of relying on adafruit dc motor
@author: joell
"""
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy

def ros_adjust_motors(joy_message):
    '''
    TWIST BREAKDOWN
    Vector3  linear
    x magnitude
    y
    z
    Vector3  angular
    x angle
    y
    z

    Table of index number of /joy.buttons:
    Index : Button name on the actual controller
    0 : A
    1 : B
    2 : X
    3 : Y
    4 : LB
    5 : RB
    6 : back
    7 : start
    8 : power
    9 : Button stick left
    10 : Button stick right
    Table of index number of /joy.axis:
    Index : Axis name on the actual controller
    0 : Left/Right Axis stick left
    1 : Up/Down Axis stick left
    2 : LT
    3 : Left/Right Axis stick right
    4 : Up/Down Axis stick right
    5 : RT
    6 : cross key left/right
    7 : cross key up/down
    '''
    speed_multiplier = 255
    # LT and RT go from 1 (no press) to -1 (full press)
    # want LT to go backwards and RT to go forward
    speed = 0.5*(joy_message.axes[2]-1) + -0.5*(joy_message.axes[5]-1)

    # Left/Right goes from 1 (full left) to zero (no press) to -1 (full right)
    angle = joy_message.axes[0]*speed
    new_message = Twist()
    new_message.linear.x = speed*speed_multiplier
    new_message.angular.x = angle*speed_multiplier
    pub.publish(new_message)




if(__name__=="__main__"):
    rospy.init_node('joystic_to_twist', anonymous=True)
    rospy.Subscriber("joy",Joy, ros_adjust_motors)
    pub = rospy.Publisher("runt_rover/cmd_vel", Twist, queue_size=1)
    rate = rospy.Rate(1)
    rospy.loginfo("Starting up the Joystick node for the runt rover")
    while not rospy.is_shutdown():
        rate.sleep()
    print "exiting safely"
