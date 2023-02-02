#!/usr/bin/env python3

import math
from assignment_2_2022.msg import odom_custom_msg
import rospy
import os

#global variables
start_description_flag=1
counter =0
temp_vel =0
avg_vel =0
des_pos_distance=0
sequence = 1




#callback function
#this function is called when a message is received on the topic /odom_custom where the type of the message is odom_custom_msg
#the function tends to compute the distance of the robot from the target and the average velocity of the robot depending on the 
#last 5 messages and then the result is printed
def callback_subscriber(data):

    #global variables
    global counter
    global temp_vel
    global avg_vel
    global des_pos_distance


    #the desired position is set in the launch file that we get it from the parameter server
    #and is used to compute the distance of the robot from the target
    #the x coordinate of the desired position is in the desired_pos_x variable
    #the y coordinate of the desired position is in the desired_pos_y variable
    des_pos_x = rospy.get_param("/des_pos_x")
    des_pos_y = rospy.get_param("/des_pos_y")

    #we want the current position of the robot
    cur_pos_x = data.x
    cur_pos_y = data.y

    #to compute the distance of the robot from the target
    des_pos_distance= math.sqrt(((des_pos_x - cur_pos_x)**2)+((des_pos_y - cur_pos_y)**2))


    #current velocity
    cur_vel_x = data.vel_x
    cur_vel_y = data.vel_y

    #to compute the current velocity of the robot
    cur_vel= math.sqrt(((cur_vel_x)**2)+((cur_vel_y)**2))


    #then the average velocity of the robot is computed using the last 5 messages
    #the result needs to be stored in the avg_vel variable
    if counter<5:

        temp_vel=temp_vel+cur_vel
        counter +=1

    elif counter==5:

        counter=0
        temp_vel /= 5
        avg_vel=temp_vel
        temp_vel=0


def start_description(start_description_flag):
    if start_description_flag == 1:
        os.system('clear')
        print("\n\n------------------Node_c description------------------\n\n")
        print("This node subscribes to the robot’s position and velocity (using the custom message) and prints the  ")
        print("distance of the robot from the target and the robot’s average velocity ")
        print("You can set the \"print_dist\" parameter in assignment_2 launch file")
        print(" to set how fast the node publishes the information.")
        
        input("\n\nPress Enter to continue!")
        start_description_flag=0   


   

#main function
if __name__ == "__main__":

    start_description(start_description_flag)
    rospy.logwarn("Node_c started")

    #Initialize the node as Node_c
    rospy.init_node('Node_c')

    #create a rate object using the parameter /print_dist
    #the parameter is used to set the rate at which the node publishes the information
    HZ=rospy.get_param("/print_dist")
    rate = rospy.Rate(HZ)

    #subscribe to the topic /odom_custom where the message is of type odom_custom_msg
    rospy.Subscriber("position_and_velocity", odom_custom_msg, callback_subscriber)

    #the node runs until it is shutdown it prints the sequence number, the data print_dist
    #it prints the distance of the robot from the target and the average velocity of the robot
    #then node sleeps for the time set in the rate object
    while not rospy.is_shutdown():
        print(f"Sequence: {sequence}")
        print(f"Data print distance : {HZ} HZ")        
        print(f"distance to target: {des_pos_distance : .3f}")
        print(f'Robot’s average velocity: {avg_vel: .3f}')
        print(f"---------------------------")
        sequence += 1
        rate.sleep()
