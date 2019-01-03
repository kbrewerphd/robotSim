README file for Robot Simulation 

Author: Dr. Kevin Brewer
** Please send error reports to kbrewer@davidsonacademy.unr.edu **
Version: 1.0 (December 2018)
Python Version: 3.6.5

Purpose: This code creates an environment where simulated robots can
exist and navigate. It was designed for python programming students
to be able to create robot movement algorithms.

Installation:
(1) Unzip the files to a folder/directory.
(2) Ensure alll student robot files are in the studentRobots folder/directory.
(3) From a terminal window, start the simulation -- "python robotSim.py"
(4) Select the studentRobots folder/directory.

Files:
robotSim.py			The main program file.
  field.py			The simulation field class.
  myFrame.py		A customized QFrame pyqt5 widget.
  point.py			A simple x/y point class.
  readme.txt		This file.
  robot.py			The parent robot class.
  robotGUI.py		Contains the pyqt5 GUI description class.
  robots.py			A class to organize all robots in the simulation.
  shape.py			The barrier class.
  shapes.py			A class to organize all the barriers in the simulation.
  target.py			A class to contain the target and starting positions.
  
studentRobots		The directory where all student robot files reside
  __init__.py		A file to enable dynamic importing of the directory files
  s1Robot.py		An example student robot file.
  

Student Robot Files:
Each student robot file needs to have a unique file name.
Each student robot class needs to define the s1Robot class like that in the s1Robot.py file.

General Information:
The idea behind this simulation is to allow students to create virtual robots (algorithms) that independently move a "robot" from a starting location to a target location, while avoiding barriers and not going out of the simulated domain. The simulated environment will call the robot's move function which needs to be programmed by students to assess sensor information and determine left and right wheel velocities for the next "turn". 

o: Robots do not interact (nor see) other robots. 
o: The virtual domain is a two-dimensional rectangle with barriers that don't move. 
o: The starting and target locations are randomly chosen.
o: The starting direction for the robot is randomly chosen.
o: Directions are given in degrees clockwise from "east".
o: Sensors can only see a limited distance from the robot, and only in the four principle directions (front, right, rear, and left).
o: Robots can find direction (clockwise from robot forward direction) and distance to the target at each step.
o: Robots have memory capability, which can be programmed by the students.
o: Robots have a maximum wheel velocity for each turn.
o: Students can choose the name for their robot.
o: Students can choose the color for their robot.
o: Note that the simulated axle width is 1.

Student Robot Rules:
#Your robot objective is to get to the target as quick as possible without hitting 
#any obstacles. If your robot hits an obstacle, it is turned off.

#Your robot can interact with the simulated environment once per time interval.

#your robot can only "see" and act in the simulated environment using four functions:

#def set_robot_wheel_velocity(self, v_left: float, v_right:float) -> bool: 
    #success of setting velocity is returned as true/false
    #values to be set are rotations per time interval of left and right wheels.
    #(you turn your robot by setting the left/right velocities differently)
    #allowed values are -10.0 thru 10.0
    #if values are out of range, values default to zero and return value is false.
    #one wheel rotation is one unit length
    
#def get_robot_sensor_readings(self) -> List[float]: 
    #returns list of four distances to obstacles: Forward,Right,Rear,Left
    #maximum sensor reading is 15.0 length units. if nothing detected, reading > 15.0
    
#def get_robot_wheel_sensor_ticks(self) -> List[float]: 
    #list of left and right rotations during time interval since last set.
    
#def get_robot_target(self) -> List[float]: 
    #returns list of degrees clockwise from forward and distance, to target.
    
#To program a robot, modify the robot_action() function which will be called at each 
#time interval. All other function calls must occur in that one function.
#def robot_action(self) -> None:

#The only memory available to your robot is a single list called self.memory. 
#it is initialized as an empty list. 

#you may create additional functions that are used by your "robot_action" function.

#you may do as much processing as you wish during your "robot_action" function, but there
#is a penalty for robots who are computationally inefficient.
