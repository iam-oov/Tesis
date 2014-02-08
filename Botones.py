
from BASEDATOS.Paciente import Paciente

from PySide import QtGui, QtCore

class Botones(QtGui.QWidget):
	def __init__(self, arr_conexion):
		super(Botones, self).__init__()

		self.__arr_conexion = arr_conexion

		self.wig = QtGui.QListWidget()

		# Elementos de la interfaz 
		self._btnCargarImagen = QtGui.QPushButton('Cargar imagen', self)
		self._btnAgregarLinea = QtGui.QPushButton('Agregar linea', self)
		self._btnAgregarLinea.setEnabled(False)

		# Este campo tiene que ser dinamico porque depende de los 
		# pacientes que esten registrados.
		lblNombrePaciente = QtGui.QLabel('Nombre del paciente: ')
		self._comboNombrePaciente = QtGui.QComboBox(self)
		pacientes = self.obtenerDatos()
		self._comboNombrePaciente.addItem('No aplica')
		for p in pacientes:
			# El valor que regresa es una tupla
			# asi que tenemos que tomar unicamente el primer valor
			p = p[0]
			self._comboNombrePaciente.addItem(p)

		lblVacio = QtGui.QLabel(' ', self)

		# Contenedores para organizar la interfaz
		botones = QtGui.QHBoxLayout() # contenedor
		botones.addWidget(self._btnCargarImagen)
		botones.addWidget(self._btnAgregarLinea)
		botones.addWidget(lblVacio)
		botones.addWidget(lblVacio)
		botones.addWidget(lblVacio)
		botones.addWidget(lblVacio)
		botones.addWidget(lblVacio)
		botones.addWidget(lblVacio)
		
		paciente = QtGui.QHBoxLayout() # contenedor
		paciente.addWidget(lblNombrePaciente)
		paciente.addWidget(self._comboNombrePaciente)
		paciente.addWidget(lblVacio)
		paciente.addWidget(lblVacio)
		paciente.addWidget(lblVacio)
		paciente.addWidget(lblVacio)
		paciente.addWidget(lblVacio)
		paciente.addWidget(lblVacio)
		paciente.addWidget(lblVacio)
		paciente.addWidget(lblVacio)

		union = QtGui.QVBoxLayout() # contenedor
		union.addLayout(paciente)
		union.addLayout(botones)

		self.wig.setLayout(union)


	def obtenerDatos(self):
		p = Paciente(self.__arr_conexion)
		lista = p.leer('nombre') # la columna de la TABLA que queremos leer
		return lista

	@property 
	def btnCargarImagen(self):
		return self._btnCargarImagen

	@property
	def btnAgregarLinea(self):
		return self._btnAgregarLinea

	@property
	def txtNombrePaciente(self):
		return self._comboNombrePaciente
