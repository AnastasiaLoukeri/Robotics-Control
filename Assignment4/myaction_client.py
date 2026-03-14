#! /usr/bin/env python
import rospy

import time
import actionlib
from assignment4_10975.msg import Asgn4Action, Asgn4Goal, Asgn4Result, Asgn4Feedback

def feedback_cb(feedback):
    print('[Feedback] Distance remaining: %f'%(feedback.distance_remaining))

# initalize the node
rospy.init_node('myaction_client')

# creation of a SimpleActionClient
# (action server name, type of action)
client = actionlib.SimpleActionClient('distance', Asgn4Action)

# wait for the action server to come up 
client.wait_for_server()

# create the goal and set the the amount of time we want the timer to wait
goal = Asgn4Goal()
goal.total_distance = 50.0
goal.time_t=rospy.Duration.from_sec(1.0)
goal.max_pause = rospy.Duration.from_sec(5.0)

# Uncomment this line to test server-side abort:
# goal.time_to_wait = rospy.Duration.from_sec(500.0)
client.send_goal(goal, feedback_cb=feedback_cb)
# Uncomment these lines to test goal preemption:
# time.sleep(3.0)
# client.cancel_goal()

# get (after 5 seconds) the result and then print it
client.wait_for_result()
print('[Result] State: %d'%(client.get_state()))
print('[Result] Status: %s'%(client.get_goal_status_text()))
print('[Result] Time elapsed: %f'%(client.get_result().time_elapsed.to_sec()))
print('[Result] Message: %s' % (client.get_result().message))