from PySide import QtGui, QtCore

from BASEDATOS.OrtodoncistaBD import OrtodoncistaBD
from BASEDATOS.AreaBD import AreaBD
import CONSTANTES

# leer las herramienta de la base de datos y 

class Ortodoncista(QtGui.QWidget):
	def __init__(self, arr_con):
		super(Ortodoncista, self).__init__()
		self.__arr_conexion = arr_con
		self.ctrlZ = list()

		lblNombre = QtGui.QLabel('Nombre: ', self)
		self._txtNombre = QtGui.QLineEdit(self)

		lblPaterno = QtGui.QLabel('Ap. paterno: ')
		self._txtPaterno = QtGui.QLineEdit(self)

		lblMaterno = QtGui.QLabel('Ap. materno: ')
		self._txtMaterno = QtGui.QLineEdit(self)

		self.__txtDefaultArea = 'Seleccione un area...'
		self._comboArea = QtGui.QComboBox(self)
		self.comboArea.addItem(self.__txtDefaultArea)

		self._btnDeshacer = QtGui.QPushButton('Deshacer', self)
		self._btnAgregar = QtGui.QPushButton('Agregar ortodoncista', self)
		self._btnBuscar = QtGui.QPushButton('Buscar ortodoncista', self)
		self._btnEliminar = QtGui.QPushButton('Eliminar ortodoncista', self)
		self._btnOk = QtGui.QPushButton('Ok', self)

		filas = 0
		self.__columnas = 5
		self.__encabezados = ['Nombre', 'Ap. paterno', 'Ap. materno', 'Telefono', 'Area']
		self._listaR = QtGui.QTableWidget(filas, self.__columnas)
		self.listaR.setHorizontalHeaderLabels(self.__encabezados)
		lista = self.obtenerDatosXColumna(columna='*', tabla='ortodoncista')
		self.cargarDatos(lista)

		lblNewNombre = QtGui.QLabel('Nombre*: ', self)
		self._txtNewNombre = QtGui.QLineEdit(self)
		lblNewPaterno = QtGui.QLabel('Ap. paterno*: ', self)
		self._txtNewPaterno = QtGui.QLineEdit(self)
		lblNewMaterno = QtGui.QLabel('Ap. materno*: ', self)
		self._txtNewMaterno = QtGui.QLineEdit(self)
		lblNewTelefono = QtGui.QLabel('Telefono*: ', self)
		self._txtNewTelefono = QtGui.QLineEdit(self)
		lblNewArea = QtGui.QLabel('Area*: ', self)
		self._comboNewArea = QtGui.QComboBox(self)
	
		self.cargarDatosArea()

		####### contenedores
		campoBotones = QtGui.QHBoxLayout()
		campoBotones.addStretch(1)
		campoBotones.addWidget(self.btnAgregar)
		campoBotones.addWidget(self.btnBuscar)
		campoBotones.addWidget(self.btnEliminar)
		campoBotones.addWidget(self.btnDeshacer)

		campoImprovistoP1 = QtGui.QVBoxLayout()
		campoImprovistoP1.addWidget(lblNewNombre)
		campoImprovistoP1.addWidget(self.txtNewNombre)
		campoImprovistoP1.addWidget(lblNewPaterno)
		campoImprovistoP1.addWidget(self.txtNewPaterno)
		campoImprovistoP1.addWidget(lblNewMaterno)
		campoImprovistoP1.addWidget(self.txtNewMaterno)
		campoImprovistoP1.addWidget(lblNewTelefono)
		campoImprovistoP1.addWidget(self.txtNewTelefono)
		campoImprovistoP1.addWidget(lblNewArea)
		campoImprovistoP1.addWidget(self.comboNewArea)
		campoImprovistoP1.addStretch(1)
		
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

		filtro = QtGui.QHBoxLayout()
		filtro.addWidget(lblNombre)
		filtro.addWidget(self.txtNombre)
		filtro.addWidget(lblPaterno)
		filtro.addWidget(self.txtPaterno)
		filtro.addWidget(lblMaterno)
		filtro.addWidget(self.txtMaterno)
		filtro.addWidget(self.comboArea)

		vert = QtGui.QVBoxLayout()
		vert.addLayout(filtro)

		cajaBuscar = QtGui.QGroupBox('Filtro')
		cajaBuscar.setLayout(vert)

		unionBuscarEmpleado = QtGui.QVBoxLayout()
		unionBuscarEmpleado.addWidget(cajaBuscar)	

		self._widgetAgregar = QtGui.QWidget()
		self.widgetAgregar.setLayout(unionAgregarEmpleado)
		self.estado = False
		self.widgetAgregar.setVisible(self.estado)

		self._widgetBuscar = QtGui.QWidget()
		self.widgetBuscar.setLayout(unionBuscarEmpleado)
		self.estadoBuscar = False
		self.widgetBuscar.setVisible(self.estadoBuscar)

		union = QtGui.QVBoxLayout()
		union.addLayout(campoBotones)
		union.addWidget(self.widgetAgregar)
		union.addWidget(self.widgetBuscar)

		cajaFiltro = QtGui.QGroupBox('Opciones')
		cajaFiltro.setLayout(union)

		unionFinal = QtGui.QVBoxLayout() # contenedor final
		unionFinal.addWidget(cajaFiltro)
		unionFinal.addWidget(self.listaR)

		self.wig = QtGui.QListWidget()
		self.wig.setLayout(unionFinal)

		self.inicializar()
		self.conexionesEventos()

	def actualizar():
		self.cargarDatosArea()

	def inicializar(self):
		self.__valorNombre = ''
		self.__valorPaterno = ''
		self.__valorMaterno = ''
	
	def conexionesEventos(self):
		self.btnOk.clicked[bool].connect(self.ok)
		self.listaR.cellClicked.connect(self.presionoUnaCelda)
		self.listaR.itemChanged.connect(self.cambioValorCelda)
		self.txtNombre.textChanged.connect(self.cambioNombre)
		self.txtPaterno.textChanged.connect(self.cambioPaterno)
		self.txtMaterno.textChanged.connect(self.cambioMaterno)
		self.btnAgregar.clicked[bool].connect(self.agregar)
		self.btnBuscar.clicked[bool].connect(self.buscar)
		self.btnDeshacer.clicked[bool].connect(self.deshacer)
		self.btnEliminar.clicked[bool].connect(self.eliminar)
		self.comboArea.currentIndexChanged.connect(self.cambioComboArea)

	def cambioComboArea(self):
		self.actualizarTabla()

	def cambioNombre(self, nuevoTexto):
		self.__valorNombre = nuevoTexto
		self.actualizarTabla()

	def cambioPaterno(self, nuevoTexto):
		self.__valorPaterno = nuevoTexto
		self.actualizarTabla()

	def cambioMaterno(self, nuevoTexto):
		self.__valorMaterno = nuevoTexto
		self.actualizarTabla()
	
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
		item.setFlags(QtCore.Qt.ItemIsEnabled)
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
		self.comboArea.clear()
		self.comboNewArea.clear()
		self.comboArea.addItem(self.__txtDefaultArea)
		self.comboNewArea.addItem(self.__txtDefaultArea)
		datos = self.obtenerDatosXColumna(columna='area', tabla='area')
		for i in datos:
			i = i[0]
			self.comboArea.addItem(i)
			self.comboNewArea.addItem(i)

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
		nuevoNombre = self.txtNewNombre.text()
		nuevoPaterno = self.txtNewPaterno.text()
		nuevoMaterno = self.txtNewMaterno.text()
		nuevoTelefono = self.txtNewTelefono.text()
		area = self.comboNewArea.currentText()

		# pegarle a la base de datos
		if len(nuevoNombre)!=0 and len(nuevoPaterno)!=0\
			 and len(nuevoMaterno)!=0 and area!=self.__txtDefaultArea:
			if self.validarDato(nuevoTelefono):
				self.agregarRegistro(
						nuevoNombre,
						nuevoPaterno,
						nuevoMaterno,
						nuevoTelefono,
						area
					)
				self.actualizarTabla()
				self.limpiarCampos(posicion="abajo")
			else:
				QtGui.QMessageBox.information(self, "Aviso",
						"El campo 'telefono' no tiene formato valido")
		else:
			QtGui.QMessageBox.information(self, "Aviso",
								      "Llene todos los campos.")

	def ejecutarQuery(self, query):
		re = OrtodoncistaBD(self.__arr_conexion)
		lista = re.ejecutarQueryDinamico(query)
		return lista

	def armarQuery(self):
		inicio = 'SELECT * FROM '+CONSTANTES.ortodoncistaBD
		coma = False
		self.query = inicio

		# if len(self.__valorId)==0:
		# 	self.query = inicio
		# else:    
		# 	self.query += ' WHERE '+CONSTANTES.columna1_PA+ ' LIKE "%'+self.__valorId+'%"'+' ORDER BY '+CONSTANTES.columna1_PA
		# 	coma = True

		if len(self.__valorNombre)==0:
			self.query = inicio
		else:
			self.query += ' WHERE '+CONSTANTES.columna2_PA+ ' LIKE "%'+self.__valorNombre+'%"'
			coma = True

		if len(self.__valorPaterno)!=0:
			if coma:
				self.query += ' AND '+CONSTANTES.columna3_PA+' LIKE "%'+self.__valorPaterno+'%"'
			else:    
				self.query += ' WHERE '+CONSTANTES.columna3_PA+ ' LIKE "%'+self.__valorPaterno+'%"'
				coma = True

		if len(self.__valorMaterno)!=0:
			if coma:
				self.query += ' AND '+CONSTANTES.columna4_PA+' LIKE "%'+self.__valorMaterno+'%"'
			else:    
				self.query += ' WHERE '+CONSTANTES.columna4_PA+ ' LIKE "%'+self.__valorMaterno+'%"'
				coma = True

		if self.comboArea.currentText()!=self.__txtDefaultArea:
			if coma:
				self.query += ' AND '+CONSTANTES.columna5_PA+' LIKE "%'+self.comboArea.currentText()+'%"'
			else:    
				self.query += ' WHERE '+CONSTANTES.columna5_PA+ ' LIKE "%'+self.comboArea.currentText()+'%"'
				coma = True

	def limpiarCampos(self, posicion="arriba"):
		if posicion=="arriba":
			self.txtNombre.clear()
			self.txtPaterno.clear()
			self.txtMaterno.clear()
		else:
			self.txtNewNombre.clear()
			self.txtNewPaterno.clear()
			self.txtNewMaterno.clear()
			self.txtNewTelefono.clear()
			self.comboNewArea.setCurrentIndex(0)

	def removerDatos(self):
		self.listaR.clear()
		self.listaR.setHorizontalHeaderLabels(self.__encabezados)

	def removerFilas(self):
		while self.numeroAnteriorFilas > -1:
			self.listaR.removeRow(self.numeroAnteriorFilas)
			self.numeroAnteriorFilas -= 1

	def actualizarTabla(self):
		self.armarQuery()
		print 'DEBUG:', self.query		
		# actualizamos la tabla
		lista = self.ejecutarQuery(self.query)
		print lista
		print '-.-.-.-.-.'
		# remover datos y actualizar
		self.removerDatos()
		self.removerFilas()
		self.cargarDatos(lista) # cargamos los datos

	def cambioValorCelda(self):
		# buscamos las coordenadas del item
		f = self.listaR.currentRow()
		c = self.listaR.currentColumn()
		
		columnasTipoNumero = [3]


		# try: # es para no marcar error cuando se elimina/agrega un registro
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
					self.ctrlZ.append([f, c, self.__valorOriginalTxt, valorCeldaClickeada])
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
				self.ctrlZ.append([f, c, self.__valorOriginalTxt, valorCeldaClickeada])
		# except:
		# 	pass

	def agregarRegistro(self, *lista):
		herr = OrtodoncistaBD(self.__arr_conexion)
		herr.nombre = lista[0]
		herr.apPaterno = lista[1]
		herr.apMaterno = lista[2]
		herr.telefono = lista[3]
		herr.area = lista[4]
		herr.agregar()

	def eliminarRegistro(self, lista):
		print lista
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
			self.limpiarCampos(posicion="abajo")
		self.widgetAgregar.setVisible(self.estado)

	def buscar(self):
		if not self.estadoBuscar:
			self.estadoBuscar = True
			self.btnBuscar.setStyleSheet('QPushButton {color: red}')
			self.btnBuscar.setText('Ocultar busqueda')
		else:
			self.estadoBuscar = False
			self.btnBuscar.setStyleSheet('QPushButton {color: black}')
			self.btnBuscar.setText('Buscar ortodoncista')
			self.limpiarCampos(posicion="arriba")
		self.widgetBuscar.setVisible(self.estadoBuscar)

	def deshacer(self):
		# hacer un update del ultimo elemento de la lista
		if self.ctrlZ:
			ultimoMov = self.ctrlZ.pop(-1) # eliminamos el ultimo valor
			lista = list()
			for l in range(self.__columnas):
				if l!=ultimoMov[1]:
					lista.append(self.listaR.item(ultimoMov[0], l).text())
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



	@property
	def listaR(self):
		return self._listaR	

	@property
	def txtNombre(self):
		return self._txtNombre

	@property
	def txtPaterno(self):
		return self._txtPaterno

	@property
	def txtMaterno(self):
		return self._txtMaterno

	@property
	def txtNewNombre(self):
		return self._txtNewNombre

	@property
	def txtNewPaterno(self):
		return self._txtNewPaterno

	@property
	def txtNewMaterno(self):
		return self._txtNewMaterno

	@property
	def txtNewTelefono(self):
		return self._txtNewTelefono

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
	def btnOk(self):
		return self._btnOk

	@property
	def widgetAgregar(self):
		return self._widgetAgregar

	@property
	def widgetBuscar(self):
		return self._widgetBuscar

	@property
	def btnBuscar(self):
		return self._btnBuscar

	@property
	def comboArea(self):
		return self._comboArea

	@property
	def comboNewArea(self):
		return self._comboNewArea

	

	

	
