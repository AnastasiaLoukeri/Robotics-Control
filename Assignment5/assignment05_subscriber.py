#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from sensor_msgs.msg import Image, LaserScan
import cv2
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
 
THRESHOLD = 0.5  # metres
 
bridge = CvBridge()
too_close = False
min_distance = float('inf')
 
def scan_callback(msg):
    global too_close, min_distance
    ranges = np.array(msg.ranges)
    ranges = ranges[np.isfinite(ranges)]
    if len(ranges) > 0:
        min_distance = float(np.min(ranges))
        too_close = min_distance < THRESHOLD
 
def image_callback(msg):
    if not too_close:
        return
    try:
        img = bridge.imgmsg_to_cv2(msg, "bgr8")
 
        # Red banner at top
        cv2.rectangle(img, (0, 0), (img.shape[1], 50), (0, 0, 200), -1)
 
        # Distance text
        text = "Obstacle: {:.2f} m".format(min_distance)
        cv2.putText(img, text, (10, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
 
        cv2.imshow("Camera", img)
        cv2.waitKey(1)
    except CvBridgeError as e:
        rospy.logerr(e)
 
rospy.init_node("obstacle_camera_node", anonymous=True)
rospy.Subscriber("/scan", LaserScan, scan_callback)
rospy.Subscriber("/camera/rgb/image_raw", Image, image_callback)
rospy.spin()