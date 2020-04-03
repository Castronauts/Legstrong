#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Standard libraries
import sys
import os
import time
import math

#ROS Libraries
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Joy

class Joystick_Object(object):
    def __init__(self):
    	rospy.init_node('joy_controller')
        #Initialize rover stuff
        self.rover_pub = rospy.Publisher("leggy_wheels", String, queue_size=10)
        self.rover_msg = String()
        self.rover_speed = 30.0 #Out of 200 max , Was 20
        self.rover_speed_half = 15.0 #Out of 200 max , Was 20
        self.rover_msg.data = "rst\r"
        self.rover_pub.publish(self.rover_msg)
        #Rate for loop
        self.rate = rospy.Rate(10) #10 Hertz

    def runLoop(data):

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
            		self.rover_msg.data = "gospd " + str(int(self.rover_speed)) + " " + str(int(self.rover_speed_half)) + "\r" #Only takes integers
            		self.rover_pub.publish(self.rover_msg)
            	#Forward Right
            	elif (y_left > 0 and x_right < 0):
            		self.rover_msg.data = "gospd " + str(int(self.rover_speed_half)) + " " + str(int(self.rover_speed)) + "\r" #Only takes integers
            		self.rover_pub.publish(self.rover_msg)
            	#Back Left
            	elif (y_left < 0 and x_right > 0):
            		self.rover_msg.data = "gospd " + str(int(self.rover_speed_half * -1)) + " " + str(int(self.rover_speed * -1)) + "\r" #Only takes integers
            		self.rover_pub.publish(self.rover_msg)
            	#Back Right
            	else:
            		self.rover_msg.data = "gospd " + str(int(self.rover_speed * -1)) + " " + str(int(self.rover_speed_half * -1)) + "\r" #Only takes integers
            		self.rover_pub.publish(self.rover_msg)

            #Check Spin command only
            elif (abs(y_left) <= 0.5 and abs(x_right) >= 0.5):
            	#Left
            	if (x_right > 0):
            		self.rover_msg.data = "gospd " + str(int(self.rover_speed * -1)) + " " + str(int(self.rover_speed)) + "\r" #Only takes integers
                	self.rover_pub.publish(self.rover_msg)
                #Right
                else:
            		self.rover_msg.data = "gospd " + str(int(self.rover_speed)) + " " + str(int(self.rover_speed * -1)) + "\r" #Only takes integers
                	self.rover_pub.publish(self.rover_msg)   

            #Check Go command only
            else:
            	#Forward
            	if (y_left > 0):
            		self.rover_msg.data = "gospd " + str(int(self.rover_speed)) + " " + str(int(self.rover_speed)) + "\r" #Only takes integers
                	self.rover_pub.publish(self.rover_msg)
                #Backward
                else:
            		self.rover_msg.data = "gospd " + str(int(self.rover_speed * -1)) + " " + str(int(self.rover_speed * -1)) + "\r" #Only takes integers
                	self.rover_pub.publish(self.rover_msg)   
        	
        	rospy.sleep(0.1)

        else:	
        	self.rover_msg.data = "go 0 0\r"
    		self.rover_pub.publish(self.rover_msg)
    		rospy.sleep(0.1)

        #Final ROS sleep rate
        rospy.loginfo(self.rover_msg)
        self.rate.sleep()

    def start(data):
        #Initialize joystick
        rospy.Subscriber("joy", Joy, runLoop)
        rospy.spin()

#----------------------------------------------------------------------------------------------------
#Main Function start
#----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    try:
        joystick_controll = Joystick_Object()
        joystick_controll.start()

    except rospy.ROSInterruptException:
        pass