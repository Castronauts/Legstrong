#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Standard libraries
import sys
import pygame
import os
import time
import math
#ROS Libraries
import rospy
import subprocess
from std_msgs.msg import Float64, String, Int64
from geometry_msgs.msg import Point
from dynamixel_msgs.msg import JointState
from sensor_msgs.msg import Joy

class Joystick_Object(object):
    def __init__(self):
        #Initialize arm stuff
        self.arm_pub = rospy.Publisher('control_signal', Point, queue_size=10)
        self.arm_msg = Point()
        self.prev_arm_msg = Point()
        #Initialize gripper stuff
        self.gripper_pub = rospy.Publisher("/dual_gripper_controller/command", Float64, queue_size=10)
        rospy.Subscriber("/dual_gripper_controller/state", JointState, self.updateGripperLoad)
        self.gripper_msg = Float64()
        self.prev_gripper_msg = Float64()
        self.gripper_msg.data = 0.0
        self.gripper_pub.publish(self.gripper_msg)

        self.joy_sub = rospy.Subscriber("joy", Joy, self.runLoop)

    #----------------------------------------------------------------------------------------------------
    #Function Declarations
    #----------------------------------------------------------------------------------------------------

    def updateGripperLoad(self, msg):
        self.gripper_load = msg.load
        #print(self.gripper_load)

    def degreeHeading(self, x, y):
        #Convert to degree heading
        heading_degree = math.atan2((x), (y*-1.0)) #Flipped orientation

        if (heading_degree < 0.0):
            heading_degree += 2.0 * math.pi

        heading_degree *= 180.0 / math.pi

        final_degree = int(heading_degree)

        #Need 360 degree values 0...359
        if(final_degree > 359):
            final_degree = 359

        return final_degree

    def runLoop(self, data):

        #Get Joystick values
        x_right = data.axes[3]
        y_right = data.axes[4]

        #Get Button Values
        open_button = data.buttons[0] #A button
        close_button = data.buttons[1] #B button

        #Get bumper values
        arm_down = data.buttons[4] #Left bumper
        arm_up = data.buttons[5] #Right bumper

        #----------------------------------------------------------------------------------------------------
        #Arm Commands
        #----------------------------------------------------------------------------------------------------
        #Bumpers, No Triggers
        if (arm_up != 0.0 or arm_down != 0.0) and (abs(x_right) <= 0.5 and abs(y_right) <= 0.5):

            #Check only up
            if(arm_up != 0.0 and arm_down == 0.0):

                self.arm_msg.z = 1.0
                self.arm_msg.x = 0.0
                self.arm_msg.y = 0.0

            #Check only down
            elif(arm_down != 0.0 and arm_up == 0.0):

                self.arm_msg.z = -1.0
                self.arm_msg.x = 0.0
                self.arm_msg.y = 0.0

            else:
                self.arm_msg.z = 0.0
                self.arm_msg.x = 0.0
                self.arm_msg.y = 0.0

        #Check only joystick arm x and y
        elif ((abs(x_right) >= 0.5 or abs(y_right) >= 0.5) and (arm_up == 0.0 and arm_down == 0.0)):

            #Get heading
            final_degree = self.degreeHeading(x_right, y_right)

            #Check forward signal
            if ((final_degree > 315 and final_degree <=359) or (final_degree >= 0 and final_degree <= 45)):
                self.arm_msg.z = 0.0
                self.arm_msg.y = 1.0
                self.arm_msg.x = 0.0

            #Check right signal
            elif (final_degree > 45 and final_degree <= 135):
                self.arm_msg.z = 0.0
                self.arm_msg.y = 0.0
                self.arm_msg.x = 1.0

            #Check backward signal
            elif (final_degree > 135 and final_degree <= 225):
                self.arm_msg.z = 0.0
                self.arm_msg.y = -1.0
                self.arm_msg.x = 0.0

            #Check left signal
            elif (final_degree > 225 and final_degree <= 315):
                self.arm_msg.z = 0.0
                self.arm_msg.y = 0.0
                self.arm_msg.x = -1.0

            else:
                self.arm_msg.z = 0.0
                self.arm_msg.y = 0.0
                self.arm_msg.x = 0.0  

        else:
            self.arm_msg.z = 0.0
            self.arm_msg.x = 0.0
            self.arm_msg.y = 0.0



        #----------------------------------------------------------------------------------------------------
        #Gripper Commands
        #----------------------------------------------------------------------------------------------------
        #Check open close buttons
        if (open_button != 0.0 or close_button != 0.0):
            #Check open button only
            if (open_button != 0 and close_button == 0.0 and self.gripper_msg.data >= -0.4):
                self.gripper_msg.data = self.gripper_msg.data - 0.01

            #Check close button only
            elif (close_button != 0 and open_button == 0.0 and self.gripper_msg.data <= 0.65 and self.gripper_load > -0.15):
                self.gripper_msg.data = self.gripper_msg.data + 0.01

            else:
                self.arm_msg.z = 0.0
                self.arm_msg.x = 0.0
                self.arm_msg.y = 0.0

        if self.prev_arm_msg != self.arm_msg :
            self.arm_pub.publish(self.arm_msg)

        if self.prev_gripper_msg != self.gripper_msg :
            self.gripper_pub.publish(self.gripper_msg)
    
        self.prev_arm_msg = self.arm_msg
        self.prev_gripper_msg = self.gripper_msg


#----------------------------------------------------------------------------------------------------
#Main Function start
#----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    try:
        rospy.init_node('joy2arm')
        joystick_control = Joystick_Object()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
