#!/usr/bin/env python
# -*- coding: utf-8 -*-

#ROS Libraries
import rospy
import subprocess
from std_msgs.msg import String
from sensor_msgs.msg import Joy

class Joystick_Object(object):
    def __init__(self):
        #Initialize rover stuff
        self.rover_pub = rospy.Publisher("leggy_wheels", String, queue_size=1)
        self.rover_msg = String()
        self.rover_msg.data = "RST\r"
        self.rover_pub.publish(self.rover_msg)
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
            		self.rover_msg.data = "GOSPD 15 30\r" #Only takes integers
            		self.rover_pub.publish(self.rover_msg)
            	#Forward Right
            	elif (y_left > 0 and x_right < 0):
            		self.rover_msg.data = "GOSPD 30 15\r" #Only takes integers
            		self.rover_pub.publish(self.rover_msg)
            	#Back Left
            	elif (y_left < 0 and x_right > 0):
            		self.rover_msg.data = "GOSPD -15 -30\r" #Only takes integers
            		self.rover_pub.publish(self.rover_msg)
            	#Back Right
            	else:
            		self.rover_msg.data = "GOSPD -30 -15\r" #Only takes integers
            		self.rover_pub.publish(self.rover_msg)

            #Check Spin command only
            elif (abs(y_left) <= 0.5 and abs(x_right) >= 0.5):
            	#Left
            	if (x_right > 0):
            		self.rover_msg.data = "GOSPD -30 30\r" #Only takes integers
                	self.rover_pub.publish(self.rover_msg)
                #Right
                else:
            		self.rover_msg.data = "GOSPD 30 -30\r" #Only takes integers
                	self.rover_pub.publish(self.rover_msg)   

            #Check Go command only
            else:
            	#Forward
            	if (y_left > 0):
            		self.rover_msg.data = "GOSPD 30 30\r" #Only takes integers
                	self.rover_pub.publish(self.rover_msg)
                #Backward
                else:
            		self.rover_msg.data = "GOSPD -30 -30\r" #Only takes integers
                	self.rover_pub.publish(self.rover_msg)   

        else:	
        	self.rover_msg.data = "GO 0 0\r"
    		self.rover_pub.publish(self.rover_msg)


#----------------------------------------------------------------------------------------------------
#Main Function start
#----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    rospy.init_node('joy_controller')
    joystick_controll = Joystick_Object()
    rospy.spin()