"""
Program name: robots.py
Author:       Dr. Brewer
Initial Date: 20-Nov-2018 through 05-Dec-2018
Python vers:  3.6.5

Description:  A simple robot simulation environment.

Code vers:    1.0 - Initial release
"""
import robot as rb
import sys
#import s1Robot as s1rb
import importlib.util

class Robots():
	"""
	This is the Robots class. It is a data
	structure for storing all Robot class instances.

	Inherits:
		None

	Returns:
		None
	"""
	__robotList = []
	
	def __init__(self):
		"""
		This is the constructor for the Robots class

		Args:
			None
		
		Returns:
			None
		"""
		self.__robotList = []

	def NumberOfRobots(self):
		"""
		This returns the number of Robots being stored.

		Args:
			None
		
		Returns:
			(int): the number of robot instances being stored
		"""
		return len(self.__robotList)
		
	def NewRobot(self,module,s,d,x,y,xT,yT,rgb): #Add robot
		"""
		This creates and adds a Robot instance to the Robots list.

		Args:
			module (String): the name of the Robot file
			s (String): the name of the robot
			d (int): the initial direction of the robot
			x (int): the initial x coordinate of the robot
			y (int): the initial y coordinate of the robot
			xT (int): the target x coordinate
			yT (int): the target y coordinate
			rbg (List[int]): the red,green,blue values (0-255) for the robot display
		
		Returns:
			None
		"""
		sys.path.insert(0, './studentRobots')
		mname = module[:-3]
		
		spec = importlib.util.find_spec(mname)
		if spec is None:
			print("can't find the module")
		else:
			# the actual import ...
			module = importlib.util.module_from_spec(spec)
			spec.loader.exec_module(module)
		print(mname,module)
		rbot = module.s1Robot(s,d,x,y,xT,yT,rgb)
		self.__robotList.append(rbot)
		
	def eraseAll(self): # remove all robots
		"""
		This resets the Robots list to empty.

		Args:
			None
		
		Returns:
			None
		"""
		self.__robotList = []
		
	def GetRobot(self, Index): # return requested robot
		"""
		This returns the Robot instance at Index location in the 
		robots list.

		Args:
			Index (int): the index value
		
		Returns:
			(Robot): the Robot instance at index Index
		"""
		return self.__robotList[Index]





