#!/usr/bin/env python
# -*- coding: utf-8 -*-

#ROS Libraries
import rospy
import subprocess
from XXX.msg import Point
from sensor_msgs.msg import Joy

class Joystick_Object(object):
    def __init__(self):
        #Initialize rover stuff
        self.arm_pub = rospy.Publisher("leggy_arm", Point, queue_size=1)
        self.arm_msg = Point()

        self.joy_sub = rospy.Subscriber("joy", Joy, self.runLoop)

    def runLoop(self, data):

        #Get Joystick values
        y_left = data.axes[1]
        x_right = data.axes[3]

        #----------------------------------------------------------------------------------------------------
        #Rover Commands
        #----------------------------------------------------------------------------------------------------
        #Left and Right Sticks
        if (abs(y_left) >= 0.5 or abs(x_right) >= 0.5):

            #Check Spin and Go command
            if (abs(y_left) >= 0.5 and abs(x_right) >= 0.5):
            	#Forward Left
            	if (y_left > 0 and x_right > 0):
            		self.rover_msg.data = "GOSPD " + str(self.rover_spd_half) + " " + str(self.rover_spd) + "\r"
            	#Forward Right
            	elif (y_left > 0 and x_right < 0):
            		self.rover_msg.data = "GOSPD " + str(self.rover_spd) + " " + str(self.rover_spd_half) + "\r"
            	#Back Left
            	elif (y_left < 0 and x_right > 0):
            		self.rover_msg.data = "GOSPD -" + str(self.rover_spd_half) + " -" + str(self.rover_spd) + "\r"
            	#Back Right
            	else:
            		self.rover_msg.data = "GOSPD -" + str(self.rover_spd) + " -" + str(self.rover_spd_half) + "\r"

            #Check Spin command only
            elif (abs(y_left) <= 0.5 and abs(x_right) >= 0.5):
            	#Left
            	if (x_right > 0):
            		self.rover_msg.data = "GOSPD -" + str(self.rover_spd) + " " + str(self.rover_spd) + "\r"
                #Right
                else:
            		self.rover_msg.data = "GOSPD " + str(self.rover_spd) + " -" + str(self.rover_spd) + "\r"

            #Check Go command only
            else:
            	#Forward
            	if (y_left > 0):
            		self.rover_msg.data = "GOSPD " + str(self.rover_spd) + " " + str(self.rover_spd) + "\r"
                #Backward
                else:
            		self.rover_msg.data = "GOSPD -" + str(self.rover_spd) + " -" + str(self.rover_spd) + "\r"

        else:	
        	self.rover_msg.data = "GO 0 0\r"
            self.rover_pub.publish(self.rover_msg)
	
	if self.prev_rover_msg != self.rover_msg.data :
		self.rover_pub.publish(self.rover_msg)

	self.prev_rover_msg = self.rover_msg.data

#----------------------------------------------------------------------------------------------------
#Main Function start
#----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    rospy.init_node('joy2arm')
    joystick_control = Joystick_Object()
    rospy.spin()
