"""
Program name: myFrame.py
Author:       Dr. Brewer
Initial Date: 20-Nov-2018 through 05-Dec-2018
Python vers:  3.6.5

Description:  A simple robot simulation environment.

Code vers:    1.0 - Initial release
"""
import PyQt5.QtGui as QtGui
from PyQt5.QtWidgets import *
import PyQt5.QtCore  as QtCore
import field as fld
import target as tgt
import robots as rbs
import robot as rb
#import s1Robot as s1r
import random as r
import math
import importlib
import os
#import robots as rbs

class MyFrame(QFrame):
	"""
	This is the MyFrame class. It replaces the Designer generated 
	frame widget. It handles the display of the simulation.

	Inherits:
		QFrame: PyQt5 Frame Widget

	Returns:
		None
	"""
	def __init__(self,x) -> None:
		"""
		This is the constructor for the MyFrame class

		Args:
			Standard
		
		Returns:
			None
		"""
		super().__init__(x)
		
		self.TEST = False
		self.plotSensors = False
		
		directoryName = str(QFileDialog.getExistingDirectory(self, "Select Directory with Robot classes:"))
		self.directory = os.fsencode(directoryName)

			
		self.fw = self.frameRect().width()
		self.fh = self.frameRect().height()
		#print("Pre field initialization")
		self.field = fld.Field(100,100,10)
		self.robots = rbs.Robots()
		print("Done initializing frame")

	def createField(self,x,y,n):
		"""
		A function that is called when the field needs to be (re)created.

		Args:
			x (int): not used
			y (int): not used
			n (int): number of barriers
		
		Returns:
			None
		"""
		self.numBarriers = n
		self.fw = self.frameRect().width()
		self.fh = self.frameRect().height()
		#print("myFrame width, height ::",self.fw, self.fh)
		self.field = fld.Field(self.fw,self.fh,self.numBarriers)
		#print("Done initializing field")	
		self.robots = rbs.Robots()
		#print("Created robots class")
		
		
		
		#add robots
		names = ["Alpha","Beta","Gamma","Delta","Epsilon","Zeta","Eta","Theta",
				"Iota","Kappa","Lambda","Mu","nu","Xi","Omicron","Pi","Rho","Sigma","Tau","Upsilon",
				"Phi","Chi","Psi","Omega"]
				
		loc = self.field.getStartLocation()
		locT = self.field.getTargetLocation()
		
		if self.TEST:
			dir = 0
			rgb = [50,50,50]
			self.robots.NewRobot(names[0],dir,loc[0],loc[1],locT[0],locT[1],rgb)
		
		else:

			dir = float(r.randint(0,360))  #start all robots the same direction
			for file in os.listdir(self.directory):
				filename = os.fsdecode(file)
				if filename.endswith(".py"): 
					if not filename.endswith("__.py"):
						# print(os.path.join(directory, filename))
						#importlib.import_module(filename)
						print("Creating student robot...")
						rgb = [r.randint(50,250),r.randint(50,250),r.randint(50,250)]
						#dir = float(r.randint(0,360)) #comment this line out to have all robots start similar
						self.robots.NewRobot(filename,"dummyName",dir,loc[0],loc[1],locT[0],locT[1],rgb)
						continue
				else:
					continue
										


	def paintEvent(self, event): 
		"""
		A function that is automatically called when the frame needs 
		to be updated (repainted).

		Args:
			standard
		
		Returns:
			None
		"""
		qp = QtGui.QPainter(self)

		#draw border around field		
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0)) 
		pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 100), 3, QtCore.Qt.SolidLine)
		qp.setPen(pen)
		qp.setBrush(brush)
		qp.drawRect(QtCore.QRect(QtCore.QPoint(2,2), QtCore.QPoint(self.fw-3,self.fh-3)))
		
		#draw barriers (shapes)
		ds = self.field.getShapes()
		totShapes = ds.NumberOfShapes()
		try:
			for i in range(totShapes):
				s = ds.GetShape(i)
				qp.setPen(s.Pen)
				qp.setBrush(s.Brush)
				if s.RectType:
					tl = QtCore.QPoint(s.StartPoint.x(),s.StartPoint.y ())
					br = QtCore.QPoint(s.EndPoint.x(),s.EndPoint.y())
					qp.drawRect(QtCore.QRect(tl, br))
				else:
					pass
		except:
			print("barriers oops!")
			pass	

		#draw target
		try:
			#plot target
			brush = QtGui.QBrush(QtGui.QColor(10, 255, 10, 100)) 
			pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 100), 2, QtCore.Qt.SolidLine)
			qp.setPen(pen)
			qp.setBrush(brush)
			loc = self.field.getTargetLocation()
			#print("Drawing target at: ",loc[0],loc[1])
			qp.drawEllipse(QtCore.QPoint(loc[0],loc[1]),4,4)
			#print("Target")
		except:
			print("target oops!")
			pass
			
		#draw start Point
		try:
			brush = QtGui.QBrush(QtGui.QColor(255, 10, 10, 100)) 
			pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 100), 2, QtCore.Qt.SolidLine)
			qp.setPen(pen)
			qp.setBrush(brush)
			loc = self.field.getStartLocation()
			#print("Drawing target at: ",loc[0],loc[1])
			qp.drawEllipse(QtCore.QPoint(loc[0],loc[1]),4,4)
			#print("Target")
		except:
			print("start point oops!")
			pass
			
		#draw robots
		try:
			#print("pre list of robots")
			for i in range(self.robots.NumberOfRobots()):
				#print("drawing robot",i)
				robot = self.robots.GetRobot(i)
				#print("Got robot",i)
				rgb = robot.getColor()
				#print(rgb)
				rgbColor = QtGui.QColor(rgb[0],rgb[1],rgb[2])
				#print(rgb)
				brush = QtGui.QBrush(rgbColor) 
				pen = QtGui.QPen(rgbColor, 2, QtCore.Qt.SolidLine)
				#print("Ready to plot")
				x,y = robot.get_position()
				dir = robot.get_heading_degrees()
				self.plotRobot(qp,pen,brush,dir,x,y)
				paths = robot.locationHistory
				if(len(paths) > 1):
					for i in range(1,len(paths)):
						stPoint = paths[i-1]
						#print(stPoint)
						endPoint = paths[i]
						#print("Path points:",stPoint[0],stPoint[1],"::",endPoint[0],endPoint[1])
						qp.drawLine(QtCore.QPoint(stPoint[0],stPoint[1]),QtCore.QPoint(endPoint[0],endPoint[1]))

				if self.plotSensors:
					sensorPoints = robot.get_robot_sensor_readings()
					rgbColor = QtGui.QColor(100,100,100)
					brush = QtGui.QBrush(rgbColor) 
					pen = QtGui.QPen(rgbColor, 2, QtCore.Qt.SolidLine)
					qp.setPen(pen)
					qp.setBrush(brush)
					for i in range(4):
						#print(i,dir,x,y,sensorPoints[i])
						endX = x + math.cos(math.radians(dir + i*90.))*sensorPoints[i]
						endY = y + math.sin(math.radians(dir + i*90.))*sensorPoints[i]
						#print("sensor ends:",endX,endY)
						qp.drawLine(QtCore.QPoint(x,y),QtCore.QPoint(endX,endY))




		except:
			print("robot oops!")

	def plotRobot(self,qp,pen,brush,dir,x,y):
		"""
		A function that draws the robot.

		Args:
			qp (QPainter): the PyQt5 painter object
			pen (QPen): the PyQt5 pen object
			brush (QBrush): the PyQt5 brush object
			dir (float): the robot heading in degrees
			x (float): the robot x location
			y (float): the robot y location
		
		Returns:
			None
		"""
		qp.setPen(pen)
		qp.setBrush(brush)
		poly = self.createPoly(dir,x,y)
		#qp.drawPolygon(poly)
		qp.drawEllipse(QtCore.QPoint(x,y),2,2)


	def createPoly(self, d, x, y):
		"""
		A function that creates QPolygonF object to
		represent the robot location and direction
		it is pointing. Generates a triangle.

		Args:
			d (float): heading in degrees
			x (float): x location
			y (float): y location
		
		Returns:
			QPolygonF
		"""
		r = math.radians(d)
	
		triangle = QtGui.QPolygonF() 
		triangle.append(QtCore.QPointF(x,y))
		triangle.append(QtCore.QPointF(x-10.0,y)) #tail left
		triangle.append(QtCore.QPointF(x,y-10.0)) #tail right
		triangle.append(QtCore.QPointF(x,y))
		return triangle
