"""
Program name: robot.py
Author:       Dr. Brewer
Initial Date: 20-Nov-2018 through 05-Dec-2018
Python vers:  3.6.5

Description:  A simple robot simulation environment.

Code vers:    1.0 - Initial release
"""
from typing import List,Any
import math
import random as r
import time

class Robot():
	"""
	This is the Robot class. It is the parent class for the
	individual student robot classes.

	Inherits:
		None

	Returns:
		None
	"""
	def __init__(self, s: str, d: float, x: float, y: float, xT: float, yT: float, color: List[int]) -> None:
		"""
		This is the constructor for the Robot class

		Args:
			s (String): the name for the robot (to be overridden by student class)
			d (float): the direction the robot is initially heading, in degrees
			x (float): the initial x coordinate location value
			y (float): the initial y coordinate location value
			xT (float): the target x coordinate location value
			yT (float): the target y coordinate location value
			color (List[int]): the red/green/blue color values (0-255) (to be overridden by student class)
		
		Returns:
			None
		"""
		self.memory = [] #to be defined by individual robots
		self.name = s #to be defined by the individual robot and used as an identifier
		
		self.locationHistory = [] #used for plotting 
		self.locationHistory.append([x,y])
		self.heading = math.radians(d) #the direction (radians) the robot is pointing
		self.__sensorReadings = [] #Forward,Right,Rear,Left
		self.rgb = color
		self.__v_Left = 0.0 #wheel velocity setting
		self.__v_Right = 0.0
		self.__x_Pos = x #where the robot is located 
		self.__y_Pos = y
		self.__xT_Pos = xT #where the target is located 
		self.__yT_Pos = yT
		self.__delta_Left = 0.0 #how much the wheels have turned since last step
		self.__delta_Right = 0.0
		self.__stillMoving = True
		self.MAX_WHEEL_V = 10.0
		self.__totalTime = 0.0

		#
#the following to be used only by the simulation and not overridden by the student robot class
#
	def set_wheel_deltas(self,l,r):
		"""
		This stores how much the wheels have turned since last step.

		Args:
			l (float): the left wheel movement
			r (float): the right wheel movement
		
		Returns:
			None
		"""
		self.__delta_Left = l
		self.__delta_Right = r
	
	def set_new_position(self,leftDelta,rightDelta):
		"""
		This calculates and stores the new robot position and 
		heading given the left and right wheel movement. See 
		comments for source of algorithm.

		Args:
			leftDelta (float): the left wheel movement
			rrightDelta (float): the right wheel movement
		
		Returns:
			None
		"""
	#below code from https://robotics.stackexchange.com/questions/1653/calculate-position-of-differential-drive-robot
	#also from: http://www8.cs.umu.se/research/ifor/IFORnav/reports/rapport_MartinL.pdf
	#leftDelta and rightDelta = distance that the left and right wheel have moved along the ground
	
		if (math.fabs(leftDelta - rightDelta) < 1.0e-6): #basically going straight
			new_x = self.__x_Pos + leftDelta * math.cos(self.heading)
			new_y = self.__y_Pos + rightDelta * math.sin(self.heading)
			new_heading = self.heading
		else:
			R = 1.0 * (rightDelta + leftDelta) / (2.0 * (leftDelta - rightDelta))
			wd = (leftDelta - rightDelta) / 1.0 #axis width

			new_x = self.__x_Pos + R * (math.sin(wd + self.heading) - math.sin(self.heading))
			new_y = self.__y_Pos - R * (math.cos(wd + self.heading) - math.cos(self.heading))
			new_heading = self.heading + wd
			
		self.__x_Pos = new_x
		self.__y_Pos = new_y
		self.locationHistory.append([new_x,new_y])
		self.heading = new_heading
		
	def get_wheel_vel(self):
		"""
		This returns the left and righ wheel velocity settings.

		Args:
			None
		
		Returns:
			(float): the left wheel velocity setting
			(float): the right wheel velocity setting
		"""
		return [ self.__v_Left, self.__v_Right ]

	def getColor(self):
		"""
		This returns the color setting of the robot.

		Args:
			None
		
		Returns:
			(List[int]): the red/green/blue color values
		"""
		return  self.rgb 

	def getTotalTime(self):
		"""
		This returns the total processing time the robot used.

		Args:
			None
		
		Returns:
			(float): the total processing time
		"""
		return  self.__totalTime 
		
	def move_robot(self,delta_t):
		"""
		This calculates the movement of the robot for a given
		delta time value.

		Args:
			delta_t (float): the time delta
		
		Returns:
			None
		"""
		#setup the movement
		if self.__stillMoving:
			#startTime = time.process_time_ns() #BEGIN TIMER  <-- for v 3.7 or later of python!
			startTime = time.process_time() #BEGIN TIMER
			self.robot_action() #used to call the child function to be programmed by students
			self.__totalTime += (time.process_time() - startTime) #END TIMER AND ADD TO STORE
			#now move the robot
			vl, vr = self.get_wheel_vel()
			dir = self.heading
			#now record the new position
			self.set_new_position(vl,vr)
			#now record the wheel turns
			self.set_wheel_deltas(vl,vr)
		
	def get_position(self) ->List[float]:
		"""
		This returns the current position of the robot.

		Args:
			None
		
		Returns:
			(List[float]): the x and y coordinates
		"""
		return [self.__x_Pos, self.__y_Pos]

	def get_heading_degrees(self) ->float:
		"""
		This returns the current heading of the robot.

		Args:
			None
		
		Returns:
			(float): the heading, in degrees
		"""
		return math.degrees(self.heading)

	def stillMoving(self) -> bool:
		"""
		This returns whether the robot is currently
		still able to move.

		Args:
			None
		
		Returns:
			(bool): True if still moving
		"""
		return self.__stillMoving
		
	def setMoving(self, m: bool) -> None:
		"""
		This sets whether the robot is still able
		to move.

		Args:
			m (bool): whether the robot can still move
		
		Returns:
			None
		"""
		self.__stillMoving = m

	def set_sensor_readings(self,st: List[float]) -> None:
		"""
		This sets the four sensor readings. If any of the 
		readings are greater than 15, they are set to 15.3.

		Args:
			st (List[float]): the four sensor values
				forward, right, rear, left
		
		Returns:
			None
		"""
		s = [15.3,15.3,15.3,15.3]
		if st[0] > 15.0: 
			s[0] = 15.3
		else:
			s[0] = st[0]
		if st[1] > 15.0: 
			s[1] = 15.3
		else:
			s[1] = st[1]
		if st[2] > 15.0: 
			s[2] = 15.3
		else:
			s[2] = st[2]
		if st[3] > 15.0: 
			s[3] = 15.3
		else:
			s[3] = st[3]
		self.__sensorReadings = s
		 
#
#the following to be used by the child object
#
	def set_robot_wheel_velocity(self, v_left: float, v_right:float) -> bool: 
		"""
		This sets the two wheel velocities. The success of setting velocity 
		is returned as true/false. Values to be set are rotations per time 
		interval of left and right wheels. (Robot turns by setting the left/right 
		velocities differently.) Allowed values are -10.0 thru 10.0, if values 
		are out of range, values default to zero and return value is false.
		One wheel rotation is one unit length.

		Args:
			v_left (float): the left wheel velocity
			v_right (float): the right wheel velocity
		
		Returns:
			(bool): the success of setting the velocities
		"""
		if(v_left >= -self.MAX_WHEEL_V and v_left <= self.MAX_WHEEL_V and v_right >= -self.MAX_WHEEL_V and v_right <= self.MAX_WHEEL_V):
			self.__v_Left = v_left
			self.__v_Right = v_right
			return True
		else:
			return False

	def get_robot_sensor_readings(self) -> List[float]: 
		"""
		This gets the sensor readings. Returns the 
		#list of four distances to obstacles: Forward,
		Right,Rear,Left. Maximum sensor reading is 15.0 
		length units.

		Args:
			None
		
		Returns:
			(List[float]): the sensor values
					forward, right, rear, left
		"""
		return self.__sensorReadings
		
	def get_robot_wheel_sensor_ticks(self) -> List[float]: 
		"""
		This returns list of left and right wheel rotations 
		during previous time interval.

		Args:
			None
		
		Returns:
			(List[float]): the left,right wheel rotations
		"""
		return [self.__delta_Left, self.__delta_Right]
		
	def get_robot_target(self) -> List[float]: 
		"""
		This calculates and returns list of degrees clockwise 
		from forward, and distance, to target.

		Args:
			None
		
		Returns:
			(List[float]): the direction (degrees),distance
		"""
		x_delta = (self.__xT_Pos - self.__x_Pos) 
		y_delta = (self.__yT_Pos - self.__y_Pos)
		target_dist = math.sqrt((y_delta*y_delta)+(x_delta*x_delta))
		target_angle = math.degrees(math.asin(abs(x_delta/target_dist)))
		if(x_delta > 0 and y_delta > 0): target_angle = 90. - target_angle
		if(x_delta > 0 and y_delta < 0): target_angle = -90. + target_angle
		if(x_delta < 0 and y_delta < 0): target_angle = -90. - target_angle
		if(x_delta < 0 and y_delta > 0): target_angle = 90. + target_angle
		target_angle -= math.degrees(self.heading)		
		while (target_angle > 180.):
			target_angle -= 360
		while (target_angle < -180.):
			target_angle += 360
		return target_angle,target_dist
	
	
#
#the following to be overridden by the child object
#
	def robot_action(self) -> None:
		"""
		This function is to be overridden by the student robot
		implementation.
		#The student robot only has access to 
			self.memory, 
			self.set_robot_wheel_velocity(),
			self.get_robot_target(),
			self.get_robot_wheel_sensor_ticks()
			self.get_robot_sensor_readings

		Args:
			None
		
		Returns:
			None
		"""
		self.set_robot_wheel_velocity(0.0,0.0)
		
