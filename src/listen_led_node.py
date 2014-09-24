#!/usr/bin/env python

__author__ = 'mandeep'

import rospy
from std_msgs.msg import Bool
from ros_pololu_servo.msg import MotorCommand

class listen_led:
    channel_name="listen_led"
    def __init__(self):
        rospy.init_node("listen_led_node")
        self.pub=rospy.Publisher("/pololu/command",MotorCommand,queue_size=4)
        rospy.Subscriber("/pololu_trajectory",Bool, self.callback)

    def callback(self,msg):
        mtr=MotorCommand()
        if msg:
            mtr.position=0.77
            mtr.speed=1.0
            mtr.acceleration=1.0
        else:
            mtr.position=-0.77
            mtr.speed=0.0
            mtr.acceleration=0.0

        self.pub.publish(mtr)

if __name__ == '__main__':
    led=listen_led()
    rospy.spin()
