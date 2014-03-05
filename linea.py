
import sys
import math
from PySide import QtGui, QtCore

def segmentos(p):
	todos = []
	primero = None
	ultimo = None

	for x in p:
		if primero is None:
			primero = x
		
		if ultimo is not None:
			if x != ultimo:
				todos.append((ultimo, x))
		ultimo = x
	return todos

def unirPuntos(p0, p1):
	yield p0
	yield p1


class Linea():
	def __init__(self, s, p0, p1, color):
		self.puntos = []
		self.p0 = p0
		self.p1 = p1

		pe = QtGui.QPen(color)
		br = QtGui.QBrush(color)
		gr = (QtGui.QPen(QtCore.Qt.gray),)

		# p0 <-> p1
		s.addLine(*(p0+p1+gr))
		self.union = list(segmentos(unirPuntos(p0, p1)))

	def pendiente(self):
		y = self.p1[1]-self.p0[1]
		x = self.p1[0]-self.p0[0]

		try:
			m = (float(y)/float(x))
			m = int(m*10)/10.0
			return m
		except:
			return 0 

class Ventana(QtGui.QGraphicsScene):
	def __init__(self):
		QtGui.QGraphicsScene.__init__(self)
		self.coordenadas = []
		self.lineas = []

	def mouseReleaseEvent(self, event):
		calculados = list()
		c = QtCore.Qt.red
		x,y = event.scenePos().x(), event.scenePos().y()
		self.coordenadas.append((x,y))
		self.addEllipse(QtCore.QRectF(x-3, y-3, 6, 6), QtGui.QPen(c), QtGui.QBrush(c))
		if len(self.coordenadas)==2:
			self.coordenadas.append(c)
			self.lineas.append(Linea(self, *self.coordenadas))
			if len(self.lineas)>1:
				for i,n in enumerate(self.lineas):
					for j,m in enumerate(self.lineas):
						if i != j:
							if (i,j) not in calculados or (j,i) not in calculados:
								# las lineas se cruzan?
								if n.pendiente() != m.pendiente():
									ang = self.obtenerAngulo(n.pendiente(), m.pendiente())
									if ang<0:
										ang+=180
									ang = int(ang*10)/10.0
									print ang
									calculados.append((i,j))
									calculados.append((j,i))
			self.coordenadas = []

	def obtenerAngulo(self, m1, m2):
		formula = (m2-m1)/(1+(m2*m1))
		return math.degrees(math.atan(formula))
			


def main():
	app = QtGui.QApplication(sys.argv)
	vt = Ventana()
	vt.setSceneRect(QtCore.QRectF(0, 0, 300, 300))

	vista = QtGui.QGraphicsView(vt)
	vista.setRenderHint(QtGui.QPainter.Antialiasing)
	vista.setWindowTitle('Angulos')
	vista.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
