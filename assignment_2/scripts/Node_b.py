#!/usr/bin/env python3

import rospy
from std_srvs.srv import Empty,EmptyResponse
import assignment_2_2022.msg
import os



#global variables
reached_goals = 0
canceled_goals = 0
sequence = 1 
start_description_flag = 1
print_flag = True

#callback function is called when the service is called to print the number of reached and canceled goals and returns an empty response
#and the sequence number of the service call which is a global variable
#the sequence number is used to know how many calls have been made 
def callback_service(req):
    global canceled_goals , reached_goals , sequence
    print("-------------------------------------")
    print(f"Sequence: {sequence}\nNumber of canceled goals: {canceled_goals}\nNumber of reached goals: {reached_goals}")
    print("-------------------------------------")
    sequence += 1
    return EmptyResponse()


#callback function is called when a message is received on the topic /reaching_goal/result which is of type PlanningAction/Result
#this function increments the global variables canceled_goals and reached_goals depending on the status message
#that can be an integer :
#2: canceled
#3: reached
def callback_subscriber(data):

    if data.status.status == 2:

        global canceled_goals
        canceled_goals += 1
    
    elif data.status.status == 3:

        global reached_goals
        reached_goals += 1

#start_description function is called to print the description of the node and waits for the user to press enter
#it also sets the start_description_flag to 0
def start_description(start_description_flag):
    if start_description_flag == 1:
        os.system('clear')
        print("\n\n------------------Node_b description------------------\n\n")
        print("This node is a service node that, when called,")
        print("prints the number of goals reached and canceled.")
        input("\n\nPress Enter to continue!")
        start_description_flag=0   



#main function
if __name__ == "__main__":

    #start_description_flag is done for printing the description of the node once.
    start_description(start_description_flag)

    #logwarn is used to print a message once and in the terminal
    rospy.logwarn("service started")

    #Initialize the node as Node_b
    rospy.init_node('Node_b')

    
    #subscribe to the topic /reaching_goal/result where PlanningAction/Result is the type of the message
    #the callback function is a callback_subscriber   
    rospy.Subscriber("/reaching_goal/result", assignment_2_2022.msg.PlanningActionResult, callback_subscriber)

    #create a service with name reach_cancel_goal and type Empty
    #the callback function is callback_service
    rospy.Service('reach_cancel_goal', Empty, callback_service)

    rate = rospy.Rate(1) # 1hz
    #the node is alive until the user presses ctrl+c
    while not rospy.is_shutdown():
        
        if print_flag== True:
            print("waiting for a client to call the service ...")   
            print_flag = not print_flag
        else:
            print("waiting for a client to call the service ..")
            print_flag = not print_flag
        
        rate.sleep()
