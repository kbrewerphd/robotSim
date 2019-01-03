import shape
## Shapes class; holds all the drawn shapes
class Shapes:
	__Shapes = []
	
	#CONSTRUCTOR
	def __init__(self):
		self.__Shapes = []
	
	def NumberOfShapes(self): #Returns the number of shapes being stored.
		return len(self.__Shapes)
	def NewShape(self,st,ed,br, co, pn, tp): #Add shape
		Sh = shape.Shape(st,ed,br,co,pn,tp)
		self.__Shapes.append(Sh)
	def eraseAll(self): # remove all shapes
		self.__Shapes = []
	def GetShape(self, Index): # return requested shape
		return self.__Shapes[Index]
		
	def insideBarrier(self,i,x,y):
		xMin,xMax = self.__Shapes[i].getXBounds()
		yMin,yMax = self.__Shapes[i].getYBounds()
		if(x > xMin-4 and x < xMax+4):
			xReturn = True
		else:
			xReturn = False
		if(y > yMin-4 and y < yMax+4):
			yReturn = True
		else:
			yReturn = False
		if (xReturn and yReturn):
			return True
		else:
			return False


