
from PySide import QtGui, QtCore

from BASEDATOS.AreaBD import AreaBD
import CONSTANTES

class Area(QtGui.QWidget):
	def __init__(self, arr_con):
		super(Area, self).__init__()
		self.__arr_conexion = arr_con

		lblBuscador = QtGui.QLabel('Buscador: ', self)
		self._txtBuscador = QtGui.QLineEdit(self)

		self.ctrlZ = list()

		filas = 0
		self.__columnas = 1
		self.__encabezados = ['Areas']
		self._tablaArea = QtGui.QTableWidget(filas, self.__columnas)
		self.tablaArea.setHorizontalHeaderLabels(self.__encabezados)
		lista = self.obtenerDatosxColumna(columna='*')
		self.cargarDatos(lista)

		lblArea = QtGui.QLabel('Area:', self)
		self._txtArea = QtGui.QLineEdit(self)
		self._btnOk = QtGui.QPushButton('Ok', self)

		self._btnDeshacer = QtGui.QPushButton('Deshacer', self)
		self._btnAgregar = QtGui.QPushButton('Agregar area', self)
		self._btnEliminar = QtGui.QPushButton('Eliminar area', self)


		###contenedores
		parte1 = QtGui.QHBoxLayout()
		parte1.addStretch(1)
		parte1.addWidget(lblBuscador)
		parte1.addWidget(self.txtBuscador)

		parte3 = QtGui.QHBoxLayout()
		parte3.addStretch(1)
		parte3.addWidget(self._btnAgregar)
		parte3.addWidget(self._btnEliminar)

		parte2 = QtGui.QVBoxLayout()
		parte2.addLayout(parte1)
		parte2.addLayout(parte3)

		parte5 = QtGui.QHBoxLayout()
		parte5.addWidget(lblArea)
		parte5.addWidget(self._txtArea)
		parte5.addWidget(self._btnOk)

		cajaNuevaArea = QtGui.QGroupBox('Area a agregar')
		cajaNuevaArea.setLayout(parte5)

		unionArea = QtGui.QVBoxLayout()
		unionArea.addWidget(cajaNuevaArea)

		self._widgetAgregar = QtGui.QWidget()
		self.widgetAgregar.setLayout(unionArea)
		self.estado = False
		self.widgetAgregar.setVisible(self.estado)

		parte4 = QtGui.QVBoxLayout()
		parte4.addLayout(parte2)
		parte4.addWidget(self._widgetAgregar)

		cajaFiltro = QtGui.QGroupBox('Filtro')
		cajaFiltro.setLayout(parte4)

		union = QtGui.QVBoxLayout() # contnedor final
		union.addWidget(cajaFiltro)
		union.addWidget(self.tablaArea)

		self.wig = QtGui.QListWidget()
		self.wig.setLayout(union)

		self.inicializar()
		self.conexionesEventos()

	def inicializar(self):
		self.__valorBuscador = ''

	def conexionesEventos(self):
		self.btnOk.clicked[bool].connect(self.ok)
		self.btnAgregar.clicked[bool].connect(self.agregar)
		self.btnDeshacer.clicked[bool].connect(self.deshacer)
		self.btnEliminar.clicked[bool].connect(self.eliminar)
		self.txtBuscador.textChanged.connect(self.cambioBuscador)
		self.tablaArea.cellClicked.connect(self.presionoUnaCelda)
		self.tablaArea.itemChanged.connect(self.cambioValorCelda)

	def obtenerDatosxColumna(self, columna=''):
		re = AreaBD(self.__arr_conexion)
		lista = re.leer(columna)
		return lista

	def validarDato(self, dato):
		try:
			# validamos que el numero sea un numero
			dato = float(dato)
			return True
		except:
			return False

	def ok(self):
		# validar los campos de los registros
		nuevaArea = self.txtArea.text()
		# pegarle a la base de datos
		self.agregarRegistro(nuevaArea)
		self.actualizarTabla()
		self.limpiarCampos()

	def agregar(self):
		if not self.estado:
			self.estado = True
			self.btnAgregar.setStyleSheet('QPushButton {color: red}')
			self.btnAgregar.setText('CANCELAR')
		else:
			self.estado = False
			self.btnAgregar.setStyleSheet('QPushButton {color: black}')
			self.btnAgregar.setText('Agregar area')
			self.limpiarCampos()
		self.widgetAgregar.setVisible(self.estado)

	def limpiarCampos(self):
		self.txtArea.clear()

	def deshacer(self):
		# hacer un update del ultimo elemento de la lista
		if self.ctrlZ:
			ultimoMov = self.ctrlZ.pop(-1) # eliminamos el ultimo valor
			lista = list()
			for l in range(self.__columnas):
				if l!=ultimoMov[1]:
					lista.append(self._tablaArea.item(ultimoMov[0], l).text())
				else:
					lista.append(ultimoMov[3])
			self.actualizarRegistro(lista, ultimoMov[1], ultimoMov[2])
			self.actualizarTabla()
		else:
			QtGui.QMessageBox.information(self, 'Information', 'Ya no hay cambios que deshacer.')

	def eliminar(self):
		try: # validar que halla seleccionado una celda
			lista = list()
			for l in range(self.__columnas):
				lista.append(self.tablaArea.item(self.valorCeldaPresionada[0], l).text())
			MENSAJE='Desea eliminar el area: '+self.tablaArea.item(self.valorCeldaPresionada[0], 0).text()
			reply = QtGui.QMessageBox.question(self, 'Message', MENSAJE, \
						QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
			if reply==QtGui.QMessageBox.Yes:
				self.eliminarRegistro(lista)
				self.actualizarTabla()
		except:
			MENSAJE ='No se pudo completar la operacion.\n1.- Asegurese de haber seleccionado una area en la tabla.'
			QtGui.QMessageBox.critical(self, 'CRITICAL ERROR', MENSAJE, QtGui.QMessageBox.Abort)

	def crearCelda(self, var=''):
		var = str(var)
		item = QtGui.QTableWidgetItem()
		item.setText(var)
		return item

	def noEditable(self, item):
		item.setFlags(QtCore.Qt.ItemIsEnabled)
		return item

	def cargarDatos(self, datos):
		self.numeroAnteriorFilas = 0
		for indice, campos in enumerate(datos):
			self.tablaArea.insertRow(indice)
			self.tablaArea.setItem(indice, 0, self.noEditable(self.crearCelda(campos[0])))
			self.numeroAnteriorFilas += 1

	def removerDatos(self):
		self.tablaArea.clear()
		self.tablaArea.setHorizontalHeaderLabels(self.__encabezados)

	def removerFilas(self):
		while self.numeroAnteriorFilas > -1:
			self.tablaArea.removeRow(self.numeroAnteriorFilas)
			self.numeroAnteriorFilas -= 1

	def ejecutarQuery(self, query):
		re = AreaBD(self.__arr_conexion)
		lista = re.ejecutarQueryDinamico(query)
		return lista

	def armarQuery(self):
		inicio = 'SELECT * FROM '+CONSTANTES.areaBD
		coma = False
		self.query = inicio

		if len(self.__valorBuscador)==0:
			self.query = inicio
		else:    
			self.query += ' WHERE '+CONSTANTES.areaBD+ ' LIKE "%'+\
							self.__valorBuscador+'%"'
			coma = True	

	def actualizarTabla(self):
		self.armarQuery()
		# print 'DEBUG:', self.query		
		# actualizamos la tabla
		lista = self.ejecutarQuery(self.query)
		# remover datos y actualizar
		self.removerDatos()
		self.removerFilas()
		self.cargarDatos(lista) # cargamos los datos

	def cambioBuscador(self, nuevoTexto):
		self.__valorBuscador = nuevoTexto
		self.actualizarTabla()

	def presionoUnaCelda(self, f, c):
		self.valorCeldaPresionada = [f,c]
		self.valorOriginalTxt = self.tablaArea.item(f,c).text()
	
	def cambioValorCelda(self):
		# buscamos las coordenadas del item
		f = self.tablaArea.currentRow()
		c = self.tablaArea.currentColumn()
		
		columnasTipoNumero = [1,2]

		try: # es para no marcar error cuando se elimina/agrega un registro
			valorCeldaClickeada = self.tablaArea.item(f,c).text()
			if self.valorOriginalTxt!=valorCeldaClickeada:
				# validar que sea una modificacion valida
				if c in columnasTipoNumero:
					if self.validarDato(valorCeldaClickeada):
						lista = list()
						for l in range(self.__columnas):
							if l!=c:
								lista.append(self.tablaArea.item(f, l).text())
							else:
								lista.append(self.valorOriginalTxt)
						self.actualizarRegistro(lista, c, valorCeldaClickeada)
						self.ctrlZ.append([f, c, self.valorOriginalTxt, valorCeldaClickeada])
					else:
						QtGui.QMessageBox.information(self, 'Information',\
									 'No se hizo la modificacion. Dato invalido.')
						# regresar al valor que tenia
						it = QtGui.QTableWidgetItem()
						it.setText(self.valorOriginalTxt)
						self.tablaArea.setItem(f, c, it)
				else:
					lista = list()
					for l in range(self.__columnas):
						if l!=c:
							lista.append(self.tablaArea.item(f, l).text())
						else:
							lista.append(self.valorOriginalTxt)
					self.actualizarRegistro(lista, c, valorCeldaClickeada)
					self.ctrlZ.append([f, c, self.valorOriginalTxt, valorCeldaClickeada])
		except:
			pass

	def agregarRegistro(self, area):
		herr = AreaBD(self.__arr_conexion)
		herr.area = area
		herr.agregar()

	def eliminarRegistro(self, lista):
		herr = AreaBD(self.__arr_conexion)
		herr.area = lista[0]
		herr.borrar()

	def actualizarRegistro(self, lista, c, nuevoValor):
		herr = AreaBD(self.__arr_conexion)
		# es donde el encabezado no tiene el mismo nombre que la columna de la tabla
		if c!=2:
			columna = self.__encabezados[c]
		else:
			columna = 'precio'

		herr.nombre = ('', str(lista[0]))[lista[0]!='']
		herr.cantidad = lista[1]
		herr.precio = lista[2]
		herr.actualizar(columna, nuevoValor)


	@property
	def txtBuscador(self):
		return self._txtBuscador

	@property
	def tablaArea(self):
		return self._tablaArea

	@property
	def btnDeshacer(self):
		return self._btnDeshacer

	@property
	def btnAgregar(self):
		return self._btnAgregar

	@property
	def btnEliminar(self):
		return self._btnEliminar

	@property
	def txtArea(self):
		return self._txtArea

	@property
	def txtPiezas(self):
		return self._txtPiezas

	@property
	def txtPrecio(self):
		return self._txtPrecio

	@property
	def btnOk(self):
		return self._btnOk

	@property
	def widgetAgregar(self):
		return self._widgetAgregar


		

