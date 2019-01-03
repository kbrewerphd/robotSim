"""
Author:       
Initial Date: 
Python vers:  3.6.5

Description:  A student robot.

Code vers:    1.0 - Initial release
"""

from typing import List,Any
import math
import random as r
from robot import Robot

class s1Robot(Robot):
	"""
	This is the s1Robot class - the first version of the student robot
	class. It inherits from the Robot class. It is the class that students 
	create their robots for the robotSim.py environment.

	Inherits:
		Robot: the complete robot description

	Returns:
		None
	"""
	def __init__(self, s: str, d: float, x: float, y: float, xT: float, yT: float, color: List[int]) -> None:
		"""
		The constructor for the s1Robot class.

		Args:
			s (string): default Robot name (overridden by this class)
			d (float): used by Robot class only
			x (int): used by Robot class only
			y (int): used by Robot class only
			xT (float): used by Robot class only
			yT (float): used by Robot class only
			color (List[int]): default Robot color (overridden by this class)
		
		Returns:
			None
		"""
		Robot.__init__(self,s, d, x, y, xT, yT, color)
		
		self.name = "Basic Robot" #to be defined by this class and used as an identifier
		self.rgb = [0,250,0]	#students can customize their color by specifying a list of ints instead of "color"
								# colors are 0-255 for [red, green, blue]
		self.memory = [] #to be defined and used by this class 
		
#the following to be defined by the individual robot
	def robot_action(self) -> None:
		"""
		The only function defined by this class. This function is called 
		each time the robot needs to move.

		Args:
			None
		
		Returns:
			None
		"""
		#The following describes the limits of each robot.
		#The robot has access to self.memory and the following functions: 
		#	self.set_robot_wheel_velocity(leftWheelVelocity: float, rightWheelVelocity: float) -> bool,
				#success of setting velocity is returned as true/false
				#values to be set are rotations per time interval of left and right wheels.
				#(you turn your robot by setting the left/right velocities differently)
				#allowed values are -10.0 thru 10.0
				#if values are out of range, values default to zero (i.e., no robot movement in the
				#subsequent time interval. The return value is false.
				#one wheel rotation is one domain unit length
		#	self.get_robot_target() -> List[float],
				#returns list of degrees clockwise from forward, and distance, to target.
		#	self.get_robot_wheel_sensor_ticks() -> List[float]
				#returns list of left and right wheel rotations during previous time interval.
		#	self.get_robot_sensor_readings() -> List[float] 
				#returns list of four distances to obstacles: Forward,Right,Rear,Left
				#maximum sensor reading is 15.0 length units.
				#any value at or above 15.0 length units is unreliable and should be ignored
		
		#the following is example code to "drive" the robot. 
		#Students should rewrite all of the following code
		
		sensors = self.get_robot_sensor_readings()
		angle, dist = self.get_robot_target()
		lv = 10.
		rv = 10.
		if(dist < 10): #close to target, so move slowly so as not to overshoot
			lv,rv = self.honeIn(sensors,angle,dist)
		elif min(sensors)< 5.0:  #barrier nearby!
			if sensors[0] < 5.0: #barrier ahead!
				if sensors[1] < 15.0:  #..rotate left
					mult = r.random() #add a random component to avoid persistent occilation
					lv = -0.05*mult
					rv = 0.05*mult
				else:  #..rotate right
					lv = 0.05
					rv = -0.05
			else: #  barrier not ahead, but one is close, so go slow
				lv = 1.0
				rv = 1.0
		else: #not close and no close barriers, 
			if(angle>10):  #..turn slightly right
				lv = 4.5
				rv = 4.3
			elif(angle<-10):  #..turn slighty left
				lv = 4.3
				rv = 4.5
			else:  #..go straight
				if sensors[0] > 10.0: #barrier far, go FAST
					lv = 9.0
					rv = 9.0
				else: #barrier close, go SLOW
					lv = 3.
					rv = 3.
		if not(self.set_robot_wheel_velocity(lv,rv)):
			self.set_robot_wheel_velocity(0.0,0.0) #something went wrong, so just don't move
		
	#end of robot_action() function
	
	#students can add their own functions that are called from within robot_action()
	def honeIn(self,s,a,d):
		if(abs(a)<90):
			if(a>0):  #..turn slightly right
				lvel = 0.5
				rvel = 0.48
			else:  #..turn slightly left
				lvel = 0.48
				rvel = 0.5
		else:  #..turn around
			lvel = 2.0
			rvel = 0.1
		return lvel,rvel

