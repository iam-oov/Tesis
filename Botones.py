
from PySide import QtGui, QtCore

import os
from datetime import date

from Caso import Caso
from BASEDATOS.Paciente import Paciente
from BASEDATOS.Historial import Historial
from BASEDATOS.Ortodoncista import Ortodoncista

from UTILERIAS.AdministradorArchivos import AdministradorArchivos


class Botones(QtGui.QWidget):
	def __init__(self, arr_conexion):
		super(Botones, self).__init__()

		self.__arr_conexion = arr_conexion
		self.ca = Caso()

		# Elementos de la interfaz 
		self._btnCargarImagen = QtGui.QPushButton('Cargar imagen', self)
		# self._btnAgregarLinea = QtGui.QPushButton('Agregar linea', self)
		# self.btnAgregarLinea.setEnabled(False)
		self._btnVerHistorial = QtGui.QPushButton('Ver historial', self)
		self.btnVerHistorial.setEnabled(False)
		
		self._btnProcesamiento = QtGui.QPushButton('Procesar imagen')
		self._btnAgregarCasoAPaciente = QtGui.QPushButton('Agregar a paciente', self)
		self.btnAgregarCasoAPaciente.setEnabled(False)

		self._btnCrearNuevoPaciente = QtGui.QPushButton('Crear nuevo paciente', self)
		self.btnCrearNuevoPaciente.setEnabled(False)


		# Este campo tiene que ser dinamico porque depende de los 
		# pacientes que esten registrados.
		self._comboNombrePaciente = QtGui.QComboBox(self)
		self.refrescarPacientes()

		lblVacio = QtGui.QLabel(' ', self)

		# acciones secundarias del boton '_btnAgregarCasoAPaciente'
		lblIdAgregar = QtGui.QLabel('Id: ')
		self._txtIdAgregar = QtGui.QLineEdit(self) 
		self.txtIdAgregar.setReadOnly(True)
		self._comboNombrePacienteAgregar = QtGui.QComboBox(self)
		self.comboNombrePacienteAgregar.addItem(self.__palabraDefault)
		for p in pacientes:
			# El valor que regresa es una tupla
			# asi que tenemos que tomar unicamente el primer valor
			p = p[0]
			self.comboNombrePacienteAgregar.addItem(p)
		lblOrtodoncistaAgregar = QtGui.QLabel('Ortodoncista: ')
		self.__palabraDefaultOrtodoncista = 'Seleccione uno...'
		self._comboOrtodoncistaAgregar = QtGui.QComboBox(self)
		self.comboOrtodoncistaAgregar.addItem(self.__palabraDefaultOrtodoncista)
		nombres = self.obtenerDatosXColumna(columna='nombre', tabla='ortodoncista')
		apPaternos = self.obtenerDatosXColumna(columna='apPaterno', tabla='ortodoncista')
		for n,ap in zip(nombres, apPaternos):
			n = n[0]
			ap = ap[0]
			self.comboOrtodoncistaAgregar.addItem('Dr. '+n+' '+ap)
		lblComentarioAgregar = QtGui.QLabel('Comentario: ')
		self._txtComentarioAgregar = QtGui.QLineEdit(self)
		lblCasoAgregar = QtGui.QLabel('Caso: ')
		self.__palabraDefaultCaso = 'Seleccione uno...'
		self._comboCasoAgregar = QtGui.QComboBox(self)
		self.comboCasoAgregar.addItem(self.__palabraDefaultCaso)
		
		for i in self.ca.casos:
			self.comboCasoAgregar.addItem(i)

		self._btnOkAgregar = QtGui.QPushButton('Aceptar', self)

		# acciones secundario del boton '_btnCrearNuevoPaciente'
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
		self._comboCasoCrear = QtGui.QComboBox(self)
		self._btnOkCrear = QtGui.QPushButton('Aceptar', self)

		# CONTENEDORES ########################

		botonesFijos = QtGui.QVBoxLayout() 
		botonesFijos.addWidget(self.comboNombrePaciente)
		botonesFijos.addWidget(self.btnCargarImagen)
		botonesFijos.addWidget(self.btnVerHistorial)
		botonesFijos.addStretch(1)

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
		botonImprovistoAgregar.addWidget(self.comboOrtodoncistaAgregar)
		botonImprovistoAgregar.addWidget(lblCasoAgregar)
		botonImprovistoAgregar.addWidget(self.comboCasoAgregar)
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
		botonImprovistoCrear.addWidget(self.comboCasoCrear)
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
		union.addStretch(1)

		self.wig = QtGui.QListWidget()
		self.wig.setLayout(union)

		self.inicializar()
		self.conexionesEventos()

	def abrir(self):
		archivo = QtGui.QFileDialog.getOpenFileName(self, "Open File",
							     QtCore.QDir.currentPath())
		archivo = archivo[0]
		if archivo: # validamos que haya escogido algo en el fileDialog
			imagen = QtGui.QImage(archivo)
			if imagen.isNull():
				QtGui.QMessageBox.information(self, "Aviso",
							      "No se puede cargar el %s." % archivo)
				return
			self.imagen = imagen
			self.rutaImagen = archivo
			self.actualizarComponente()
			self.btnAgregarCasoAPaciente.setEnabled(False)
			self.btnCrearNuevoPaciente.setEnabled(False)

	def actualizar(self):
		self.refrescarPacientes()

	def actualizarComponente(self):
		if not self.__estadoCargar:
			self.__estadoCargar = True
		else:
			self.__estadoCargar = False
		self.imagenCargada.setVisible(self.__estadoCargar)

	def agregarBD(self, campos=''):
		if campos=='Agregar':
			x = self.obtenerDatosAnteriores()
			if not x:
				casoAnterior = None
				rutaCasoAnterior = None
			else:
				casoAnterior = x[0]
				rutaCasoAnterior = x[1]

			id = int(self.txtIdAgregar.text())
			casoNuevo = self.comboCasoAgregar.currentText()
			rutaCasoNuevo = os.getcwd()
			
			hoy = date.today()
			fecha = str(hoy.year) +'/'+str(hoy.month)+'/'+str(hoy.day)
			
			ortodoncista = self.valorComboOrtodoncistaAgregar
			comentario = self.txtComentarioAgregar.text()

			self.agregarRegistro(
				id, 
				casoAnterior, 
				casoNuevo, 
				fecha, 
				ortodoncista,
				comentario,
				rutaCasoAnterior,
				rutaCasoNuevo
				)

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

	def agregarRegistro(self, *datos):
		s = Historial(self.__arr_conexion)
		s.id = datos[0]
		s.casoAnterior = datos[1]
		s.casoNuevo = datos[2]
		s.fecha = datos[3]
		s.ortodoncista = datos[4]
		s.comentario = datos[5]
		s.rutaCasoAnterior = datos[6]
		s.rutaCasoNuevo = datos[7]
		s.agregar()

	def asignarCasoAFormulario(self, caso):
		self.comboCasoAgregar.setCurrentIndex(self.comboCasoAgregar.findText(caso))

	def buscarId(self, paciente):
		p = Caso(self.__arr_conexion)
		id = p.obtenerId(paciente)
		return id

	def cambioNombrePacienteAgregar(self):
		try:
			self.valorComboPacienteAgregar = \
							str(self.comboNombrePacienteAgregar.currentText())
		except:
			self.valorComboPacienteAgregar = \
							unicode(self.comboNombrePacienteAgregar.currentText())

		# buscar el id en la tabla y asignarla al editLine
		if self.valorComboPacienteAgregar!=self.__palabraDefault:
			id = self.buscarId(self.valorComboPacienteAgregar)[0][0]
			self.txtIdAgregar.setText(str(id))
		else:
			self.txtIdAgregar.clear()

	def cambioOrtodoncistaAgregar(self):
		try:
			self.valorComboOrtodoncistaAgregar = \
							str(self.comboOrtodoncistaAgregar.currentText())
		except:
			self.valorComboOrtodoncistaAgregar = \
							unicode(self.comboOrtodoncistaAgregar.currentText())

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

	def conexionesEventos(self):
		self.comboNombrePaciente.currentIndexChanged.connect(self.cambioPaciente)
		self.btnCargarImagen.clicked[bool].connect(self.abrir)
		self.btnAgregarCasoAPaciente.clicked[bool].connect(self.agregarCasoAPaciente)
		self.btnCrearNuevoPaciente.clicked[bool].connect(self.crearNuevoPaciente)
		self.comboNombrePacienteAgregar.currentIndexChanged.connect(self.cambioNombrePacienteAgregar)
		self.comboOrtodoncistaAgregar.currentIndexChanged.connect(self.cambioOrtodoncistaAgregar)
		self.btnOkAgregar.clicked[bool].connect(self.okAgregar)
		self.btnProcesamiento.clicked[bool].connect(self.procesar)

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

	def inicializar(self):
		self.imagen = None

	def limpiarCampos(self):
		self.txtIdAgregar.clear()
		self.comboNombrePacienteAgregar.setCurrentIndex(0)
		self.comboOrtodoncistaAgregar.setCurrentIndex(0)
		self.txtComentarioAgregar.clear()
		self.txtIdCrear.clear()
		self.txtNombrePacienteCrear.clear()
		self.txtPaterno.clear()
		self.txtMaterno.clear()
		self.txtTelefono.clear()
		self.comboOrtodoncistaCrear.setCurrentIndex(0)

	def obtenerDatosAnteriores(self):
		s = Historial(self.__arr_conexion)
		datos = s.obtenerDatosAnteriores()
		return datos

	def obtenerDatosXColumna(self, columna='', tabla=''):
		if tabla=='paciente':
			p = Paciente(self.__arr_conexion)
			lista = p.leer(columna) 
			return lista
		elif tabla=='ortodoncista':
			p = Ortodoncista(self.__arr_conexion)
			lista = p.leer(columna)
			return lista
		
	def obtenerNombreArchivo(self, ruta):
		utl = AdministradorArchivos()
		lista = utl.parsearCadena(ruta, separador='/')
		return lista[-1]

	def okAgregar(self):
		# validar los campos
		#	Que este seleccionados
		if self.comboNombrePacienteAgregar!=self.__palabraDefault\
			and self.valorComboOrtodoncistaAgregar!=self.__palabraDefaultOrtodoncista\
			and len(self.comboCasoAgregar.currentText())!=self.__palabraDefaultCaso\
			and len(self.txtComentarioAgregar.text())!=0:
				self.agregarBD(campos='Agregar')
				self.comboNombrePacienteAgregar.setCurrentIndex(0)
				self.txtComentarioAgregar.clear()

		else:
			MENSAJE ='No se pudo completar la operacion.\
			\n1.- Asegurese de tener todos los campos completos.'
			QtGui.QMessageBox.critical(self, 'CRITICAL ERROR', \
										MENSAJE, QtGui.QMessageBox.Abort)

	def procesar(self):
		nombre = self.obtenerNombreArchivo(self.rutaImagen)

		MENSAJE='Desea procesar la imagen: "'+nombre+ '".'
		reply = QtGui.QMessageBox.question(self, 'Message', MENSAJE, \
						QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
		if reply==QtGui.QMessageBox.Yes:
			caso = self.ca.seleccionarCaso()
			# asignar a los campos de los formularios
			self.asignarCasoAFormulario(caso)

			# activar los botones de agregar a cliente
			self.btnAgregarCasoAPaciente.setEnabled(True)
			self.btnCrearNuevoPaciente.setEnabled(True)

	def refrescarPacientes(self):
		self.comboNombrePaciente.clear()
		self.comboNombrePaciente.addItem(self.__txtNombreDefault)
		datos = self.obtenerDatosXColumna(columna='nombre', tabla='paciente')
		for i in datos:
			i = i[0]
			self.txtNombre.addItem(i)

	@property
	def comboCasoAgregar(self):
		return self._comboCasoAgregar

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
	def comboCasoCrear(self):
		return self._comboCasoCrear

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
	def comboOrtodoncistaAgregar(self):
		return self._comboOrtodoncistaAgregar

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

	@property
	def comboNombrePaciente(self):
		return self._comboNombrePaciente
