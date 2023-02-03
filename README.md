# assignment_2 report
##general explanation of the assignment and its purpose
in this assignment i created three nodes Node_a ,Node_b, Node_cand each one has a different code and they are all found in a folder called scripts + another folder msg containing message file named custom.msg + launch folder containing launch file named assignment_2.launch .
##How the assignment works and what are the important commands to launch/run it:
there are some steps that need to be done before launching the package 
1. create a workspace 
2. source the workspace by editing the .bashrc 
3. go to src folder and clone the package given by the professor using the command git clone https://github.com/CarmineD8/assignment_2_2022 
4. again in the src folder clone my package assignment_2
5. run the command catkin_make in the terminal opened in workspace
6. run the command source ~/my_ros_ws/devel/setup.bash
7.to launch all the nodes and see the whole simulation run the command roslaunch assignment_2 assignment_2.launch
### Node_a :it implements an action client, allowing the user to set a target (x, y) or to cancel it.to do so i have created an interface where the user can choose one operation among the three operations and each operation is a function that can do the following tasks :
1. target() to allow the user set the positions x and y of the target , then create and send the goal to the action server using the planning action file found in the professor's package assignment_2_2022, the robot will move to reach the target .
2. cancel() to cancel the target , the robot will stop in the moment of canceling
3. exit() to exit 
the wrong_input() function is when the user enters a wrong input.
after each function the interface will appear again asking the user to select an operation
also the node publishes the robot position and velocity as a custom message (x,y, vel_x, vel_z), by relying on the values
published on the topic /odom. so at first the node subscribes in the topic /odom to get the data then publishes the robot's position and velocity as a custom message of type custom in the topic /position_and_velocity .
###Node_b : it is a service node that, when called, prints the number of goals reached and canceled; so first the node subscribes to the topic /reaching_goal/result and gets data and calls the callback_subscriber function when a message is received on the topic /reaching_goal/result which is of type PlanningAction/Result,this function increments the global variables canceled_goals and reached_goals depending on the status message that can be an integer : 2 canceled and 3 reached.
then a service is created and called to print the number of reached and canceled goals in the terminal.
###Node_c :the  node subscribes to the robot’s position and velocity (using the custom message)  which means it subscribes in the topic /odom_custom where the message is of type odom_custom_msg ,and prints the distance of the robot from the target and the robot’s average velocity. a parameter is used to set how fast the node publishes the information .
a launch file is created to start the whole simulation setting the value for the frequency at which Node_c publishes the information is set.