"""
Program name: target.py
Author:       Dr. Brewer
Initial Date: 20-Nov-2018 through 05-Dec-2018
Python vers:  3.6.5

Description:  A simple robot simulation environment.

Code vers:    1.0 - Initial release
"""
import PyQt5.QtCore  as QtCore


class Target:
	"""
	This is the Target class. It is a data
	structure for storing a point (Starting
	location or target point).

	Inherits:
		None

	Returns:
		None
	"""
	location = QtCore.QPoint(0,0)
	
	def __init__(self, x,y):
		"""
		This is the constructor for the Target class

		Args:
			x (float): the x coordinate value
			y (float): the y coordinate value
		
		Returns:
			None
		"""
		self.location = QtCore.QPoint(int(x),int(y))
		
	def getLocation(self):
		"""
		This returns the target location as x,y.

		Args:
			None
		
		Returns:
			(float): the x location coordinate value
			(float): the y location coordinate value
		"""
		return self.location.x(),self.location.y()
		
