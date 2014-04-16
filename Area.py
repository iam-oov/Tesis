
from PySide import QtGui, QtCore

from BASEDATOS.AreaBD import AreaBD
import CONSTANTES

class Area(QtGui.QWidget):
	def __init__(self, arr_con):
		super(Area, self).__init__()
		self.__arr_conexion = arr_con

		self._txtBuscar = QtGui.QLineEdit(self)
		self.txtBuscar.setPlaceholderText('Busqueda')
		self.txtBuscar.setStyleSheet(CONSTANTES.campos)

		filas = 0
		self.__columnas = 1
		self.__encabezados = ['Areas']
		self._tablaArea = QtGui.QTableWidget(filas, self.__columnas)
		self.tablaArea.setHorizontalHeaderLabels(self.__encabezados)
		lista = self.obtenerDatosxColumna(columna='*')
		self.cargarDatos(lista)

		# lblArea = QtGui.QLabel('Area:', self)
		self._txtArea = QtGui.QLineEdit(self)
		self.txtArea.setPlaceholderText('* Area')
		self.txtArea.setStyleSheet(CONSTANTES.campos)
		self._btnOk = QtGui.QPushButton('Ok', self)

		self._btnAgregar = QtGui.QPushButton('Agregar area', self)
		self._btnEliminar = QtGui.QPushButton('Eliminar area', self)

		####### Contenedores
		parte3 = QtGui.QHBoxLayout()
		parte3.addWidget(self.btnAgregar)
		parte3.addWidget(self.btnEliminar)
		parte3.addStretch(1)
		parte3.addWidget(self.txtBuscar)

		camposOk = QtGui.QHBoxLayout()
		camposOk.addStretch(1)
		camposOk.addWidget(self.btnOk)

		parte5 = QtGui.QVBoxLayout()
		parte5.addWidget(self.txtArea)
		parte5.addLayout(camposOk)

		cajaNuevaArea = QtGui.QGroupBox('Datos de la nueva area')
		cajaNuevaArea.setLayout(parte5)

		unionArea = QtGui.QVBoxLayout()
		unionArea.addWidget(cajaNuevaArea)

		self._widgetAgregar = QtGui.QWidget()
		self.widgetAgregar.setLayout(unionArea)
		self.estado = False
		self.widgetAgregar.setVisible(self.estado)

		parte4 = QtGui.QVBoxLayout()
		parte4.addLayout(parte3)
		parte4.addWidget(self.widgetAgregar)

		cajaFiltro = QtGui.QGroupBox('Filtro')
		cajaFiltro.setLayout(parte4)

		union = QtGui.QVBoxLayout() # contnedor final
		union.addWidget(cajaFiltro)
		union.addWidget(self.tablaArea)

		self.wig = QtGui.QListWidget()
		self.wig.setLayout(union)

		self.inicializar()
		self.conexionesEventos()

	def actualizar(self):
		self.txtBuscar.clear()

	def inicializar(self):
		self.__valorBuscador = ''

	def conexionesEventos(self):
		self.btnOk.clicked[bool].connect(self.ok)
		self.btnAgregar.clicked[bool].connect(self.agregar)
		self.btnEliminar.clicked[bool].connect(self.eliminar)
		self.tablaArea.cellClicked.connect(self.presionoUnaCelda)
		self.tablaArea.itemChanged.connect(self.cambioValorCelda)
		self.txtBuscar.textChanged.connect(self.cambioBuscador)

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
		if self.validarCampo(self.txtArea.text()):
			nuevaArea = self.txtArea.text()
			# pegarle a la base de datos
			self.agregarRegistro(nuevaArea)
			QtGui.QMessageBox.information(self, 'Information',
						'Movimiento guardado.')
			self.actualizarTabla()
			self.limpiarCampos()
		else:
			MENSAJE = 'No se pudo completar la operacion.\n1.- Asegurese de haber agregado datos correctos.'
			QtGui.QMessageBox.critical(self, 'CRITICAL ERROR', MENSAJE, 
					QtGui.QMessageBox.Abort)


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
		item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
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
		self.query = inicio

		if len(self.__valorBuscador)==0:
			self.query = inicio
		else:    
			self.query += ' WHERE '+CONSTANTES.areaBD+ ' LIKE "%'+self.__valorBuscador+'%"'
	
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
		

		try: # es para no marcar error cuando se elimina/agrega un registro
			valorCeldaClickeada = self.tablaArea.item(f,c).text()
			if self.valorOriginalTxt!=valorCeldaClickeada:
				lista = list()
				for l in range(self.__columnas):
					if l!=c:
						lista.append(self.tablaArea.item(f, l).text())
					else:
						lista.append(self.valorOriginalTxt)
				self.actualizarRegistro(lista, c, valorCeldaClickeada)
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

	def validarCampo(self, campo):
		if len(campo)!=0:
			return True
		return False


	@property
	def txtBuscar(self):
		return self._txtBuscar

	@property
	def tablaArea(self):
		return self._tablaArea

	# @property
	# def btnDeshacer(self):
	# 	return self._btnDeshacer

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


		

