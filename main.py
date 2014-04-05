# -*- coding: utf-8 *-*
import sys
import math
from PySide import QtGui, QtCore

from Botones import Botones
from Paciente import Paciente
from Ortodoncista import Ortodoncista
from UTILERIAS.AdministradorArchivos import AdministradorArchivos
import CONSTANTES

def segmentos(p):
	todos = []
	primero = None
	ultimo = None

	for x in p:
		if primero is None:
			primero = x
		
		if ultimo is not None:
			if x != ultimo:
				todos.append((ultimo, x))
		ultimo = x
	return todos

def unirPuntos(p0, p1):
	yield p0
	yield p1


class Linea():
	def __init__(self, s, p0, p1, color):
		self.puntos = []
		self.p0 = p0
		self.p1 = p1

		pe = QtGui.QPen(color)
		br = QtGui.QBrush(color)
		gr = (QtGui.QPen(QtCore.Qt.gray),)

		# p0 <-> p1
		s.addLine(*(p0+p1+gr))
		self.union = list(segmentos(unirPuntos(p0, p1)))

	def pendiente(self):
		y = self.p1[1]-self.p0[1]
		x = self.p1[0]-self.p0[0]

		try:
			m = (float(y)/float(x))
			m = int(m*10)/10.0
			return m
		except:
			return 0 


class AreaDibujo(QtGui.QGraphicsScene):
	def __init__(self):
		QtGui.QGraphicsScene.__init__(self)
		self.coordenadas = []
		self.lineas = []

	def mouseReleaseEvent(self, event):
		calculados = list()
		c = QtCore.Qt.red
		x,y = event.scenePos().x(), event.scenePos().y()
		self.coordenadas.append((x,y))
		self.addEllipse(QtCore.QRectF(x-3, y-3, 6, 6), QtGui.QPen(c), QtGui.QBrush(c))
		if len(self.coordenadas)==2:
			self.coordenadas.append(c)
			self.lineas.append(Linea(self, *self.coordenadas))
			if len(self.lineas)>1:
				for i,n in enumerate(self.lineas):
					for j,m in enumerate(self.lineas):
						if i != j:
							if (i,j) not in calculados or (j,i) not in calculados:
								# las lineas se cruzan?
								if n.pendiente() != m.pendiente():
									ang = self.obtenerAngulo(n.pendiente(), m.pendiente())
									if ang<0:
										ang+=180
									ang = int(ang*10)/10.0
									print ang
									calculados.append((i,j))
									calculados.append((j,i))
			self.coordenadas = []

	def obtenerAngulo(self, m1, m2):
		try:
			formula = (m2-m1)/(1+(m2*m1))
			return math.degrees(math.atan(formula))
		except:
			return 0


class Conexion():
    def obtenerConexion(self):
    	ad = AdministradorArchivos()
    	# desencriptamos el archivo de conexiones
    	con = ad.desencriptaFichero('As05/4d0', #### PENDIENTE :: ENCRIPTAR ESTA PARTE ####
    									CONSTANTES.rutaArchivo, 
    									CONSTANTES.nombreArchivoCrenciales)
    	arr_con = ad.parsearCadena(con)
    	return arr_con



class MainWindow(QtGui.QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()

		# Abrimos una conexion a la base de datos
		co = Conexion() # instanciamos a la BD
		arr_con = co.obtenerConexion() # traemos el arreglo de las credenciales

		####### INSTANCIAMOS LAS CLASES DE LA INTERFAZ #######
		# instanciamos los botones
		self.bot = Botones(arr_con)
		self.pac = Paciente(arr_con)
		self.ort = Ortodoncista(arr_con)
		######################################################

		self.zoom = 0.0

		self.contenedorImagen = QtGui.QLabel()
		self.contenedorImagen.setBackgroundRole(QtGui.QPalette.Base)
		self.contenedorImagen.setSizePolicy(QtGui.QSizePolicy.Ignored,
						    QtGui.QSizePolicy.Ignored)
		self.contenedorImagen.setScaledContents(True)

		self.desplazamientoArea = QtGui.QScrollArea()
		self.desplazamientoArea.setBackgroundRole(QtGui.QPalette.Dark)
		self.desplazamientoArea.setWidget(self.contenedorImagen)
 		
		# self.scene = AreaDibujo()
		# self.scene.setSceneRect(QtCore.QRectF(0, 0, 300, 300))
		# # self.scene.addWidget(self.desplazamientoArea)
		# # self.scene.setBackgroundBrush(QtCore.Qt.blue)

		# self.view = QtGui.QGraphicsView(self.scene)
		# self.view.setRenderHint(QtGui.QPainter.Antialiasing)

		self.crearAtajos()
		self.crearMenus()
		self.widgetPrincipal()
		self.conexionesEventos()

		self.setWindowTitle('Tesis v1.0')

	def abrir(self):
		self.bot.abrir()
		self.cargar()

	def actualizarCambios(self):
		self.zoomMasAct.setEnabled(not self.tamanoVentanaAct.isChecked())
		self.zoomMenosAct.setEnabled(not self.tamanoVentanaAct.isChecked())
		self.tamanoNormalAct.setEnabled(not self.tamanoVentanaAct.isChecked())

	def ajustarDesplazamientoBarra(self, barra, valor):
		barra.setValue(int(valor * barra.value()
				       + ((valor - 1) * barra.pageStep()/2)))

	def cambioTab(self, indice):
		if indice==0:
			self.bot.actualizar()

	def cargar(self):
		# archivo = QtGui.QFileDialog.getOpenFileName(self, "Open File",
		# 					     QtCore.QDir.currentPath())
		# archivo = archivo[0]
		# if archivo: # validamos que haya escogido algo en el fileDialog
		# 	imagen = QtGui.QImage(archivo)
		# 	if imagen.isNull():
		# 		QtGui.QMessageBox.information(self, "Aviso",
		# 					      "No se puede cargar el%s." % archivo)
		# 		return

		if self.bot.imagen!=None:
			print 'Ruta:', self.bot.rutaImagen
			###
			# Se comentarizaron estas lineas porque tira error
			###

 			# self.scene.addWidget(QtGui.QPixmap.fromImage(self.bot.imagen))
			self.contenedorImagen.setPixmap(QtGui.QPixmap.fromImage(self.bot.imagen))
			self.zoom = 1.0
 
			self.tamanoVentanaAct.setEnabled(True)
			self.actualizarCambios()
 
			if not self.tamanoVentanaAct.isChecked():
				self.contenedorImagen.adjustSize()
		##### clase: Botones ####
		
	def conexionesEventos(self):
		self.bot.btnCargarImagen.clicked[bool].connect(self.cargar)
		
		self.pestania.currentChanged.connect(self.cambioTab)

	def crearAtajos(self):
		self.abrirAct = QtGui.QAction("&Abrir...", self, 
					      shortcut="Ctrl+O", triggered=self.abrir)

		self.salirAct = QtGui.QAction("&Salir de TESIS", self, 
					      shortcut="Ctrl+Q", triggered=self.close)

		self.zoomMasAct = QtGui.QAction("&Aumentar zoom (25%)", self,
		        			shortcut="Ctrl++", enabled=False, triggered=self.zoomMas)

		self.zoomMenosAct = QtGui.QAction("&Disminuir zoom (25%)", self,
						  shortcut="Ctrl+-", enabled=False, triggered=self.zoomMenos)

		self.tamanoNormalAct = QtGui.QAction("&Tamano normal", self,
						     shortcut="Ctrl+S", enabled=False, triggered=self.tamanoNormal)

		self.tamanoVentanaAct = QtGui.QAction("&Ancho de ventana", self,
						      enabled=False, checkable=True, shortcut="Ctrl+F", triggered=self.tamanoVentana)
		
	def crearMenus(self):
		self.menuArchivo = QtGui.QMenu("&Archivo", self)
		self.menuArchivo.addAction(self.abrirAct)
		self.menuArchivo.addSeparator()
		self.menuArchivo.addAction(self.salirAct)

		self.menuVisualizacion = QtGui.QMenu("&Visualizacion", self)
		self.menuVisualizacion.addAction(self.zoomMasAct)
		self.menuVisualizacion.addAction(self.zoomMenosAct)
		self.menuVisualizacion.addAction(self.tamanoNormalAct)
		self.menuVisualizacion.addSeparator()
		self.menuVisualizacion.addAction(self.tamanoVentanaAct)

		self.menuBar().addMenu(self.menuArchivo)
		self.menuBar().addMenu(self.menuVisualizacion)

	def tamanoNormal(self):
		self.contenedorImagen.adjustSize()
		self.zoom = 1.0

	def tamanoVentana(self):
		tamanoVentana = self.tamanoVentanaAct.isChecked()
		self.desplazamientoArea.setWidgetResizable(tamanoVentana)
		if not tamanoVentana:
			self.tamanoNormal()
		self.actualizarCambios()

	def widgetPrincipal(self):
		self.pestania = QtGui.QTabWidget()

		divisor = QtGui.QSplitter(QtCore.Qt.Horizontal)
		divisor.addWidget(self.bot.wig)
		divisor.addWidget(self.desplazamientoArea)
		# divisor.addWidget(self.view)

		divisor2 = QtGui.QSplitter(QtCore.Qt.Horizontal)
		divisor2.addWidget(self.pac.wig)

		divisor3 = QtGui.QSplitter(QtCore.Qt.Horizontal)
		divisor3.addWidget(self.ort.wig)

		divisor.setSizes([80, 500])

		self.pestania.addTab(divisor, 'Diagnostico')
		self.pestania.addTab(divisor2, 'Pacientes')
		self.pestania.addTab(divisor3, 'Ortodoncistas')

		self.setCentralWidget(self.pestania)

	def zoomImagen(self, valor):
		self.zoom *= valor
		self.contenedorImagen.resize(self.zoom * self.contenedorImagen.pixmap().size())
 
		self.ajustarDesplazamientoBarra(self.desplazamientoArea.horizontalScrollBar(), valor)
		self.ajustarDesplazamientoBarra(self.desplazamientoArea.verticalScrollBar(), valor)
 
		self.zoomMasAct.setEnabled(self.zoom < 3.0)
		self.zoomMenosAct.setEnabled(self.zoom > 0.333)

	def zoomMas(self):
		self.zoomImagen(1.25)

	def zoomMenos(self):
		self.zoomImagen(0.8)
	

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	mainWindow = MainWindow()
	mainWindow.showMaximized()
	sys.exit(app.exec_())
