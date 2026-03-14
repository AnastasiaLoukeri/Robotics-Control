#!/usr/bin/env python

import rospy 
import math
from assignment3.msg import Info
from std_msgs.msg import String

#Dimiourgia tou Publisher (kanei publish sto randomtopic)
pub = rospy.Publisher('random_topic',String,queue_size=10)
# arxikopoihsh twn global metavliton tou Info
static_x=0
static_y=0
static_z=100
min_dist=2

def callback(data):
    #opos kai ston dual node, xrisimolpoio tis global metablites
    global static_x, static_y,static_z,min_dist

    #anagnosi ton suntetagmenon apo to custom message gia to randomwalk
    curr_x=data.xyz_coordinates.x
    curr_y=data.xyz_coordinates.y
    curr_z=data.xyz_coordinates.z

    #Upologizo thn apostasi tou random walk point apo to static point
    distance=math.sqrt((curr_x-static_x)**2+(curr_y-static_y)**2+(curr_z-static_z)**2)
    #
    status_msg=String()
    if distance>min_dist:
        status_msg.data="warning"
        rospy.logwarn("Distance: %.2f WARNING",distance)
    else:
        status_msg.data="OK"
        rospy.loginfo("Distance: %.2f OK",distance)

def listener():
    global static_x,static_y,static_z,min_dist
    rospy.init_node('check_distance',anonymous=True)
    #  Parameter Server
    static_x = rospy.get_param('static_x', 0.0)
    static_y = rospy.get_param('static_y', 0.0)
    static_z = rospy.get_param('static_z', 100.0)
    min_dist = rospy.get_param('threshold', 2.0)
    rospy.loginfo("Check distance node started! Threshold is: %.2f", min_dist)
    
    # 
    sub = rospy.Subscriber('drone_location', Info, callback)
    
    
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass

    





