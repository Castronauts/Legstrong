#!/usr/bin/env python

from __future__ import division
from numpy import pi, sqrt
from std_msgs.msg import String
import sys
import time
import serial
import rospy

def callback(message):
	arduino_serial.write(message.data)
	rospy.loginfo(message.data)

def listener():
	rospy.init_node('drive_controller')	
	rospy.Subscriber("leggy_wheels", String, callback, queue_size=10)	
	rospy.spin()


if __name__ == '__main__':
	arduino_serial = serial.Serial("/dev/ttyACM0", baudrate = 19200, timeout=1, write_timeout=0)
	listener()
	
