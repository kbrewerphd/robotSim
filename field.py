"""
Program name: field.py
Author:       Dr. Brewer
Initial Date: 20-Nov-2018 through 05-Dec-2018
Python vers:  3.6.5

Description:  A simple robot simulation environment.

Code vers:    1.0 - Initial release
"""
import shapes as shs
import math
import point as p
import target as tgt
import random as r
import PyQt5.QtGui as QtGui
from PyQt5.QtWidgets import *
import PyQt5.QtCore  as QtCore


class Field():
	"""
	This is the Field class. It handles the data of the simulation.

	Inherits:
		None

	Returns:
		None
	"""
	def __init__(self, x: float, y: float, n: int) -> None:
		"""
		This is the constructor for the Field class

		Args:
			x (float): the maximum x domain value
			y (float): the maximum y domain value
			n (int): the number of barriers in the domain
		
		Returns:
			None
		"""
		self.max_x = x
		self.max_y = y
		
		self.TEST = False
		
		
		#create new barriers
		print("Creating new barriers...")
		self.ds = shs.Shapes()
		
		if self.TEST:
			self.numBarriers = 1
			newX = 100
			newY = 100
			newXX = 150
			newYY = 150
			self.ds.NewShape(QtCore.QPoint(newX,newY),
							QtCore.QPoint(newXX,newYY),
							QtGui.QBrush(QtGui.QColor(100, 10, 10, 40)),
							QtGui.QColor(100, 10, 10, 40),
							QtGui.QPen(QtGui.QColor(100, 10, 10, 40), 2, QtCore.Qt.SolidLine),
							True)
			
		else:
			self.numBarriers = n
			for i in range(self.numBarriers):
				newX = r.randint(0,int(self.max_x*0.9))
				newY = r.randint(0,int(self.max_y*0.9))
				newXX = newX + r.randint(5,100)
				newYY = newY + r.randint(5,100)
				self.ds.NewShape(QtCore.QPoint(newX,newY),
								QtCore.QPoint(newXX,newYY),
								QtGui.QBrush(QtGui.QColor(100, 10, 10, 40)),
								QtGui.QColor(100, 10, 10, 40),
								QtGui.QPen(QtGui.QColor(100, 10, 10, 40), 2, QtCore.Qt.SolidLine),
								True)
																																
		#create new target	
		print("Creating new target point...")
		if self.TEST:
			self.target = tgt.Target(200,170)
		
		else:
			targetX,targetY = self.goodTarget(0,0)			
			self.target = tgt.Target(targetX,targetY)
		#print("created new target at: ",targetX,targetY)
	
		#create new starting point	
		print("Creating new starting point...")
		if self.TEST:
			self.startPoint = tgt.Target(100,70)

		else:
			targetX,targetY = self.goodTarget(self.target.getLocation()[0],self.target.getLocation()[1])			
			self.startPoint = tgt.Target(targetX,targetY)
		#print("created new starting point at: ",targetX,targetY)
	
	def goodTarget(self,Tx,Ty):
		"""
		This calculates a good location for a target (that
		is not within a barrier).

		Args:
			Tx (float): the proposed target x location
			Ty (float): the proposed target y location
		
		Returns:
			x (float): the proposed target x location
			y (float): the proposed target y location
		"""
		notGoodPoint = True
		while notGoodPoint:
			notGoodPoint = False
			potential_x = float(r.randint(10,self.max_x-10))
			potential_y = float(r.randint(10,self.max_y-10))
			if (Tx == 0 and Ty == 0):
				dist = 500
			else:
				delX = potential_x - Tx
				delY = potential_y - Ty
				dist = math.sqrt(delX*delX + delY*delY)
			#print("Dist:",dist," :: tryCount:",tryCount)
			#if dist < (self.max_y * 0.75):
			if False:
				notGoodPoint = True
				continue
			else:
				for i in range(self.numBarriers):
					if(self.ds.insideBarrier(i,potential_x,potential_y)):
						notGoodPoint = True
		return potential_x,potential_y
		
	def calcEndPoint(self,x,y,d,dist):
		"""
		This function calculates and returns the end point of a line,
		given the starting point, the direction, and the length.

		Args:
			x (float): x location of starting point 
			y (float): y location of starting point 
			d (float): the direction, in degrees 
			dist (float): the length of the line segment 
		
		Returns:
			(Point): the Point at the end of the line segment
		"""
		while d < 0.:
			d = d + 360.
		while d >= 360.:
			d = d - 360.
		if d == 0.:
			return p.Point(x+dist,y)
		elif d == 90.:
			return p.Point(x,y+dist)
		elif d == 180:
			return p.Point(x-dist,y)
		elif d == 270:
			return p.Point(x,y-dist)
			
		if d < 90.:
			xend = math.cos(math.radians(d))*dist + x
			yend = math.sin(math.radians(d))*dist + y
		elif d < 180.:
			xend = x - math.cos(math.radians(180-d))*dist
			yend = math.sin(math.radians(180-d))*dist + y
		elif d < 270.:
			xend = x - math.cos(math.radians(d-180))*dist
			yend = y - math.sin(math.radians(d-180))*dist
		else:
			xend = math.cos(math.radians(360-d))*dist + x
			yend = y - math.sin(math.radians(360-d))*dist
		return p.Point(xend,yend)
	

	def getDist(self,a,b,deg,c,d):
		"""
		This function calculates and returns the distance of 
		intersection along line segment a-b with line segment c-d.
		If there is no intersection, return a large number (50.0).

		Args:
			a (Point): starting point of first line segment
			b (Point): ending point of first line segment 
			deg (float): the direction, in degrees (NOT USED) 
			c (Point): starting point of second line segment 
			d (Point): ending point of second line segment 
		
		Returns:
			(float): the distance along line segment a-b of the intersection,
			if there is no intersection, 50.0 is returned.
		"""
	#stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect#565282
	#Returns 1 if the lines intersect, otherwise 0. In addition, if the lines 
	#intersect the intersection point may be stored in the floats i_x and i_y.

	#char get_line_intersection(float p0_x, float p0_y, float p1_x, float p1_y, 
	#float p2_x, float p2_y, float p3_x, float p3_y, float *i_x, float *i_y)

		p0_x = a.x
		p0_y = a.y
		p1_x = b.x
		p1_y = b.y
		p2_x = c.x
		p2_y = c.y
		p3_x = d.x
		p3_y = d.y

		s1_x = p1_x - p0_x
		s1_y = p1_y - p0_y
		s2_x = p3_x - p2_x
		s2_y = p3_y - p2_y

		try:
			s = (-s1_y * (p0_x - p2_x) + s1_x * (p0_y - p2_y)) / (-s2_x * s1_y + s1_x * s2_y)
			t = ( s2_x * (p0_y - p2_y) - s2_y * (p0_x - p2_x)) / (-s2_x * s1_y + s1_x * s2_y)
		except ZeroDivisionError:
			s = 2.0
			t = 2.0
		if (s >= 0 and s <= 1 and t >= 0 and t <= 1):
			#Intersection detected
			int_x = p0_x + (t * s1_x)
			int_y = p0_y + (t * s1_y)
			dist = math.sqrt((p0_x-int_x)*(p0_x-int_x) + (p0_y-int_y)*(p0_y-int_y))
			return dist
		else:
			return 50.0 #no intersection

	def getSensorResults(self,x,y,d):
		"""
		This function calculates and returns the minimum distance of 
		intersection along four sensor line segments with domain barriers and 
		boundaries. The four sensor segments are front, right, rear, and left -
		relative to the heading given.

		Args:
			x (float): starting x location of sensor beams
			y (float): starting y location of sensor beams 
			deg (float): the direction, in degrees of front 
		
		Returns:
			List[float]: the distance along the four sensor beams
			front, right, rear, and left
			if there is no intersection, 50.0 is returned.
		"""
		#d is pointing direction in degrees
		s_forward = 50.0
		s_right = 50.0
		s_rear = 50.0
		s_left = 50.0
		
		A = p.Point(x,y)
		Bfd = self.calcEndPoint(x,y,d,15.)
		Brt = self.calcEndPoint(x,y,d+90.,15.)
		Brr = self.calcEndPoint(x,y,d+180.,15.)
		Blt = self.calcEndPoint(x,y,d+270.,15.)
		
		#print(x,y,"::",Bfd.x,Bfd,y,":",Brt.x,Brt,y,":",Brr.x,Brr,y,":",Blt.x,Blt,y)
		
		#print("Robot looks from:",x,y," at degrees:",d)
		#print("  Forward to:",Bfd.x,Bfd.y)
		#print("  Right to:",Brt.x,Brt.y)
		#print("  Back to:",Brr.x,Brr.y)
		#print("  Left to:",Blt.x,Blt.y)
		
		
		
		maxX = max(A.x,Bfd.x,Brt.x,Brr.x,Blt.x)
		minX = min(A.x,Bfd.x,Brt.x,Brr.x,Blt.x)
		maxY = max(A.y,Bfd.y,Brt.y,Brr.y,Blt.y)
		minY = min(A.y,Bfd.y,Brt.y,Brr.y,Blt.y)
		
		totShapes = self.ds.NumberOfShapes()
		for i in range(totShapes):
			s = self.ds.GetShape(i)
			x1,x2 = s.getXBounds()
			y1,y2 = s.getYBounds()
			if (min(x1,x2) > maxX): continue
			if (max(x1,x2) < minX): continue
			if (min(y1,y2) > maxY): continue
			if (max(y1,y2) < minY): continue
			#print("Barrier ",i," close by...",x,y,x1,x2,y1,y2)
			C = p.Point(x1,y1)
			D = p.Point(x2,y2)
			E = p.Point(x1,y2)
			F = p.Point(x2,y1)
			#print("forward:",d)
			s_1 = self.getDist(A,Bfd,d,C,E)
			s_2 = self.getDist(A,Bfd,d,E,D)
			s_3 = self.getDist(A,Bfd,d,D,F)
			s_4 = self.getDist(A,Bfd,d,F,C)
			s_fd = min(s_1,s_2,s_3,s_4)
			#print("right:",d+90)
			s_1 = self.getDist(A,Brt,d,C,E)
			s_2 = self.getDist(A,Brt,d,E,D)
			s_3 = self.getDist(A,Brt,d,D,F)
			s_4 = self.getDist(A,Brt,d,F,C)
			s_rt = min(s_1,s_2,s_3,s_4)
			#print("rear:",d+180)
			s_1 = self.getDist(A,Brr,d,C,E)
			s_2 = self.getDist(A,Brr,d,E,D)
			s_3 = self.getDist(A,Brr,d,D,F)
			s_4 = self.getDist(A,Brr,d,F,C)
			s_rr = min(s_1,s_2,s_3,s_4)
			#print("left:",d+270)
			s_1 = self.getDist(A,Blt,d,C,E)
			s_2 = self.getDist(A,Blt,d,E,D)
			s_3 = self.getDist(A,Blt,d,D,F)
			s_4 = self.getDist(A,Blt,d,F,C)
			s_lt = min(s_1,s_2,s_3,s_4)
			if s_fd < s_forward: s_forward = s_fd
			if s_rt < s_right: s_right = s_rt
			if s_rr < s_rear: s_rear = s_rr
			if s_lt < s_left: s_left = s_lt
		
		#do bounaries
		#Sprint("Doing Boundaries")
		AA = p.Point(1,1)
		BB = p.Point(self.max_x-1,1)
		CC = p.Point(self.max_x-1,self.max_y-1)
		DD = p.Point(1,self.max_y-1)
		
		b_fd1 = self.getDist(A,Bfd,d,AA,BB)
		b_fd2 = self.getDist(A,Bfd,d,BB,CC)
		b_fd3 = self.getDist(A,Bfd,d,CC,DD)
		b_fd4 = self.getDist(A,Bfd,d,DD,AA)
		b_fd = min(b_fd1,b_fd2,b_fd3,b_fd4)
		
		b_rt1 = self.getDist(A,Brt,d,AA,BB)
		b_rt2 = self.getDist(A,Brt,d,BB,CC)
		b_rt3 = self.getDist(A,Brt,d,CC,DD)
		b_rt4 = self.getDist(A,Brt,d,DD,AA)
		b_rt = min(b_rt1,b_rt2,b_rt3,b_rt4)
		
		b_rr1 = self.getDist(A,Brr,d,AA,BB)
		b_rr2 = self.getDist(A,Brr,d,BB,CC)
		b_rr3 = self.getDist(A,Brr,d,CC,DD)
		b_rr4 = self.getDist(A,Brr,d,DD,AA)
		b_rr = min(b_rr1,b_rr2,b_rr3,b_rr4)
		
		b_lt1 = self.getDist(A,Blt,d,AA,BB)
		b_lt2 = self.getDist(A,Blt,d,BB,CC)
		b_lt3 = self.getDist(A,Blt,d,CC,DD)
		b_lt4 = self.getDist(A,Blt,d,DD,AA)
		b_lt = min(b_lt1,b_lt2,b_lt3,b_lt4)
		
		if b_fd < s_forward: s_forward = b_fd
		if b_rt < s_right: s_right = b_rt
		if b_rr < s_rear: s_rear = b_rr
		if b_lt < s_left: s_left = b_lt
		
		#print(s_forward,s_right,s_rear,s_left)
		
		return s_forward,s_right,s_rear,s_left
		
		
			
	def inBarrier(self,rX,rY):
		result = False
		totShapes = self.ds.NumberOfShapes()
		for i in range(totShapes):
			s = self.ds.GetShape(i)
			if(s.inShape(rX,rY)): result = True
		return result

	def getTargetLocation(self):
		#print("Getting target location")
		tarPoint = self.target.getLocation()
		#print("target at:",tarPoint[0],tarPoint[1])
		return tarPoint
		
	def getStartLocation(self):
		#print("Getting target location")
		tarPoint = self.startPoint.getLocation()
		#print("target at:",tarPoint[0],tarPoint[1])
		return tarPoint
		
	def getShapes(self):
		return self.ds

	  
	def drawField(self) -> None:
		pass
		
	def update(self) -> None:
		self.drawField()
		pass

