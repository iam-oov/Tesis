
from PySide import QtGui, QtCore

class Botones(QtGui.QWidget):
	def __init__(self):
		super(Botones, self).__init__()

		self.wig = QtGui.QListWidget()

		# Elementos de la interfaz 
		self._btnCargarImagen = QtGui.QPushButton('Cargar imagen', self)
		self._btnAgregarLinea = QtGui.QPushButton('Agregar linea', self)

		# Contenedores para organizar la interfaz
		botones = QtGui.QHBoxLayout() # contenedor
		botones.addWidget(self._btnCargarImagen)
		botones.addWidget(self._btnAgregarLinea)

		self.wig.setLayout(botones)

	@property 
	def btnCargarImagen(self):
		return self._btnCargarImagen

	@property
	def btnAgregarLinea(self):
		return self._btnAgregarLinea
