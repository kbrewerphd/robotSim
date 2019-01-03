"""
Program name: point.py
Author:       Dr. Brewer
Initial Date: 20-Nov-2018 through 05-Dec-2018
Python vers:  3.6.5

Description:  A simple robot simulation environment.

Code vers:    1.0 - Initial release
"""
class Point:
	"""
	This is the Point class. It is a simple data
	structure for x,y coordinates.

	Inherits:
		None

	Returns:
		None
	"""
	def __init__(self,x,y):
		"""
		This is the constructor for the Point class

		Args:
			x (float): the x coordinate value
			y (float): the y coordinate value
		
		Returns:
			None
		"""
		self.x = x
		self.y = y
