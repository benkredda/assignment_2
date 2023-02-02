#! /usr/bin/env python3 

import rospy
from geometry_msgs.msg import PoseStamped 
import actionlib.msg 
import assignment_2_2022.msg 
import actionlib
import rospy
from nav_msgs.msg import Odometry
from assignment_2.msg import custom
import os

#the start_description_flag is used for printing the description of the node once
start_description_flag=1

#target function
#is called when the user choses the operation 1,the user has to enter x and y positions of the target
#it creates a goal of type PoseStamped and sends it to the action server using the send_goal function 
#which is a member function of the SimpleActionClient class
#the goal is sent to the action server using the topic /reaching_goal and the action type PlanningAction

#target function 
def target():

    x_value = input("\nenter here X position : ")
    y_value = input("\nenter here Y position : ")

 
    x_position = int(x_value)
    y_position = int(y_value)
 
    
    print(f'\nYou have entered: \nposition X: {x_position}  \nposition Y: {y_position}')
    # to Create the SimpleActionClient specifying the type of the action

    print("\n----------------------------------------------")
    print("\nWaiting to connect to the action server")

    #we do this to Wait until the server receives goals 
    client.wait_for_server()

    #first Creates a goal to send to the action server.
    goal = PoseStamped()


    goal.pose.position.x = x_position
    goal.pose.position.y = y_position


    goal = assignment_2_2022.msg.PlanningGoal(goal)

    
    #Then Sends the goal to the action server.
    client.send_goal(goal)
    print("\nthe Goal is sent to the sever")
    input("\nPress Enter to choose an operation!")

    #go again to the interface function 
    interface()
      
#cancel function 
#is called when the user choses the operation 2,it cancels the goal that is sent to the action server using 
#the cancel_goal function which is a member function of the SimpleActionClient class

      
#cancel function
def cancel():
    #to Cancel the goal that is sent to the action server
    client.cancel_goal()
    print(f"\nGoal is canceled")
    input("\n\nPress Enter to choose an operation!")

    #Back to the interface function
    interface()

#wrong_input function is called when the user enters a wrong input ,after printing the  message it waits for 3 seconds

#wrong_input function
def wrong_input():

    print("No it's a wrong input !")
    rospy.sleep(3)
    #go back to interface
    interface()


#interface function is called to print the interface and let the user choose one operation among the three operations
#either entering 1 to choose positions of the target , or entering 2 to choose cancel operation , or 3 to exit
#there are functions for all of the three operations named target(),cancel(),and exit() respectively

#interface function
def interface():

    os.system('clear')   
    print("**         Robot's interface          **\n")
    print("1:positions of the target\n")
    print("2:Cancel\n")
    print("3:Exit\n")   

    #the user is supposed to choose an operation
    user_choice = input("Please choose your operation: ")
    
    #follow the choice of the user
    if   (user_choice == "1"):
        target()

    elif (user_choice == "2"):
        cancel() 

    elif (user_choice == "3"):
        exit()

    else:
        wrong_input()

#start_description function is called to print the description of the node by setting the start_description_flag to 0

def start_description(start_description_flag):
    if start_description_flag == 1:
        os.system('clear')
        print("\n\n------------------Node-a description------------------\n\n")
        print("an action client node ,allowing the user to set a target (x, y) ")
        print("or to cancel it")
        print("\n\n----------------------------------------------------\n\n")
        print("And publishes the robot position and velocity ")
        print("as a custom message (x,y, vel_x, vel_z), by relying ")
        print("on the values published on the topic /odom.")
        input("\n\nPress Enter to continue!")
        start_description_flag=0   

#callback function is called to print the message received from the topic /odom and fuction publishes the message received from the
#topic /odom as a custom message of type custom and is published on the topic /position_and_velocity

#callback function
def callback(data):
    
    my_publisher = rospy.Publisher('position_and_velocity', custom, queue_size=5)
    my_custom_message = custom()
    my_custom_message.x = data.pose.pose.position.x
    my_custom_message.y = data.pose.pose.position.y
    my_custom_message.vel_x = data.twist.twist.linear.x
    my_custom_message.vel_y = data.twist.twist.linear.y

    my_publisher.publish(my_custom_message)



if __name__ == '__main__':
    #start_description_flag is done for printing the description of the node once.
    start_description(start_description_flag)
    
    
    #initialize the node as Node_a
    rospy.init_node('Node_a')
    #Subscribe to the topic /odom then after the node was receiving a message
    #from the topic /odom the callback function will be called 
    rospy.Subscriber("/odom", Odometry, callback)

    #the SimpleActionClient is created specifying the type of the action
    client = actionlib.SimpleActionClient('/reaching_goal',assignment_2_2022.msg.PlanningAction )
    
    #Call the interface function to choose one of the three operations 
    interface()
    # spin() to not let python exit until this node is done
    rospy.spin()

