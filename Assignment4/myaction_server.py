#! /usr/bin/env python
# -*- coding: utf-8 -*-
import rospy

import time
import random
import actionlib
from assignment4_10975.msg import Asgn4Action, Asgn4Goal, Asgn4Result, Asgn4Feedback


def do_asgn4(goal): #will be invoked when we receive a new goal (line 55)
    
    start_time = time.time() # get the current time
    
    
    # We dont want this timer to be used for long waits
    if goal.time_t.to_sec() > goal.max_pause.to_sec(): 
        # in this case the goal is aborted (set_aborted() is called that
        # sends the message to the client 

        result = Asgn4Result()
        result.time_elapsed = rospy.Duration.from_sec(time.time() - start_time)
        

        # in the message to the client the result is included along with 
        # a string to help the client understand what happend
        result.message = "Aborted: The pause time (t) was too long."
        server.set_aborted(result, "ABORTION")
        return
    covered_distance=0.0

    # Were going to loop, sleeping in increments. This allows us to do things
    # while we’re working toward the goal, such as checking for preemption and providing
    # feedback
    while covered_distance < goal.total_distance:
        if server.is_preempt_requested():
            result = Asgn4Result()
            result.time_elapsed = rospy.Duration.from_sec(time.time() - start_time)
            
            server.set_preempted(result, "Timer preempted")            
            return
        
        # Movement of the UVG
        step=random.uniform(-2.0,6.0)
        covered_distance+=step
        remaining=goal.total_distance-covered_distance

        feedback = Asgn4Feedback()
        feedback.distance_remaining = remaining
        server.publish_feedback(feedback)
        
        rospy.sleep(goal.time_t.to_sec())

    result = Asgn4Result()
    result.time_elapsed = rospy.Duration.from_sec(time.time() - start_time)
    result.message = "Success! UGV reached the target."
    server.set_succeeded(result, "ΟΚ")

rospy.init_node('myaction_server')
rospy.loginfo("init node")

server = actionlib.SimpleActionServer('distance', Asgn4Action, do_asgn4, False)
rospy.loginfo("server")
server.start()
rospy.loginfo("server start")
rospy.spin()

