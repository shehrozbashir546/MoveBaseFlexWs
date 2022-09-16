#!/usr/bin/env python3


import actionlib
import rospy
import mbf_msgs.msg as mbf_msgs
import time

def create_goal(x, y, z, xx, yy, zz, ww):
    goal = mbf_msgs.MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    goal.target_pose.pose.position.z = z
    goal.target_pose.pose.orientation.x = xx
    goal.target_pose.pose.orientation.y = yy
    goal.target_pose.pose.orientation.z = zz
    goal.target_pose.pose.orientation.w = ww
    


    return goal


def move(goal):
    mbf_ac.send_goal(goal)
    mbf_ac.wait_for_result()
   
    return mbf_ac.get_result()


def drive_diag():
    goals = [   #Go in a diagonal line, i want to see it get there
                create_goal(-1.55, 1.71, 0, 0, 0, 0.0, 1.0),
                create_goal(1.55, -1.71, 0, 0, 0, 0.0, 1.0)
    ]

    for goal in goals:
        rospy.loginfo("Attempting to reach (%1.3f, %1.3f)", goal.target_pose.pose.position.x, goal.target_pose.pose.position.y)
        result = move(goal)

        if result.outcome != mbf_msgs.MoveBaseResult.SUCCESS:
            rospy.loginfo("Unable to complete action: %s", result.message)
            return 

if __name__ == '__main__':
    rospy.init_node("move_base_flex_client")

    # move_base_flex action client
    mbf_ac = actionlib.SimpleActionClient("move_base_flex/move_base", mbf_msgs.MoveBaseAction)
    mbf_ac.wait_for_server(rospy.Duration(10))
    rospy.loginfo("Connected! Diagonal Line Test initated!")
    startTime = time.time()
    drive_diag()
    endTime = time.time()
    totaltime = endTime - startTime
    print("Execution time in seconds: ", totaltime)

    rospy.on_shutdown(lambda: mbf_ac.cancel_all_goals())

