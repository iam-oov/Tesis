
import sys
from PySide import QtGui, QtCore
import random

WIGGLY = 2
SEGMENTS = 100
SIZE = 500, 500
BORDER = 14


# def interp(p1, p2, v):
# 	"""Interpolate between p1 and p2 at value v

# 	p1 and p2 are each a two-number tuple (x, y).
# 	v is a float value 0..1.

# 	If v is 0, the result is p1.
# 	If v is 1, the result is p2.
# 	"""
# 	return (p1[0]*v+p2[0]*(1-v), p1[1]*v+p2[1]*(1-v))

def segments(p):
	print p
	"""Convert a list of points into line segments

	p is an iterable having two-number tuples (x, y)
	as elements. The result is a list of segments
	((x1, y1), (x2, y2)) connecting all points.

	Duplicate points are ignored (i.e. no lines are
	created in the result where x1==x2 and y1==y2).
	"""
	result = []
	first = None
	last = None

	for x in p:
		if first is None:
			first = x
		
		if last is not None:
			if x != last:
				result.append((last, x))
		last = x
	return result

def bezier(p0, p1):
	"""Create a bezier line from p0 to p2 using p1

	p0 is a two-number tuple (x, y) of the start point.
	p1 is a two-number tuple (x, y) of the control point.
	p2 is a two-number tuple (x, y) of the end point.

	The global constant SEGMENTS will be used to set
	the number of points/segments. The more segments,
	the more smooth the resulting bezier line is.
	"""
	yield p0

	# for i in range(SEGMENTS-1):
	# 	v = 1.-(float(i+1)/SEGMENTS)
	# 	q1 = interp(p0, p1, v)
	# 	q2 = interp(p1, p2, v)
	# 	p = interp(q1, q2, v)
	# 	yield p
	yield p1

# class BezierSegment(QtGui.QGraphicsLineItem):
# 	def __init__(self, x1, y1, x2, y2, pen):
# 		QtGui.QGraphicsLineItem.__init__(self, x1, y1, x2, y2)
# 		self.setPen(pen)
# 		self.coords = x1, y1, x2, y2

# 	def transform(self, c):
# 		return [x + random.uniform(-WIGGLY, WIGGLY) for x in c]

# 	def wiggle(self, oldpos=None, last=False):
# 		if oldpos is None:
# 			oldpos = list(self.coords[:2])
# 		newpos = list(self.coords[2:])
# 		if not last:
# 			newpos = self.transform(newpos)
# 		self.setLine(*(oldpos+newpos))
# 		return newpos

class Bezier():
	def __init__(self, s, p0, p1, color=None):
		self.children = []

		pe = QtGui.QPen(color) if color else QtGui.QPen()
		br = QtGui.QBrush(color) if color else QtGui.QBrush()
		gr = (QtGui.QPen(QtCore.Qt.gray),)

		# p0<->p1<->p2
		s.addLine(*(p0+p1+gr))
		# s.addLine(*(p1+p2+gr))

		self.lines = list(segments(bezier(p0, p1)))

		print self.lines
		# Create the bezier curve and transform into line segments
		# for a, b in self.lines:
		# 	l = BezierSegment(*(a+b+(pe,)))
		# 	self.children.append(l)
		# 	s.addItem(l)

		# Wiggle all segments, fixing the first and last point to
		# their original values to have a proper attachment
		# self.wiggle()

	# def wiggle(self):
	# 	oldpos = None
	# 	end = len(self.children) - 1
	# 	for i, c in enumerate(self.children):
	# 		oldpos = c.wiggle(oldpos, i == end)



class Ventana(QtGui.QGraphicsScene):
	def __init__(self):
		QtGui.QGraphicsScene.__init__(self)
		self.coords = []
		self.beziers = []

	def mouseReleaseEvent(self, event):
		c = QtCore.Qt.red
		x, y = event.scenePos().x(), event.scenePos().y()
		self.coords.append((x, y))
		self.addEllipse(QtCore.QRectF(x-3, y-3, 6, 6), QtGui.QPen(c), QtGui.QBrush(c))
		if len(self.coords) == 2:
			self.coords.append(c)
			self.beziers.append(Bezier(self, *self.coords))
			self.coords = []


def main():
	app = QtGui.QApplication(sys.argv)
	ventana = Ventana()
	ventana.setSceneRect(QtCore.QRectF(0, 0, *SIZE).adjusted(*((-BORDER,)*2 + (BORDER,)*2)))
	# ventana.showMaximized()

	vista = QtGui.QGraphicsView(ventana)
	vista.setRenderHint(QtGui.QPainter.Antialiasing)
	vista.setWindowTitle('Wiggly bezier curves')
	vista.show()




	sys.exit(app.exec_())




if __name__ == '__main__':
	main()