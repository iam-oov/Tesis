
from PySide import QtGui, QtCore

import os
from datetime import datetime

from Caso import Caso
from BASEDATOS.PacienteBD import PacienteBD
from BASEDATOS.HistorialBD import HistorialBD
from BASEDATOS.OrtodoncistaBD import OrtodoncistaBD
from UTILERIAS.AdministradorArchivos import AdministradorArchivos

import CONSTANTES


class Botones(QtGui.QWidget):
	def __init__(self, arr_conexion):
		super(Botones, self).__init__()

		self.__arr_conexion = arr_conexion
		self.ca = Caso()
		self.admArc = AdministradorArchivos()

		# Elementos de la interfaz 

		self._btnCargarImagen = QtGui.QPushButton('Cargar imagen', self)
		# self._btnAgregarLinea = QtGui.QPushButton('Agregar linea', self)
		# self.btnAgregarLinea.setEnabled(False)
		self._btnVerHistorialBD = QtGui.QPushButton('Ver historial', self)
		self.btnVerHistorialBD.setEnabled(False)
		
		self._btnProcesamiento = QtGui.QPushButton('Procesar imagen')
		self._btnAgregarCasoAPaciente = QtGui.QPushButton('Agregar a paciente', self)
		self.btnAgregarCasoAPaciente.setEnabled(False)

		# Este campo tiene que ser dinamico porque depende de los 
		# pacientes que esten registrados.
		self.__palabraDefaultPaciente = 'Paciente...'
		self._comboNombrePaciente = QtGui.QComboBox(self)

		# acciones secundarias del boton '_btnAgregarCasoAPaciente'
		lblO = QtGui.QLabel('o')

		lblIdAgregar = QtGui.QLabel('ID: ')
		self._txtId = QtGui.QLineEdit(self) 

		lblIdAgregarCopia = QtGui.QLabel('ID: ')
		self._txtIdCopia = QtGui.QLineEdit(self) 

		self._comboNombre = QtGui.QComboBox(self)
		self.refrescarPacientes()
		
		self.__palabraDefaultOrtodoncista = 'Ortodoncista...'
		self._comboOrtodoncista = QtGui.QComboBox(self)
		self.comboOrtodoncista.addItem(self.__palabraDefaultOrtodoncista)
		self.refrescarOrtodoncista()

		self._txtComentario = QtGui.QLineEdit(self)
		self.txtComentario.setPlaceholderText('Comentario')
		self.txtComentario.setStyleSheet(CONSTANTES.campos)
		self.__palabraDefaultCaso = 'Caso...'
		self._comboCaso = QtGui.QComboBox(self)
		self.comboCaso.addItem(self.__palabraDefaultCaso)
		self.refrescarCasos()

		self._btnOkAgregar = QtGui.QPushButton('Aceptar', self)

		

		botonesFijos = QtGui.QVBoxLayout() 
		botonesFijos.addWidget(self.btnCargarImagen)
		botonesFijos.addStretch(1)

		camposDatosPaciente = QtGui.QHBoxLayout()
		camposDatosPaciente.addWidget(lblIdAgregarCopia)
		camposDatosPaciente.addWidget(self.txtIdCopia)

		campoO = QtGui.QHBoxLayout()
		campoO.addStretch(1)
		campoO.addWidget(lblO)
		campoO.addStretch(1)

		campoHistorial = QtGui.QHBoxLayout()
		campoHistorial.addStretch(1)
		campoHistorial.addWidget(self.btnVerHistorialBD)

		botonesPaciente = QtGui.QVBoxLayout() 		
		botonesPaciente.addLayout(camposDatosPaciente)
		botonesPaciente.addLayout(campoO)
		botonesPaciente.addWidget(self.comboNombrePaciente)
		botonesPaciente.addLayout(campoHistorial)
		
		opcionesGenerales = QtGui.QGroupBox('Procesamiento')
		opcionesGenerales.setLayout(botonesFijos)

		opcionesPaciente = QtGui.QGroupBox('Pacientes')
		opcionesPaciente.setLayout(botonesPaciente)

		botonImprovistoCargarImagen = QtGui.QVBoxLayout()
		botonImprovistoCargarImagen.addWidget(self.btnProcesamiento)
		botonImprovistoCargarImagen.addWidget(self.btnAgregarCasoAPaciente)
		
		self._imagenCargada = QtGui.QGroupBox('Opciones generales')
		self.imagenCargada.setLayout(botonImprovistoCargarImagen)
		self.__estadoCargar = False
		self.imagenCargada.setVisible(self.__estadoCargar)

		camposIds = QtGui.QHBoxLayout()
		camposIds.addWidget(lblIdAgregar)
		camposIds.addWidget(self.txtId)

		campoBtnAceptar = QtGui.QHBoxLayout()
		campoBtnAceptar.addStretch(1)
		campoBtnAceptar.addWidget(self.btnOkAgregar)

		botonImprovistoAgregar = QtGui.QVBoxLayout()
		botonImprovistoAgregar.addLayout(camposIds)
		botonImprovistoAgregar.addWidget(self.comboNombre)
		botonImprovistoAgregar.addWidget(self.comboOrtodoncista)
		botonImprovistoAgregar.addWidget(self.comboCaso)
		botonImprovistoAgregar.addWidget(self.txtComentario)
		botonImprovistoAgregar.addLayout(campoBtnAceptar)

		self._imagenAgregar = QtGui.QGroupBox('Agregar paciente')
		self.imagenAgregar.setLayout(botonImprovistoAgregar)
		self.__estadoAgregar = False
		self.imagenAgregar.setVisible(self.__estadoAgregar)

		# acciones secunadior del boton '_btnCrearNuevoPaciente'
		union = QtGui.QVBoxLayout() # contenedor final
		union.addWidget(opcionesGenerales)
		union.addWidget(opcionesPaciente)
		union.addWidget(self.imagenCargada)
		union.addWidget(self.imagenAgregar)
		# union.addWidget(self.imagenCrear)
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
			# self.btnCrearNuevoPaciente.setEnabled(False)

	def actualizar(self):
		self.refrescarPacientes()
		self.refrescarOrtodoncista()
		self.refrescarCasos()

	def actualizarComponente(self):
		if not self.__estadoCargar:
			self.__estadoCargar = True
		else:
			self.__estadoCargar = False
		self.imagenCargada.setVisible(self.__estadoCargar)

	def agregarBD(self, id):
		id = str(id[0][0])
		x = self.obtenerCasoAnterior(id)

		if not x:
			casoAnterior = None
			rutaCasoAnterior = None
		else:
			casoAnterior = x[0][0]
			rutaCasoAnterior = x[0][1]

		print 'casoAnterior:', casoAnterior
		print 'rutaCasoAnterior:', rutaCasoAnterior
		print '--.-.-.'

		casoNuevo = self.comboCaso.currentText()
		rutaCasoNuevo = self.rutaImagen
		
		fecha = self.obtenerFechaActual()
		
		ortodoncista = self.valorComboOrtodoncista
		comentario = self.txtComentario.text()

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
		else:
			self.__estadoAgregar = False
			self.btnAgregarCasoAPaciente.setText('Agregar a paciente')
			self.limpiarCampos()
		self.imagenAgregar.setVisible(self.__estadoAgregar)

	def agregarRegistro(self, *datos):
		s = HistorialBD(self.__arr_conexion)
		s.id = datos[0]
		s.casoAnterior = datos[1]
		s.casoNuevo = datos[2]
		s.fecha = datos[3]
		s.ortodoncista = datos[4]
		s.comentario = datos[5]
		s.rutaCasoAnterior = datos[6]
		s.rutaCasoNuevo = datos[7]
		s.agregar()

	def analizarQuery(self):
		self.armarQuery()
		# actualizamos el valor del camboBox paciente
		lista = self.ejecutarQuery(self.query)

		if len(lista)>1:
			# Varios
			self.txtId.setStyleSheet('QLineEdit {color: blue}')
			self.txtIdCopia.setStyleSheet('QLineEdit {color: blue}')
			self.seleccionarCampos(lista) 
		elif len(lista)==1:
			# Unico
			self.txtId.setStyleSheet('QLineEdit {color: green}')
			self.txtIdCopia.setStyleSheet('QLineEdit {color: green}')
			self.seleccionarCampos(lista) 
		else:
			# Todos
			self.txtId.setStyleSheet('QLineEdit {color: red}')
			self.txtIdCopia.setStyleSheet('QLineEdit {color: red}')
			self.refrescarPacientes()

	def armarQuery(self):
		inicio = 'SELECT nombre FROM '+ CONSTANTES.pacienteBD
		self.query = inicio
		if len(self.__valorId)==0:
			self.query = inicio
			self.__reseteo = True
		else:    
			self.query += ' WHERE '+CONSTANTES.columna1_PA+ ' LIKE "%'+self.__valorId+'%"'
			self.__reseteo = False	

	def asignarCasoAFormulario(self, caso):
		self.comboCaso.setCurrentIndex(self.comboCaso.findText(caso))

	def buscarId(self, paciente):
		p = PacienteBD(self.__arr_conexion)
		id = p.obtenerId(paciente)
		return id

	def cambioId(self, nuevoId):
		self.__valorId = nuevoId
		self.analizarQuery()

	def cambioIdCopia(self, nuevoId):
		self.__valorId = nuevoId
		self.analizarQuery()

	def cambioNombre(self):
		try:
			self.valorComboPacienteAgregar = \
							str(self.comboNombre.currentText())
		except:
			self.valorComboPacienteAgregar = \
							unicode(self.comboNombre.currentText())

	def cambioOrtodoncista(self):
		try:
			self.valorComboOrtodoncista = \
							str(self.comboOrtodoncista.currentText())
		except:
			self.valorComboOrtodoncista = \
							unicode(self.comboOrtodoncista.currentText())

	def cambioPaciente(self, nuevoValor):
		try:
			self.valorComboPaciente = \
								str(self.comboNombrePaciente.currentText())
		except:
			self.valorComboPaciente = \
								unicode(self.comboNombrePaciente.currentText())

		if self.valorComboPaciente!=self.__palabraDefaultPaciente:
			self.btnVerHistorialBD.setEnabled(True)
		else:
			self.btnVerHistorialBD.setEnabled(False)

	def conexionesEventos(self):
		self.comboNombrePaciente.currentIndexChanged.connect(self.cambioPaciente)
		self.btnCargarImagen.clicked[bool].connect(self.abrir)
		self.btnVerHistorialBD.clicked[bool].connect(self.verHistorial)
		self.btnProcesamiento.clicked[bool].connect(self.procesar)
		self.btnAgregarCasoAPaciente.clicked[bool].connect(self.agregarCasoAPaciente)
		self.comboNombre.currentIndexChanged.connect(self.cambioNombre)
		self.comboOrtodoncista.currentIndexChanged.connect(self.cambioOrtodoncista)
		self.txtId.textChanged.connect(self.cambioId)
		self.txtIdCopia.textChanged.connect(self.cambioIdCopia)
		self.btnOkAgregar.clicked[bool].connect(self.okAgregar)

	def ejecutarQuery(self, query):
		re = PacienteBD(self.__arr_conexion)
		lista = re.ejecutarQueryDinamico(query)
		return lista
		
	def inicializar(self):
		self.__valorId = ''
		self.__valorIdCopia = ''
		self.imagen = None

	def limpiarCampos(self):
		self.txtId.clear()
		self.comboNombre.setCurrentIndex(0)
		self.comboOrtodoncista.setCurrentIndex(0)
		self.txtComentario.clear()

	def obtenerApellidos(self, nombre):
		s = PacienteBD(self.__arr_conexion)
		apellidos = s.obtenerApellidos(nombre)
		apellidos = apellidos[0]
		ap = ''
		for i in apellidos:
			ap+=i+' '
		ap = ap[:len(ap)-1] # eliminamos el ultimo elemento de la cadena
		return ap

	def obtenerCasoAnterior(self, id):
		s = HistorialBD(self.__arr_conexion)
		datos = s.obtenerCasoAnterior(id)
		return datos

	def obtenerDatosXColumna(self, columna='', tabla=''):
		if tabla=='paciente':
			p = PacienteBD(self.__arr_conexion)
			lista = p.leer(columna) 
			return lista
		elif tabla=='ortodoncista':
			p = OrtodoncistaBD(self.__arr_conexion)
			lista = p.leer(columna)
			return lista

	def obtenerFechaActual(self):
		i = datetime.now()
		fecha = str(i)
		return fecha

	def obtenerHistorial(self, id):
		s = HistorialBD(self.__arr_conexion)
		datos = s.obtenerHistorial(id)
		return datos
		
	def obtenerNombreArchivo(self, ruta):
		utl = AdministradorArchivos()
		lista = utl.parsearCadena(ruta, separador='/')
		return lista[-1]

	def okAgregar(self):
		# validar los campos
		#	Que este seleccionados
		if self.comboNombre.currentText()!=self.__palabraDefaultPaciente\
			and self.valorComboOrtodoncista!=self.__palabraDefaultOrtodoncista\
			and len(self.comboCaso.currentText())!=self.__palabraDefaultCaso\
			and len(self.txtComentario.text())!=0:
				nombre = self.admArc.parsearCadena(self.comboNombre.currentText(), separador=' ')
				nombre = nombre[0]
				self.agregarBD(self.buscarId(nombre))

				MENSAJE ='Moviemiento guardado.'
				QtGui.QMessageBox.information(self, 'Information', MENSAJE)
				
				# limpiar campos
				self.comboNombre.setCurrentIndex(0)
				self.txtComentario.clear()

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

	def refrescarCasos(self):
		for i in self.ca.casos:
			self.comboCaso.addItem(i)

	def refrescarOrtodoncista(self):
		self.comboOrtodoncista.clear()
		self.comboOrtodoncista.addItem(self.__palabraDefaultOrtodoncista)

		nombres = self.obtenerDatosXColumna(columna='nombre', tabla='ortodoncista')
		apPaterno = self.obtenerDatosXColumna(columna='apPaterno', tabla='ortodoncista')
		for n,apP in zip(nombres, apPaterno):
			n = n[0]
			apP = apP[0]
			self.comboOrtodoncista.addItem('Dr. '+n+' '+apP)

	def refrescarPacientes(self):
		self.comboNombrePaciente.clear()
		self.comboNombre.clear()
		
		self.comboNombrePaciente.addItem(self.__palabraDefaultPaciente)
		self.comboNombre.addItem(self.__palabraDefaultPaciente)

		nombre = self.obtenerDatosXColumna(columna='nombre', tabla='paciente')
		apPaterno = self.obtenerDatosXColumna(columna='apPaterno', tabla='paciente')
		apMaterno = self.obtenerDatosXColumna(columna='apMaterno', tabla='paciente')
		
		for i in range(len(nombre)):
			n = nombre[i][0]
			apP = apPaterno[i][0]
			apM = apMaterno[i][0]

			self.comboNombrePaciente.addItem(n+' '+apP+' '+apM)
			self.comboNombre.addItem(n+' '+apP+' '+apM)

	def seleccionarCampos(self, lista):
		item = lista[0][0]
		apellidos = self.obtenerApellidos(item)
		item = item+' '+apellidos

		if self.__reseteo:
			self.comboNombre.setCurrentIndex(0)
			self.comboNombrePaciente.setCurrentIndex(0)
		else:
			self.comboNombre.setCurrentIndex(self.comboNombre.findText(item))
			self.comboNombrePaciente.setCurrentIndex(self.comboNombre.findText(item))

	def verHistorial(self):
		nombre = self.admArc.parsearCadena(self.comboNombrePaciente.currentText(), separador=' ')
		nombre = nombre[0]
		id = self.buscarId(nombre)
		id = str(id[0][0])
		historial = self.obtenerHistorial(id)
		if not historial:
			QtGui.QMessageBox.information(self, "Aviso",
				'El paciente seleccionado no cuenta con un historial.')	
			return
		print historial
		


	@property
	def comboCaso(self):
		return self._comboCaso

	@property
	def imagenCrear(self):
		return self._imagenCrear

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
	def comboNombre(self):
		return self._comboNombre

	@property
	def comboOrtodoncista(self):
		return self._comboOrtodoncista

	@property
	def txtComentario(self):
		return self._txtComentario

	@property
	def txtId(self):
		return self._txtId

	@property
	def btnProcesamiento(self):
		return self._btnProcesamiento

	@property
	def btnAgregarCasoAPaciente(self):
		return self._btnAgregarCasoAPaciente

	@property
	def btnVerHistorialBD(self):
		return self._btnVerHistorialBD

	@property 
	def btnCargarImagen(self):
		return self._btnCargarImagen

	@property
	def comboNombrePaciente(self):
		return self._comboNombrePaciente

	@property
	def txtIdCopia(self):
		return self._txtIdCopia


	

	
