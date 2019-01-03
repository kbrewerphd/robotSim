"""
Program name: shape.py
Author:       Dr. Brewer
Initial Date: 20-Nov-2018 through 05-Dec-2018
Python vers:  3.6.5

Description:  A simple robot simulation environment.

Code vers:    1.0 - Initial release
"""
import PyQt5.QtGui as QtGui
from PyQt5.QtWidgets import *
import PyQt5.QtCore  as QtCore


class Shape:
	"""
	This is the Shape class. It handles the data of the barriers.
	Each barrier is an instance of this class

	Inherits:
		None

	Returns:
		None
	"""
	StartPoint = QtCore.QPoint()
	EndPoint = QtCore.QPoint()
	Color = QtGui.QColor(100, 10, 10, 40)
	Brush = QtGui.QBrush(QtGui.QColor(100, 10, 10, 40)) 
	Pen = QtGui.QPen(QtGui.QColor(100, 10, 10, 40), 5, QtCore.Qt.SolidLine)
	RectType = True #FALSE if drawing a line
	
	#CONSTRUCTOR
	def __init__(self, st, ed, br, co, pn, tp):
		"""
		This is the constructor for the Shape class

		Args:
			st (Point): one corner of the barrier shape
			ed (Point): opposite corner of the barrier shape
			br (QBrush): the Brush for drawing the shape
			co (QColor): the Color for drawing the shape
			pn (QPen): the Pen for drawing the shape
			tp (bool): the barrier type NOT YET IMPLEMENTED
						True -- rectangle
		
		Returns:
			None
		"""
		self.StartPoint = st
		self.EndPoint = ed
		self.Brush = br
		self.Color = co
		self.Pen = pn
		self.RectType = True #tp not yet implemented
		
	def getXBounds(self):
		"""
		This returns the x bounding coordinates of the barrier.

		Args:
			None
		
		Returns:
			(float): an x coordinate value
			(float): another x coordinate value
		"""
		return self.StartPoint.x(),self.EndPoint.x()
		
	def getYBounds(self):
		"""
		This returns the y bounding coordinates of the barrier.

		Args:
			None
		
		Returns:
			(float): an y coordinate value
			(float): another y coordinate value
		"""
		return self.StartPoint.y(),self.EndPoint.y()
		
	def inShape(self,x,y):
		"""
		This returns True/False whether x,y point
		is within the barrier.

		Args:
			x (float): the x coordinate value
			y (float): the y coordinate value
		
		Returns:
			(bool): if in barrier or not
		"""
		x1 = self.StartPoint.x()
		y1 = self.StartPoint.y()
		x2 = self.EndPoint.x()
		y2 = self.EndPoint.y()
		if(x1 > x2):
			minX = x2
			maxX = x1
		else:
			minX = x1
			maxX = x2
		if(y1 > y2):
			minY = y2
			maxY = y1
		else:
			minY = y1
			maxY = y2
		if(x <= maxX and x >= minX and y <= maxY and y >= minY):
			result = True
		else:
			result = False
		return result

