from PySide import QtGui, QtCore

from BASEDATOS.PacienteBD import PacienteBD
import CONSTANTES

# leer las herramienta de la base de datos y 

class Paciente(QtGui.QWidget):
	def __init__(self, arr_con):
		super(Paciente, self).__init__()
		self.__arr_conexion = arr_con
		self.ctrlZ = list()

		lblId = QtGui.QLabel('Id: ', self)
		self._txtId = QtGui.QLineEdit(self)

		lblNombre = QtGui.QLabel('Nombre: ', self)
		self._txtNombre = QtGui.QLineEdit(self)

		lblPaterno = QtGui.QLabel('Ap. paterno: ')
		self._txtPaterno = QtGui.QLineEdit(self)

		lblMaterno = QtGui.QLabel('Ap. materno: ')
		self._txtMaterno = QtGui.QLineEdit(self)

		self._btnDeshacer = QtGui.QPushButton('Deshacer', self)
		self._btnAgregar = QtGui.QPushButton('Agregar paciente', self)
		self._btnBuscar = QtGui.QPushButton('Buscar paciente', self)
		self._btnEliminar = QtGui.QPushButton('Eliminar paciente', self)
		self._btnOk = QtGui.QPushButton('Ok', self)

		filas = 0
		self.__columnas = 5
		self.__encabezados = ['Id', 'Nombre', 'Ap. paterno', 'Ap. materno', 'Telefono']
		self._listaR = QtGui.QTableWidget(filas, self.__columnas)
		self.listaR.setHorizontalHeaderLabels(self.__encabezados)
		lista = self.obtenerDatosxColumna(columna='*')
		self.cargarDatos(lista)

		lblNewNombre = QtGui.QLabel('Nombre: ', self)
		self._txtNewNombre = QtGui.QLineEdit(self)
		lblNewPaterno = QtGui.QLabel('Ap. paterno: ', self)
		self._txtNewPaterno = QtGui.QLineEdit(self)
		lblNewMaterno = QtGui.QLabel('Ap. materno: ', self)
		self._txtNewMaterno = QtGui.QLineEdit(self)
		lblNewTelefono = QtGui.QLabel('Telefono: ', self)
		self._txtNewTelefono = QtGui.QLineEdit(self)
	
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
		campoImprovistoP1.addStretch(1)
		
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

		filtro = QtGui.QHBoxLayout()
		filtro.addWidget(lblId)
		filtro.addWidget(self.txtId)
		filtro.addWidget(lblNombre)
		filtro.addWidget(self.txtNombre)
		filtro.addWidget(lblPaterno)
		filtro.addWidget(self.txtPaterno)
		filtro.addWidget(lblMaterno)
		filtro.addWidget(self.txtMaterno)

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

	def inicializar(self):
		self.__valorId = ''
		self.__valorNombre = ''
		self.__valorPaterno = ''
		self.__valorMaterno = ''
	
	def conexionesEventos(self):
		self.btnOk.clicked[bool].connect(self.ok)
		self.listaR.cellClicked.connect(self.presionoUnaCelda)
		self.listaR.itemChanged.connect(self.cambioValorCelda)
		self.txtId.textChanged.connect(self.cambioId)
		self.txtNombre.textChanged.connect(self.cambioNombre)
		self.txtPaterno.textChanged.connect(self.cambioPaterno)
		self.txtMaterno.textChanged.connect(self.cambioMaterno)
		self.btnAgregar.clicked[bool].connect(self.agregar)
		self.btnBuscar.clicked[bool].connect(self.buscar)
		self.btnDeshacer.clicked[bool].connect(self.deshacer)
		self.btnEliminar.clicked[bool].connect(self.eliminar)

	def cambioId(self, nuevoTexto):
		self.__valorId = nuevoTexto
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
	
	def obtenerDatosxColumna(self, columna=''):
		re = PacienteBD(self.__arr_conexion)
		lista = re.leer(columna)
		return lista

	def crearCelda(self, var=''):
		var = str(var)
		item = QtGui.QTableWidgetItem()
		item.setText(var)
		return item

	def cargarDatos(self, datos):
		self.numeroAnteriorFilas = 0
		for indice, campos in enumerate(datos):
			self.listaR.insertRow(indice)
			self.listaR.setItem(indice, 0, self.crearCelda(campos[0]))
			self.listaR.setItem(indice, 1, self.crearCelda(campos[1]))
			self.listaR.setItem(indice, 2, self.crearCelda(campos[2]))
			self.listaR.setItem(indice, 3, self.crearCelda(campos[3]))
			self.listaR.setItem(indice, 4, self.crearCelda(campos[4]))
			self.numeroAnteriorFilas += 1

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

	def ok(self):
		nuevoNombre = self.txtNewNombre.text()
		nuevoPaterno = self.txtNewPaterno.text()
		nuevoMaterno = self.txtNewMaterno.text()
		nuevoId = self.generarId(nuevoNombre, nuevoPaterno, nuevoMaterno)
		print 'Id generado:', nuevoId
		nuevoTelefono = self.txtNewTelefono.text()

		if self.validarDato(nuevoId):
			# pegarle a la base de datos
			self.agregarRegistro(nuevoId,
					nuevoNombre,
					nuevoPaterno,
					nuevoMaterno,
					nuevoTelefono,
				)
			QtGui.QMessageBox.information(self, 'Information',\
									 'El Id para el paciente "'+nuevoNombre+'" es "'+str(nuevoId)+ '".')
			self.actualizarTabla()
			self.limpiarCampos(False)

		else:
			MENSAJE ='No se pudo completar la operacion.\n1.- Asegurese de haber agregado datos correctos.'
			QtGui.QMessageBox.critical(self, 'CRITICAL ERROR', MENSAJE, QtGui.QMessageBox.Abort)

	def ejecutarQuery(self, query):
		re = PacienteBD(self.__arr_conexion)
		lista = re.ejecutarQueryDinamico(query)
		return lista

	def armarQuery(self):
		inicio = 'SELECT * FROM '+CONSTANTES.pacienteBD
		coma = False
		self.query = inicio

		if len(self.__valorId)==0:
			self.query = inicio
		else:    
			self.query += ' WHERE '+CONSTANTES.columna1_PA+ ' LIKE "%'+self.__valorId+'%"'+' ORDER BY '+CONSTANTES.columna1_PA
			coma = True

		if len(self.__valorNombre)!=0:
			if coma:
				self.query += ' AND '+CONSTANTES.columna2_PA+' LIKE "%'+self.__valorNombre+'%"'+' ORDER BY '+CONSTANTES.columna2_PA
			else:    
				self.query += ' WHERE '+CONSTANTES.columna2_PA+ ' LIKE "%'+self.__valorNombre+'%"'+' ORDER BY '+CONSTANTES.columna2_PA
				coma = True

		if len(self.__valorPaterno)!=0:
			if coma:
				self.query += ' AND '+CONSTANTES.columna3_PA+' LIKE "%'+self.__valorPaterno+'%"'+' ORDER BY '+CONSTANTES.columna3_PA
			else:    
				self.query += ' WHERE '+CONSTANTES.columna3_PA+ ' LIKE "%'+self.__valorPaterno+'%"'+' ORDER BY '+CONSTANTES.columna3_PA
				coma = True

		if len(self.__valorMaterno)!=0:
			if coma:
				self.query += ' AND '+CONSTANTES.columna4_PA+' LIKE "%'+self.__valorMaterno+'%"'+' ORDER BY '+CONSTANTES.columna4_PA
			else:    
				self.query += ' WHERE '+CONSTANTES.columna4_PA+ ' LIKE "%'+self.__valorMaterno+'%"'+' ORDER BY '+CONSTANTES.columna4_PA
				coma = True

	def limpiarCampos(self, posicion="arriba"):
		if posicion=="arriba":
			self.txtId.clear()
			self.txtNombre.clear()
			self.txtPaterno.clear()
			self.txtMaterno.clear()
		else:
			self.txtNewNombre.clear()
			self.txtNewPaterno.clear()
			self.txtNewMaterno.clear()
			self.txtNewTelefono.clear()

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
		
		columnaTipoFecha = [4]
		columnasTipoNumero = [0]

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
						self.ctrlZ.append([f, c, self.__valorOriginalTxt, valorCeldaClickeada])
					else:
						QtGui.QMessageBox.information(self, 'Information',\
									 'No se hizo la modificacion. Dato invalido.')
						# regresar al valor que tenia
						it = QtGui.QTableWidgetItem()
						it.setText(self.__valorOriginalTxt)
						self.listaR.setItem(f, c, it)
				elif c in columnaTipoFecha:
					# print 'FECHA'
					# 1999-12-31
					if self.parsearFecha(valorCeldaClickeada):
						lista = list()
						for l in range(self.__columnas):
							if l!=c:
								lista.append(self.listaR.item(f, l).text())
							else:
								lista.append(self.__valorOriginalTxt)
						self.actualizarRegistro(lista, c, valorCeldaClickeada)
						self.ctrlZ.append([f, c, self.__valorOriginalTxt, valorCeldaClickeada])
					else:
						QtGui.QMessageBox.information(self, 'Information', 
											'No se hizo la modificacion. Fecha invalida.')
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
		except:
			pass

	def agregarRegistro(self, *lista):
		herr = PacienteBD(self.__arr_conexion)
		
		herr.id = lista[0]
		herr.nombre = lista[1]
		herr.apPaterno = lista[2]
		herr.apMaterno = lista[3]
		herr.telefono = lista[4]
		herr.agregar()

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

	def parsearFecha(self, cadena):
		try:
			(ano, mes, dia) = cadena.split("-")
			if int(ano)>0 and int(mes)>0 and int(mes)<13 and int(dia)>0 and int(dia)<32:
				return True
			else:
				return False
		except:
			return False

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


	def agregar(self):
		if not self.estado:
			self.estado = True
			self.btnAgregar.setStyleSheet('QPushButton {color: red}')
			self.btnAgregar.setText('CANCELAR')
		else:
			self.estado = False
			self.btnAgregar.setStyleSheet('QPushButton {color: black}')
			self.btnAgregar.setText('Agregar paciente')
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
			self.btnBuscar.setText('Buscar paciente')
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
		# try: # validar que halla seleccionado una celda
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
		# except:
		# 	MENSAJE ='No se pudo completar la operacion.\n1.- Asegurese de haber seleccionado un paciente en la tabla.'
		# 	QtGui.QMessageBox.critical(self, 'CRITICAL ERROR', MENSAJE, QtGui.QMessageBox.Abort)



	@property
	def listaR(self):
		return self._listaR	

	@property
	def txtId(self):
		return self._txtId

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

	
