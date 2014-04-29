
from PySide import QtGui, QtCore

from BASEDATOS.PacienteBD import PacienteBD
from UTILERIAS.AdministradorArchivos import AdministradorArchivos

import CONSTANTES


class Paciente(QtGui.QWidget):
	def __init__(self, arr_con):
		super(Paciente, self).__init__()
		self.__arr_conexion = arr_con

		self.util = AdministradorArchivos()

		self._btnAgregar = QtGui.QPushButton('Agregar paciente', self)
		self._txtBuscar = QtGui.QLineEdit()
		self.txtBuscar.setPlaceholderText('Busqueda')
		self.txtBuscar.setStyleSheet(CONSTANTES.campos)

		self._btnEliminar = QtGui.QPushButton('Eliminar paciente', self)
		self._btnOk = QtGui.QPushButton('Ok', self)

		filas = 0
		self.__columnas = 5
		self.__encabezados = ['Id', 'Nombre', 'Ap. paterno', 'Ap. materno', 'Telefono']
		self._listaR = QtGui.QTableWidget(filas, self.__columnas)
		self.listaR.setHorizontalHeaderLabels(self.__encabezados)
		lista = self.obtenerDatosxColumna(columna='*')
		self.cargarDatos(lista)

		self._txtNuevoNombre = QtGui.QLineEdit(self)
		self.txtNuevoNombre.setPlaceholderText('* Nombre(s)')
		self.txtNuevoNombre.setStyleSheet(CONSTANTES.campos)
		
		self._txtNuevoPaterno = QtGui.QLineEdit(self)
		self.txtNuevoPaterno.setPlaceholderText('* Ap. paterno')
		self.txtNuevoPaterno.setStyleSheet(CONSTANTES.campos)
		
		self._txtNuevoMaterno = QtGui.QLineEdit(self)
		self.txtNuevoMaterno.setPlaceholderText('* Ap. materno')
		self.txtNuevoMaterno.setStyleSheet(CONSTANTES.campos)

		lblNuevoTelefono = QtGui.QLabel('* Telefono:')
		self._txtNuevoTelefono = QtGui.QLineEdit(self)
		self.txtNuevoTelefono.setInputMask('+9999999999;_')
		self.txtNuevoTelefono.setStyleSheet(CONSTANTES.campos)
	
		####### Contenedores
		campoBotones = QtGui.QHBoxLayout()
		campoBotones.addWidget(self.btnAgregar)
		campoBotones.addWidget(self.btnEliminar)
		campoBotones.addStretch(1)
		campoBotones.addWidget(self.txtBuscar)

		campoTelefono = QtGui.QHBoxLayout()
		campoTelefono.addWidget(lblNuevoTelefono)
		campoTelefono.addWidget(self.txtNuevoTelefono)
		
		campoImprovistoP1 = QtGui.QVBoxLayout()
		campoImprovistoP1.addWidget(self.txtNuevoNombre)
		campoImprovistoP1.addWidget(self.txtNuevoPaterno)
		campoImprovistoP1.addWidget(self.txtNuevoMaterno)
		campoImprovistoP1.addLayout(campoTelefono)
		
		camposImprovistoUnion = QtGui.QHBoxLayout()
		camposImprovistoUnion.addLayout(campoImprovistoP1)
		
		camposOk = QtGui.QHBoxLayout()
		camposOk.addStretch(1)
		camposOk.addWidget(self.btnOk)

		campoUnionOkConcamposImprovistoUnion = QtGui.QVBoxLayout()
		campoUnionOkConcamposImprovistoUnion.addLayout(camposImprovistoUnion)
		campoUnionOkConcamposImprovistoUnion.addLayout(camposOk)

		cajaAgregarPaciente = QtGui.QGroupBox('Datos del nuevo paciente')
		cajaAgregarPaciente.setLayout(campoUnionOkConcamposImprovistoUnion)

		unionAgregarEmpleado = QtGui.QVBoxLayout()
		unionAgregarEmpleado.addWidget(cajaAgregarPaciente)		
	
		self._widgetAgregar = QtGui.QWidget()
		self.widgetAgregar.setLayout(unionAgregarEmpleado)
		self.estado = False
		self.widgetAgregar.setVisible(self.estado)

		union = QtGui.QVBoxLayout()
		union.addLayout(campoBotones)
		union.addWidget(self.widgetAgregar)
		# union.addWidget(self.widgetBuscar)

		cajaFiltro = QtGui.QGroupBox('Opciones')
		cajaFiltro.setLayout(union)

		unionFinal = QtGui.QVBoxLayout() # contenedor final
		unionFinal.addWidget(cajaFiltro)
		unionFinal.addWidget(self.listaR)

		self.wig = QtGui.QListWidget()
		self.wig.setLayout(unionFinal)

		self.inicializar()
		self.conexionesEventos()

	def actualizar(self):
		self.txtBuscar.clear()
	
	def actualizarRegistro(self, lista, c, nuevoValor):
		emp = PacienteBD(self.__arr_conexion)
		
		nombreColumnasReales={
			0:'id',
			1:'nombre',
			2:'apPaterno',
			3:'apMaterno',
			4:'fechaNacimiento',
			5:'domicilio',
			6:'telefono',
			7:'celular'
		}
		
		columna = nombreColumnasReales[c]
		emp.id = lista[0]
		emp.nombre = lista[1]
		emp.apPaterno = lista[2]
		emp.apMaterno = lista[3]
		emp.actualizar(columna, nuevoValor)

	def actualizarTabla(self):
		self.armarQuery()
		# print 'DEBUG:', self.query		
		# actualizamos la tabla
		lista = self.ejecutarQuery(self.query)
		# remover datos y actualizar
		self.removerDatos()
		self.removerFilas()
		self.cargarDatos(lista) # cargamos los datos

	def agregar(self):
		if not self.estado:
			self.estado = True
			self.btnAgregar.setStyleSheet('QPushButton {color: red}')
			self.btnAgregar.setText('CANCELAR')
		else:
			self.estado = False
			self.btnAgregar.setStyleSheet('QPushButton {color: black}')
			self.btnAgregar.setText('Agregar paciente')
			self.limpiarCampos()
		self.widgetAgregar.setVisible(self.estado)

	def agregarRegistro(self, *lista):
		herr = PacienteBD(self.__arr_conexion)
		
		herr.id = lista[0]
		herr.nombre = lista[1]
		herr.apPaterno = lista[2]
		herr.apMaterno = lista[3]
		herr.telefono = lista[4]
		herr.agregar()

	def armarQuery(self):
		inicio = 'SELECT * FROM '+CONSTANTES.pacienteBD
		self.query = inicio

		if len(self.__valorBuscador)==0:
			self.query = inicio
		else:    
			self.query += ' WHERE '+CONSTANTES.columna1_PA+ ' LIKE "%'+self.__valorBuscador+'%"'+\
					' OR '+CONSTANTES.columna2_PA+ ' LIKE "%'+self.__valorBuscador+'%"'+\
					' OR '+CONSTANTES.columna3_PA+ ' LIKE "%'+self.__valorBuscador+'%"'+\
					' OR '+CONSTANTES.columna4_PA+ ' LIKE "%'+self.__valorBuscador+'%"'
					

	def cambioBuscador(self, nuevoTexto):
		self.__valorBuscador = nuevoTexto
		self.actualizarTabla()

	def cambioValorCelda(self):
		# buscamos las coordenadas del item
		f = self.listaR.currentRow()
		c = self.listaR.currentColumn()
		
		columnasTipoNumero = [4]

		try: # es para no marcar error cuando se elimina/agrega un registro
			valorCeldaClickeada = self.listaR.item(f,c).text()
			if self.__valorOriginalTxt!=valorCeldaClickeada:
				# validar que sea una modificacion valida
				if c in columnasTipoNumero:
					if self.validarDato(valorCeldaClickeada):
						lista = list()
						for l in range(self.__columnas):
							if l!=c:
								lista.append(self.listaR.item(f, l).text())
							else:
								lista.append(self.__valorOriginalTxt)
						self.actualizarRegistro(lista, c, valorCeldaClickeada)
						# self.ctrlZ.append([f, c, self.__valorOriginalTxt, valorCeldaClickeada])
					else:
						QtGui.QMessageBox.information(self, 'Information',\
									 'No se hizo la modificacion. Esta columna solo acepta datos numericos.')
						# regresar al valor que tenia
						it = QtGui.QTableWidgetItem()
						it.setText(self.__valorOriginalTxt)
						self.listaR.setItem(f, c, it)
				else:
					lista = list()
					for l in range(self.__columnas):
						if l!=c:
							lista.append(self.listaR.item(f, l).text())
						else:
							lista.append(self.__valorOriginalTxt)
					self.actualizarRegistro(lista, c, valorCeldaClickeada)
					# self.ctrlZ.append([f, c, self.__valorOriginalTxt, valorCeldaClickeada])
		except:
			pass

	def cargarDatos(self, datos):
		self.numeroAnteriorFilas = 0
		for indice, campos in enumerate(datos):
			self.listaR.insertRow(indice)
			self.listaR.setItem(indice, 0, self.noEditable(self.crearCelda(campos[0])))
			self.listaR.setItem(indice, 1, self.crearCelda(campos[1]))
			self.listaR.setItem(indice, 2, self.crearCelda(campos[2]))
			self.listaR.setItem(indice, 3, self.crearCelda(campos[3]))
			self.listaR.setItem(indice, 4, self.crearCelda(campos[4]))
			self.numeroAnteriorFilas += 1

	def crearCelda(self, var=''):
		var = str(var)
		item = QtGui.QTableWidgetItem()
		item.setText(var)
		return item
	
	def conexionesEventos(self):
		self.btnOk.clicked[bool].connect(self.ok)
		self.listaR.cellClicked.connect(self.presionoUnaCelda)
		self.listaR.itemChanged.connect(self.cambioValorCelda)
		self.btnAgregar.clicked[bool].connect(self.agregar)
		self.btnEliminar.clicked[bool].connect(self.eliminar)
		self.txtBuscar.textChanged.connect(self.cambioBuscador)

	def eliminar(self):
		try: # validar que halla seleccionado una celda
			lista = list()
			for l in range(self.__columnas):
				lista.append(self.listaR.item(self.valorCeldaPresionada[0], l).text())
			MENSAJE="Desea eliminar el siguiente registro:\nId: "+\
			self.listaR.item(self.valorCeldaPresionada[0], 0).text()+\
			"\nNombre: "+self.listaR.item(self.valorCeldaPresionada[0], 1).text()+\
			"\nAp. paterno: "+self.listaR.item(self.valorCeldaPresionada[0], 2).text()+\
			"\nAp. materno: "+self.listaR.item(self.valorCeldaPresionada[0], 3).text()
			reply = QtGui.QMessageBox.question(self, 'Message', MENSAJE, \
						QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
			if reply==QtGui.QMessageBox.Yes:
				self.eliminarRegistro(lista)
				self.actualizarTabla()
		except:
			MENSAJE ='No se pudo completar la operacion.\n1.- Asegurese de haber seleccionado un paciente en la tabla.'
			QtGui.QMessageBox.critical(self, 'CRITICAL ERROR', MENSAJE,
				 QtGui.QMessageBox.Abort)

	def eliminarRegistro(self, lista):
		herr = PacienteBD(self.__arr_conexion)
		
		herr.id = lista[0]
		herr.nombre = lista[1]
		herr.apPaterno = lista[2]
		herr.apMaterno = lista[3]
		herr.telefono = lista[4]
		herr.ortodoncista = ''
		herr.casoActual = ''
		herr.rutaImagen = ''

		herr.borrar()

	def ejecutarQuery(self, query):
		re = PacienteBD(self.__arr_conexion)
		lista = re.ejecutarQueryDinamico(query)
		return lista

	def generarId(self, nuevoNombre, nuevoPaterno, nuevoMaterno):
		lp = self.recorte(ord(nuevoNombre[0]))
		lmp = self.recorte(ord(nuevoNombre[len(nuevoNombre)/2]))
		lpp = self.recorte(ord(nuevoPaterno[0]))
		lmm = self.recorte(ord(nuevoMaterno[len(nuevoMaterno)/2]))

		return int(str(lp) + str(lmm) + str(lmp) + str(lpp))

	def inicializar(self):
		self.__valorBuscador = ''

	def limpiarCampos(self):
		self.txtNuevoNombre.clear()
		self.txtNuevoPaterno.clear()
		self.txtNuevoMaterno.clear()
		self.txtNuevoTelefono.clear()

	def noEditable(self, item):
		item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
		return item

	def obtenerDatosxColumna(self, columna=''):
		re = PacienteBD(self.__arr_conexion)
		lista = re.leer(columna)
		return lista

	def ok(self):
		if self.validarCampo(self.txtNuevoNombre.text()) and\
		 self.validarCampo(self.txtNuevoPaterno.text()) and\
		 self.validarCampo(self.txtNuevoMaterno.text()) and\
		 self.validarCampo(self.txtNuevoTelefono.text()):

			nuevoNombre = self.txtNuevoNombre.text()
			nuevoPaterno = self.txtNuevoPaterno.text()
			nuevoMaterno = self.txtNuevoMaterno.text()
			nuevoId = self.generarId(nuevoNombre, nuevoPaterno, nuevoMaterno)
			nuevoTelefono = self.txtNuevoTelefono.text()

			nuevoTelefono = self.util.eliminarPrimerCaracter(nuevoTelefono)

			if self.validarDato(nuevoId):
				# pegarle a la base de datos
				self.agregarRegistro(nuevoId,
						nuevoNombre,
						nuevoPaterno,
						nuevoMaterno,
						nuevoTelefono,
					)
				QtGui.QMessageBox.information(self, 'Information',
					'El Id para el paciente "'+nuevoNombre+' " es "'+str(nuevoId)+ '".')
				self.actualizarTabla()
				self.limpiarCampos()

			else:
				MENSAJE = 'No se pudo completar la operacion.\n1.- Asegurese de haber agregado datos correctos.'
				QtGui.QMessageBox.critical(self, 'CRITICAL ERROR', MENSAJE, 
					QtGui.QMessageBox.Abort)
		else:
			MENSAJE ='No se pudo completar la operacion.\n1.- Asegurese de tener todos los campos llenos.'
			QtGui.QMessageBox.critical(self, 'CRITICAL ERROR', MENSAJE, 
				QtGui.QMessageBox.Abort)

	def orgnizarDato(self, dato):
		# recibe: 01 - 01 - 2000
		# y debe ser: 2000-01-01
		dato = str(dato)
		dato = dato.replace(' ', '').split('-')
		largo = len(dato)-1

		cadena = ''
		for i in range(largo, (largo-largo)-1, -1):
			cadena += dato[i]+'-'
		cadena = cadena[:-1]
		return cadena

	def parsearFecha(self, cadena):
		try:
			(ano, mes, dia) = cadena.split("-")
			if int(ano)>0 and int(mes)>0 and int(mes)<13 and int(dia)>0 and int(dia)<32:
				return True
			else:
				return False
		except:
			return False

	def presionoUnaCelda(self, f, c):
		self.valorCeldaPresionada = [f,c]
		self.__valorOriginalTxt = self.listaR.item(f,c).text()

	def recorte(self, valor):
		valor = str(valor)
		nuevoValor = 0
		for n in valor:
			nuevoValor+=int(n) 
		if len(str(nuevoValor))!=1:
			return self.recorte(nuevoValor)
		else:
			return nuevoValor

	def removerDatos(self):
		self.listaR.clear()
		self.listaR.setHorizontalHeaderLabels(self.__encabezados)

	def removerFilas(self):
		while self.numeroAnteriorFilas > -1:
			self.listaR.removeRow(self.numeroAnteriorFilas)
			self.numeroAnteriorFilas -= 1

	def validarCampo(self, campo):
		if len(campo)!=0:
			return True
		return False

	def validarDato(self, dato):
		try:
			# validamos que el numero sea un numero
			dato = int(dato)
			return True
		except:
			return False




	@property
	def listaR(self):
		return self._listaR	

	@property
	def txtNuevoNombre(self):
		return self._txtNuevoNombre

	@property
	def txtNuevoPaterno(self):
		return self._txtNuevoPaterno

	@property
	def txtNuevoMaterno(self):
		return self._txtNuevoMaterno

	@property
	def txtNuevoTelefono(self):
		return self._txtNuevoTelefono

	@property
	def btnAgregar(self):
		return self._btnAgregar

	@property
	def btnEliminar(self):
		return self._btnEliminar

	@property
	def btnOk(self):
		return self._btnOk

	@property
	def widgetAgregar(self):
		return self._widgetAgregar

	@property
	def txtBuscar(self):
		return self._txtBuscar
	
