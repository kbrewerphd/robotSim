"""
Program name: robotSim.py
Author:       Dr. Brewer
Initial Date: 20-Nov-2018 through 05-Dec-2018
Python vers:  3.6.5

Description:  A simple robot simulation environment.

Code vers:    1.0 - Initial release
"""

# ------ import section ------
import sys
import time
import random as r
import robot 
import target as tgt
from typing import List
import PyQt5.QtGui as QtGui
from PyQt5.QtWidgets import *
import PyQt5.QtCore  as QtCore

#remember to use: pyuic5 xyz.ui > xyz.py 
from robotGUI import Ui_MainWindow

# ------ global variables ------
DOMAIN_X = 800.0
DOMAIN_Y = 500.0
MAX_WHEEL_V = 10.0

# ------ class section ------

###########################################################	
## MainWindow class;
class MainWindow(QMainWindow, Ui_MainWindow):
	"""
	This is the main window class. It uses a Designer generated 
	UI (user interface) file as well as a custom frame widget.

	Inherits:
		QMainWindow: PyQt5 Main Window Widget
		Ui_MainWindow: Designer generated user interface widgets

	Returns:
		None
	"""
	def __init__(self, *args, **kwargs):
		"""
		This is the constructor for the Main Window class

		Args:
			Standard
		
		Returns:
			None
		"""
		super(MainWindow, self).__init__(*args, **kwargs)
		
		self.setupUi(self)
		
		self.outputString = "" #this will be the content of the textEdit widget
		self.stopSim = False
		
		self.numBarriers = 10 #the default number of barriers 
		
		self.createSim()
		
		self.sld.valueChanged.connect(self.changeBarriers) # connect slider to function
		self.runButton.pressed.connect(self.runSim) # connects button to function
		self.createButton.pressed.connect(self.createSim) # connects button to function
		
		self.show()
		
	def changeBarriers(self, value):
		"""
		A function that is called when the slider is moved.

		Args:
			value (int): current slider value
		
		Returns:
			None
		"""
		self.numBarriers = value
		
	def createSim(self):
		"""
		A function that is called when the create button is pressed.
		This is where the simulation is created.

		Args:
			None
		
		Returns:
			None
		"""
		self.stopSim = True
		self.outputString = "" #reset the textEdit string
		self.textEdit.setText(self.outputString)
		#create&draw new frame/field/target/start point
		self.frame.createField(DOMAIN_X,DOMAIN_Y,self.numBarriers)
		#display the robots in the simulation
		for i in range(self.frame.robots.NumberOfRobots()):
			robot = self.frame.robots.GetRobot(i)
			color = robot.rgb
			name = robot.name
			self.outputString += "Robot '"+robot.name+"' has color"+str(color)+"\n"
			self.textEdit.setText(self.outputString)
		self.update()
		
	def runSim(self):
		"""
		A function that is called when the run button is pressed.
		This is where the simulation runs.

		Args:
			None
		
		Returns:
			None
		"""
		#setup time -- start at 0 and increment by 1
		simTime = 0
		delta_t = 1
		
			
		#loop time till all robots are immobile
		robotsMoving = True
		self.stopSim = False
		while robotsMoving:
			print("Simulation time:", simTime)
			#for each robot, update the sensors and move the robot
			for i in range(self.frame.robots.NumberOfRobots()):
				robot = self.frame.robots.GetRobot(i)
				if robot.stillMoving():
					#update robot sensors
					rX,rY = robot.get_position()
					dir = robot.get_heading_degrees()
					s = self.frame.field.getSensorResults(rX,rY,dir)
					robot.set_sensor_readings(s)
					#now move robot if not already stopped
					robot.move_robot(delta_t)
					
			#for each robot, update moving status and update the textEdit string if needed
			robotsMoving = False
			for i in range(self.frame.robots.NumberOfRobots()):
				robot = self.frame.robots.GetRobot(i)
				if robot.stillMoving():
					rX,rY = robot.get_position()
					if(self.frame.field.inBarrier(rX,rY)): 
						robot.setMoving(False) #crash into barrier
						self.outputString += "Robot '"+robot.name+"' crashed into a barrier!\n"
						self.textEdit.setText(self.outputString)
					if(rX < 1 or rY < 1): 
						robot.setMoving(False) #crash out of domain
						self.outputString += "Robot '"+robot.name+"' crashed out of the domain!\n"
						self.textEdit.setText(self.outputString)
					if(rX > DOMAIN_X or rY > DOMAIN_Y): 
						robot.setMoving(False) #crash out of domain
						self.outputString += "Robot '"+robot.name+"' crashed out of the domain!\n"
						self.textEdit.setText(self.outputString)
					ang,dist = robot.get_robot_target()
					if(dist < 2): 
						robot.setMoving(False) #stop robot if at target!
						self.outputString += "Robot '"+robot.name+"' reached target!\n"
						self.outputString += "   using "+str(robot.getTotalTime())+" seconds of processor time.\n"
						self.textEdit.setText(self.outputString)
					if robot.stillMoving(): robotsMoving = True
				
			simTime += delta_t
			self.update()
			QApplication.processEvents()
			time.sleep(0.05)	#a slight delay just to make the simulation visually nicer
			
			#determine if simulation is over
			if self.stopSim:
				robotsMoving = False
				self.stopSim = False
			
		#simulation over, update the textEdit output
		self.outputString += "===Simulation run finished===\n"
		self.textEdit.setText(self.outputString)
		print("===Simulation run finished===")
		self.update()
		
# ------ execution section ------
if __name__ == '__main__':
	"""
	This is where the application runs. It starts the GUI main window.
	"""
	app = QApplication([])
	app.setApplicationName("RobotSimApp")

	window = MainWindow()
	app.exec_()