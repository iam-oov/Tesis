
from BASEDATOS.Caso import Caso

from PySide import QtGui, QtCore

class Botones(QtGui.QWidget):
	def __init__(self, arr_conexion):
		super(Botones, self).__init__()

		self.__arr_conexion = arr_conexion

		self.wig = QtGui.QListWidget()

		# Elementos de la interfaz 
		self._btnCargarImagen = QtGui.QPushButton('Cargar imagen', self)
		# self._btnAgregarLinea = QtGui.QPushButton('Agregar linea', self)
		# self.btnAgregarLinea.setEnabled(False)
		self._btnVerHistorial = QtGui.QPushButton('Ver historial', self)
		self.btnVerHistorial.setEnabled(False)
		
		self._btnProcesamiento = QtGui.QPushButton('Procesar imagen')
		self._btnAgregarCasoAPaciente = QtGui.QPushButton('Agregar a paciente', 
																self)
		self._btnCrearNuevoPaciente = QtGui.QPushButton('Crear nuevo paciente', 
																self)

		# Este campo tiene que ser dinamico porque depende de los 
		# pacientes que esten registrados.
		self._comboNombrePaciente = QtGui.QComboBox(self)
		pacientes = self.obtenerDatos()
		self.__palabraDefault = 'Nombre del paciente'
		self.comboNombrePaciente.addItem(self.__palabraDefault)
		for p in pacientes:
			# El valor que regresa es una tupla
			# asi que tenemos que tomar unicamente el primer valor
			p = p[0]
			self.comboNombrePaciente.addItem(p)

		lblVacio = QtGui.QLabel(' ', self)

		# acciones secundarias del boton '_btnAgregarCasoAPaciente'
		lblIdAgregar = QtGui.QLabel('Id: ')
		self._txtIdAgregar = QtGui.QLineEdit(self)
		self._comboNombrePacienteAgregar = QtGui.QComboBox(self)
		self._comboNombrePacienteAgregar.addItem(self.__palabraDefault)
		for p in pacientes:
			# El valor que regresa es una tupla
			# asi que tenemos que tomar unicamente el primer valor
			p = p[0]
			self._comboNombrePacienteAgregar.addItem(p)
		lblOrtodoncistaAgregar = QtGui.QLabel('Ortodoncista: ')
		self._comboNombreOrtodoncistaAgregar = QtGui.QComboBox(self)
		lblComentarioAgregar = QtGui.QLabel('Comentario: ')
		self._txtComentarioAgregar = QtGui.QLineEdit(self)
		self._btnOkAgregar = QtGui.QPushButton('Aceptar', self)

		# acciones secunadior del boton '_btnCrearNuevoPaciente'
		lblIdCrear = QtGui.QLabel('Id: ')
		self._txtIdCrear = QtGui.QLineEdit(self)
		lblNombrePacienteCrear = QtGui.QLabel('Nombre del paciente: ')
		self._txtNombrePacienteCrear = QtGui.QLineEdit(self)
		lblApPaterno = QtGui.QLabel('Apeido paterno: ')
		self._txtPaterno = QtGui.QLineEdit(self)
		lblApMaterno = QtGui.QLabel('Apeido materno: ')
		self._txtMaterno = QtGui.QLineEdit(self)
		lblTelefono = QtGui.QLabel('Telefono: ')
		self._txtTelefono = QtGui.QLineEdit(self)
		lblOrtodoncistaCrear = QtGui.QLabel('Ortodoncista: ')
		self._combotOrtodoncistaCrear = QtGui.QComboBox(self)
		lblCasoCrear = QtGui.QLabel('Caso: ')
		self._txtCasoCrear = QtGui.QLineEdit(self)
		self._btnOkCrear = QtGui.QPushButton('Aceptar', self)

		


		# CONTENEDORES ########################

		botonesFijos = QtGui.QVBoxLayout() 
		botonesFijos.addWidget(self.comboNombrePaciente)
		botonesFijos.addWidget(self.btnCargarImagen)
		botonesFijos.addWidget(self.btnVerHistorial)

		opcionesGenerales = QtGui.QGroupBox('Opciones genereales')
		opcionesGenerales.setLayout(botonesFijos)

		botonImprovistoCargarImagen = QtGui.QVBoxLayout()
		botonImprovistoCargarImagen.addWidget(self.btnProcesamiento)
		botonImprovistoCargarImagen.addWidget(self.btnAgregarCasoAPaciente)
		botonImprovistoCargarImagen.addWidget(self.btnCrearNuevoPaciente)
		
		self._imagenCargada = QtGui.QGroupBox('Imagen cargada...')
		self.imagenCargada.setLayout(botonImprovistoCargarImagen)
		self.__estadoCargar = False
		self.imagenCargada.setVisible(self.__estadoCargar)

		botonImprovistoAgregar = QtGui.QVBoxLayout()
		botonImprovistoAgregar.addWidget(lblIdAgregar)
		botonImprovistoAgregar.addWidget(self.txtIdAgregar)
		botonImprovistoAgregar.addWidget(self.comboNombrePacienteAgregar)
		botonImprovistoAgregar.addWidget(lblOrtodoncistaAgregar)
		botonImprovistoAgregar.addWidget(self.comboNombreOrtodoncistaAgregar)
		botonImprovistoAgregar.addWidget(lblComentarioAgregar)
		botonImprovistoAgregar.addWidget(self.txtComentarioAgregar)
		botonImprovistoAgregar.addWidget(self.btnOkAgregar)

		self._imagenAgregar = QtGui.QGroupBox('Agregar paciente')
		self.imagenAgregar.setLayout(botonImprovistoAgregar)
		self.__estadoAgregar = False
		self.imagenAgregar.setVisible(self.__estadoAgregar)

		botonImprovistoCrear = QtGui.QVBoxLayout()
		botonImprovistoCrear.addWidget(lblIdCrear)
		botonImprovistoCrear.addWidget(self.txtIdCrear)
		botonImprovistoCrear.addWidget(lblNombrePacienteCrear)
		botonImprovistoCrear.addWidget(self.txtNombrePacienteCrear)
		botonImprovistoCrear.addWidget(lblApPaterno)
		botonImprovistoCrear.addWidget(self.txtPaterno)
		botonImprovistoCrear.addWidget(lblApMaterno)
		botonImprovistoCrear.addWidget(self.txtMaterno)
		botonImprovistoCrear.addWidget(lblTelefono)
		botonImprovistoCrear.addWidget(self.txtTelefono)
		botonImprovistoCrear.addWidget(lblOrtodoncistaCrear)
		botonImprovistoCrear.addWidget(self.comboOrtodoncistaCrear)
		botonImprovistoCrear.addWidget(lblCasoCrear)
		botonImprovistoCrear.addWidget(self.txtCasoCrear)
		botonImprovistoCrear.addWidget(self.btnOkCrear)

		self._imagenCrear = QtGui.QGroupBox('Nuevo paciente')
		self.imagenCrear.setLayout(botonImprovistoCrear)
		self.__estadoCrear = False
		self.imagenCrear.setVisible(self.__estadoCrear)

		# acciones secunadior del boton '_btnCrearNuevoPaciente'
		union = QtGui.QVBoxLayout() # contenedor final
		union.addWidget(opcionesGenerales)
		union.addWidget(self.imagenCargada)
		union.addWidget(self.imagenAgregar)
		union.addWidget(self.imagenCrear)

		self.wig.setLayout(union)

		self.inicializar()
		self.conexionesEventos()

	def inicializar(self):
		self.imagen2 = None

	def conexionesEventos(self):
		self.comboNombrePaciente.currentIndexChanged.connect(self.cambioPaciente)
		self.btnCargarImagen.clicked[bool].connect(self.abrir)
		self.btnAgregarCasoAPaciente.clicked[bool].connect(self.agregarCasoAPaciente)
		self.btnCrearNuevoPaciente.clicked[bool].connect(self.crearNuevoPaciente)

	def obtenerDatos(self):
		p = Caso(self.__arr_conexion)
		lista = p.leer('nombre') # la columna de la TABLA que queremos leer
		return lista

	def cambioPaciente(self, nuevoValor):
		try:
			self.valorComboPaciente = \
								str(self.comboNombrePaciente.currentText())
		except:
			self.valorComboPaciente = \
								unicode(self.comboNombrePaciente.currentText())

		if self.valorComboPaciente!=self.__palabraDefault:
			self.btnVerHistorial.setEnabled(True)
		else:
			self.btnVerHistorial.setEnabled(False)

	def actualizarComponente(self):
		if not self.__estadoCargar:
			self.__estadoCargar = True
		else:
			self.__estadoCargar = False
		self.imagenCargada.setVisible(self.__estadoCargar)

	def limpiarCampos(self):
		self.txtIdAgregar.clear()
		self.comboNombrePacienteAgregar.setCurrentIndex(0)
		self.comboNombreOrtodoncistaAgregar.setCurrentIndex(0)
		self.txtComentarioAgregar.clear()

		self.txtIdCrear.clear()
		self.txtNombrePacienteCrear.clear()
		self.txtPaterno.clear()
		self.txtMaterno.clear()
		self.txtTelefono.clear()
		self.comboOrtodoncistaCrear.setCurrentIndex(0)
		self.txtCasoCrear.clear()


	def agregarCasoAPaciente(self):
		if not self.__estadoAgregar:
			self.__estadoAgregar = True
			self.btnAgregarCasoAPaciente.setText('CANCELAR')
			self.btnCrearNuevoPaciente.setEnabled(not self.__estadoAgregar)
		else:
			self.__estadoAgregar = False
			self.btnAgregarCasoAPaciente.setText('Agregar a paciente')
			self.btnCrearNuevoPaciente.setEnabled(not self.__estadoAgregar)
			self.limpiarCampos()
		self.imagenAgregar.setVisible(self.__estadoAgregar)

	def crearNuevoPaciente(self):
		if not self.__estadoCrear:
			self.__estadoCrear = True
			self.btnCrearNuevoPaciente.setText('CANCELAR')
			self.btnAgregarCasoAPaciente.setEnabled(not self.__estadoCrear)
		else:
			self.__estadoCrear = False
			self.btnCrearNuevoPaciente.setText('Crear nuevo paciente')
			self.btnAgregarCasoAPaciente.setEnabled(not self.__estadoCrear)
			self.limpiarCampos()
		self.imagenCrear.setVisible(self.__estadoCrear)



	def abrir(self):
		archivo = QtGui.QFileDialog.getOpenFileName(self, "Open File",
							     QtCore.QDir.currentPath())
		archivo = archivo[0]
		if archivo: # validamos que haya escogido algo en el fileDialog
			imagen = QtGui.QImage(archivo)
			if imagen.isNull():
				QtGui.QMessageBox.information(self, "Aviso",
							      "No se puede cargar el%s." % archivo)
				return
			self.imagen2 = imagen
			self.actualizarComponente()


	

	@property
	def imagenCrear(self):
		return self._imagenCrear

	@property
	def txtTelefono(self):
		return self._txtTelefono

	@property
	def comboOrtodoncistaCrear(self):
		return self._combotOrtodoncistaCrear

	@property
	def txtCasoCrear(self):
		return self._txtCasoCrear

	@property
	def btnOkCrear(self):
		return self._btnOkCrear

	@property
	def txtIdCrear(self):
		return self._txtIdCrear

	@property
	def txtNombrePacienteCrear(self):
		return self._txtNombrePacienteCrear

	@property
	def txtPaterno(self):
		return self._txtPaterno

	@property
	def txtMaterno(self):
		return self._txtMaterno

	@property
	def imagenAgregar(self):
		return self._imagenAgregar

	@property
	def imagenCargada(self):
		return self._imagenCargada

	@property
	def btnOkAgregar(self):
		return self._btnOkAgregar

	@property
	def comboNombrePacienteAgregar(self):
		return self._comboNombrePacienteAgregar

	@property
	def comboNombreOrtodoncistaAgregar(self):
		return self._comboNombreOrtodoncistaAgregar

	@property
	def txtComentarioAgregar(self):
		return self._txtComentarioAgregar

	@property
	def txtIdAgregar(self):
		return self._txtIdAgregar

	@property
	def btnProcesamiento(self):
		return self._btnProcesamiento

	@property
	def btnAgregarCasoAPaciente(self):
		return self._btnAgregarCasoAPaciente

	@property
	def btnVerHistorial(self):
		return self._btnVerHistorial

	@property
	def btnCrearNuevoPaciente(self):
		return self._btnCrearNuevoPaciente

	@property 
	def btnCargarImagen(self):
		return self._btnCargarImagen

	# @property
	# def btnAgregarLinea(self):
	# 	return self._btnAgregarLinea

	@property
	def comboNombrePaciente(self):
		return self._comboNombrePaciente
