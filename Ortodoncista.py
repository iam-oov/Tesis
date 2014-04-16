
from PySide import QtGui, QtCore

from BASEDATOS.AreaBD import AreaBD
from BASEDATOS.OrtodoncistaBD import OrtodoncistaBD
from UTILERIAS.AdministradorArchivos import AdministradorArchivos

import CONSTANTES


class Ortodoncista(QtGui.QWidget):
	def __init__(self, arr_con):
		super(Ortodoncista, self).__init__()
		self.__arr_conexion = arr_con

		self.util = AdministradorArchivos()
		
		self._btnAgregar = QtGui.QPushButton('Agregar ortodoncista', self)
		self._btnEliminar = QtGui.QPushButton('Eliminar ortodoncista', self)
		self._btnOk = QtGui.QPushButton('Ok', self)

		self._txtBuscar = QtGui.QLineEdit()
		self.txtBuscar.setPlaceholderText('Busqueda')
		self.txtBuscar.setStyleSheet(CONSTANTES.campos)

		filas = 0
		self.__columnas = 5
		self.__encabezados = ['Nombre', 'Ap. paterno', 'Ap. materno', 'Telefono', 'Area']
		self._listaR = QtGui.QTableWidget(filas, self.__columnas)
		self.listaR.setHorizontalHeaderLabels(self.__encabezados)
		lista = self.obtenerDatosXColumna(columna='*', tabla='ortodoncista')
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
		
		self.__txtDefaultArea = 'Seleccione una...'
		lblNuevoArea = QtGui.QLabel('* Area:')
		self._comboNuevoArea = QtGui.QComboBox(self)
		self.cargarDatosArea()

		####### CONTENEDORES

		campoBotones = QtGui.QHBoxLayout()
		campoBotones.addWidget(self.btnAgregar)
		campoBotones.addWidget(self.btnEliminar)
		campoBotones.addStretch(1)
		campoBotones.addWidget(self.txtBuscar)

		campoTelefono = QtGui.QHBoxLayout()
		campoTelefono.addWidget(lblNuevoTelefono)
		campoTelefono.addWidget(self.txtNuevoTelefono)

		campoArea = QtGui.QHBoxLayout()
		campoArea.addWidget(lblNuevoArea)
		campoArea.addWidget(self.comboNuevoArea)
		campoArea.addStretch(1)

		campoImprovistoP1 = QtGui.QVBoxLayout()
		campoImprovistoP1.addWidget(self.txtNuevoNombre)
		campoImprovistoP1.addWidget(self.txtNuevoPaterno)
		campoImprovistoP1.addWidget(self.txtNuevoMaterno)
		campoImprovistoP1.addLayout(campoTelefono)
		campoImprovistoP1.addLayout(campoArea)
		
		camposImprovistoUnion = QtGui.QHBoxLayout()
		camposImprovistoUnion.addLayout(campoImprovistoP1)
		
		camposOk = QtGui.QHBoxLayout()
		camposOk.addStretch(1)
		camposOk.addWidget(self.btnOk)

		campoUnionOkConcamposImprovistoUnion = QtGui.QVBoxLayout()
		campoUnionOkConcamposImprovistoUnion.addLayout(camposImprovistoUnion)
		campoUnionOkConcamposImprovistoUnion.addLayout(camposOk)

		cajaAgregarOrtodoncista = QtGui.QGroupBox('Datos del nuevo ortodoncista')
		cajaAgregarOrtodoncista.setLayout(campoUnionOkConcamposImprovistoUnion)

		unionAgregarEmpleado = QtGui.QVBoxLayout()
		unionAgregarEmpleado.addWidget(cajaAgregarOrtodoncista)		

		self._widgetAgregar = QtGui.QWidget()
		self.widgetAgregar.setLayout(unionAgregarEmpleado)
		self.estado = False
		self.widgetAgregar.setVisible(self.estado)

		union = QtGui.QVBoxLayout()
		union.addLayout(campoBotones)
		union.addWidget(self.widgetAgregar)

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
		self.cargarDatosArea()
		self.txtBuscar.clear()

	def inicializar(self):
		self.__valorBuscador = ''

	def cambioBuscador(self, nuevoTexto):
		self.__valorBuscador = nuevoTexto
		self.actualizarTabla()
	
	def conexionesEventos(self):
		self.btnOk.clicked[bool].connect(self.ok)
		self.listaR.cellClicked.connect(self.presionoUnaCelda)
		self.listaR.itemChanged.connect(self.cambioValorCelda)
		self.btnAgregar.clicked[bool].connect(self.agregar)
		self.btnEliminar.clicked[bool].connect(self.eliminar)
		self.txtBuscar.textChanged.connect(self.cambioBuscador)
	
	def obtenerDatosXColumna(self, columna='', tabla=''):
		if tabla==CONSTANTES.ortodoncistaBD:
			re = OrtodoncistaBD(self.__arr_conexion)
			lista = re.leer(columna)
			return lista
		elif tabla==CONSTANTES.areaBD:
			re = AreaBD(self.__arr_conexion)
			lista = re.leer(columna)
			return lista

	def crearCelda(self, var=''):
		var = str(var)
		item = QtGui.QTableWidgetItem()
		item.setText(var)
		return item

	def noEditable(self, item):
		item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable) 
		return item

	def cargarDatos(self, datos):
		self.numeroAnteriorFilas = 0
		for indice, campos in enumerate(datos):
			self.listaR.insertRow(indice)
			self.listaR.setItem(indice, 0, self.crearCelda(campos[0]))
			self.listaR.setItem(indice, 1, self.crearCelda(campos[1]))
			self.listaR.setItem(indice, 2, self.crearCelda(campos[2]))
			self.listaR.setItem(indice, 3, self.crearCelda(campos[3]))
			self.listaR.setItem(indice, 4, self.noEditable(self.crearCelda(campos[4])))
			self.numeroAnteriorFilas += 1

	def cargarDatosArea(self):
		self.comboNuevoArea.clear()
		self.comboNuevoArea.addItem(self.__txtDefaultArea)
		
		datos = self.obtenerDatosXColumna(columna='area', tabla='area')
		for i in datos:
			i = i[0]
			self.comboNuevoArea.addItem(i)

	def generarId(self, nuevoNombre, nuevoPaterno, nuevoMaterno):
		lp = self.recorte(ord(nuevoNombre[0]))
		lmp = self.recorte(ord(nuevoNombre[len(nuevoNombre)/2]))
		lpp = self.recorte(ord(nuevoPaterno[0]))
		lmm = self.recorte(ord(nuevoMaterno[len(nuevoMaterno)/2]))

		return int(str(lp) + str(lmm) + str(lmp) + str(lpp))

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

	def validarDato(self, dato):
		try:
			# validamos que el numero sea un numero
			dato = int(dato)
			return True
		except:
			return False

	def ok(self):
		if self.validarCampo(self.txtNuevoNombre.text()) and\
		 self.validarCampo(self.txtNuevoPaterno.text()) and\
		 self.validarCampo(self.txtNuevoMaterno.text()) and\
		 self.validarCampo(self.txtNuevoTelefono.text()) and\
		 self.comboNuevoArea.currentText()!=self.__txtDefaultArea:

			nuevoNombre = self.txtNuevoNombre.text()
			nuevoPaterno = self.txtNuevoPaterno.text()
			nuevoMaterno = self.txtNuevoMaterno.text()
			area = self.comboNuevoArea.currentText()
			nuevoTelefono = self.txtNuevoTelefono.text()

			nuevoTelefono = self.util.eliminarPrimerCaracter(nuevoTelefono)

			self.agregarRegistro(
					nuevoNombre,
					nuevoPaterno,
					nuevoMaterno,
					nuevoTelefono,
					area
				)
			QtGui.QMessageBox.information(self, 'Information', 'Movimiento guardado.')
			self.actualizarTabla()
			self.limpiarCampos()

		else:
			MENSAJE ='No se pudo completar la operacion.\n1.- Asegurese de tener todos los campos llenos.'
			QtGui.QMessageBox.critical(self, 'CRITICAL ERROR', MENSAJE, 
				QtGui.QMessageBox.Abort)


	def ejecutarQuery(self, query):
		re = OrtodoncistaBD(self.__arr_conexion)
		lista = re.ejecutarQueryDinamico(query)
		return lista

	def armarQuery(self):
		inicio = 'SELECT * FROM '+CONSTANTES.ortodoncistaBD
		self.query = inicio

		if len(self.__valorBuscador)==0:
			self.query = inicio
		else:    
			self.query += ' WHERE '+CONSTANTES.columna2_PA+ ' LIKE "%'+self.__valorBuscador+'%"'+\
					' OR '+CONSTANTES.columna3_PA+ ' LIKE "%'+self.__valorBuscador+'%"'+\
					' OR '+CONSTANTES.columna4_PA+ ' LIKE "%'+self.__valorBuscador+'%"'+\
					' OR '+CONSTANTES.columna5_PA+ ' LIKE "%'+self.__valorBuscador+'%"'

	def limpiarCampos(self):
		self.txtNuevoNombre.clear()
		self.txtNuevoPaterno.clear()
		self.txtNuevoMaterno.clear()
		self.txtNuevoTelefono.clear()
		self.comboNuevoArea.setCurrentIndex(0)

	def removerDatos(self):
		self.listaR.clear()
		self.listaR.setHorizontalHeaderLabels(self.__encabezados)

	def removerFilas(self):
		while self.numeroAnteriorFilas > -1:
			self.listaR.removeRow(self.numeroAnteriorFilas)
			self.numeroAnteriorFilas -= 1

	def actualizarTabla(self):
		self.armarQuery()
		# print 'DEBUG:', self.query		
		# actualizamos la tabla
		lista = self.ejecutarQuery(self.query)
		# remover datos y actualizar
		self.removerDatos()
		self.removerFilas()
		self.cargarDatos(lista) # cargamos los datos

	def cambioValorCelda(self):
		# buscamos las coordenadas del item
		f = self.listaR.currentRow()
		c = self.listaR.currentColumn()
		
		columnasTipoNumero = [3]

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
									 'No se hizo la modificacion. Dato invalido.')
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

	def agregarRegistro(self, *lista):
		herr = OrtodoncistaBD(self.__arr_conexion)
		herr.nombre = lista[0]
		herr.apPaterno = lista[1]
		herr.apMaterno = lista[2]
		herr.telefono = lista[3]
		herr.area = lista[4]
		herr.agregar()

	def eliminarRegistro(self, lista):
		herr = OrtodoncistaBD(self.__arr_conexion)
		herr.nombre = lista[0]
		herr.apPaterno = lista[1]
		herr.apMaterno = lista[2]
		herr.telefono = lista[3]
		herr.area = lista[4]
		herr.borrar()

	def actualizarRegistro(self, lista, c, nuevoValor):
		emp = OrtodoncistaBD(self.__arr_conexion)
		
		nombreColumnasReales={
			0:CONSTANTES.columna2_PA,
			1:CONSTANTES.columna3_PA,
			2:CONSTANTES.columna4_PA,
			3:CONSTANTES.columna6_PA,
			4:CONSTANTES.columna5_PA
		}
		
		columna = nombreColumnasReales[c]
		emp.nombre = lista[0]
		emp.apPaterno = lista[1]
		emp.apMaterno = lista[2]
		emp.telefono = lista[3]
		emp.area = lista[4]
		emp.actualizar(columna, nuevoValor)


	def agregar(self):
		if not self.estado:
			self.estado = True
			self.btnAgregar.setStyleSheet('QPushButton {color: red}')
			self.btnAgregar.setText('CANCELAR')
		else:
			self.estado = False
			self.btnAgregar.setStyleSheet('QPushButton {color: black}')
			self.btnAgregar.setText('Agregar ortodoncista')
			self.limpiarCampos()
		self.widgetAgregar.setVisible(self.estado)

	def eliminar(self):
		try: # validar que halla seleccionado una celda
			lista = list()
			for l in range(self.__columnas):
				lista.append(self.listaR.item(self.valorCeldaPresionada[0], l).text())
			MENSAJE="Desea eliminar el siguiente registro:\nNombre: "+\
			self.listaR.item(self.valorCeldaPresionada[0], 0).text()+\
			"\nAp. paterno: "+self.listaR.item(self.valorCeldaPresionada[0], 1).text()+\
			"\nAp. materno: "+self.listaR.item(self.valorCeldaPresionada[0], 2).text()
			reply = QtGui.QMessageBox.question(self, 'Message', MENSAJE, \
						QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
			if reply==QtGui.QMessageBox.Yes:
				self.eliminarRegistro(lista)
				self.actualizarTabla()
		except:
			MENSAJE ='No se pudo completar la operacion.\n1.- Asegurese de haber seleccionado un Ortodoncista en la tabla.'
			QtGui.QMessageBox.critical(self, 'CRITICAL ERROR', MENSAJE, QtGui.QMessageBox.Abort)

	def validarCampo(self, campo):
		if len(campo)!=0:
			return True
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
	def comboNuevoArea(self):
		return self._comboNuevoArea

	@property
	def txtBuscar(self):
		return self._txtBuscar

	

	

	

	
