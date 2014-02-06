# -*- coding: utf-8 *-*
import sys
from PySide import QtGui, QtCore

from Botones import Botones

class MainWindow(QtGui.QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()

		####### INSTANCIAMOS LAS CLASES DE LA INTERFAZ #######
		# instanciamos los botones
		self.bot = Botones()
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
 
		self.crearAtajos()
		self.crearMenus()
		self.conexionesEventos()
		self.widgetPrincipal()

		self.setWindowTitle('Tesis v1.0')

	def widgetPrincipal(self):
		pestania = QtGui.QTabWidget()

		divisor = QtGui.QSplitter(QtCore.Qt.Vertical)
		divisor.addWidget(self.bot.wig)
		divisor.addWidget(self.desplazamientoArea)

		divisor.setSizes([50, 700])

		pestania.addTab(divisor, 'Osvaldo Hinojosa')
		self.setCentralWidget(pestania)

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

	def conexionesEventos(self):
		##### clase: Botones ####
		self.bot.btnCargarImagen.clicked[bool].connect(self.abrir)
		self.bot.btnAgregarLinea.clicked[bool].connect(self.agregar)

	def abrir(self):
		archivo = QtGui.QFileDialog.getOpenFileName(self, "Open File",
							     QtCore.QDir.currentPath())
		archivo = archivo[0]
		if archivo: # validamos que haya escogido algo en el fileDialog
			imagen = QtGui.QImage(archivo)
			if imagen.isNull():
				QtGui.QMessageBox.information(self, "Aviso",
							      "No se puede cargar %s." % archivo)
				return
 
			self.contenedorImagen.setPixmap(QtGui.QPixmap.fromImage(imagen))
			self.zoom = 1.0
 
			self.tamanoVentanaAct.setEnabled(True)
			self.actualizarCambios()
 
			if not self.tamanoVentanaAct.isChecked():
				self.contenedorImagen.adjustSize()

	def agregar(self):
		print 'Agregar linea'

	def zoomMas(self):
		self.zoomImagen(1.25)

	def zoomMenos(self):
		self.zoomImagen(0.8)

	def tamanoNormal(self):
		self.contenedorImagen.adjustSize()
		self.zoom = 1.0

	def tamanoVentana(self):
		tamanoVentana = self.tamanoVentanaAct.isChecked()
		self.desplazamientoArea.setWidgetResizable(tamanoVentana)
		if not tamanoVentana:
			self.tamanoNormal()
		self.actualizarCambios()

	def actualizarCambios(self):
		self.bot.btnAgregarLinea.setEnabled(True)
		self.zoomMasAct.setEnabled(not self.tamanoVentanaAct.isChecked())
		self.zoomMenosAct.setEnabled(not self.tamanoVentanaAct.isChecked())
		self.tamanoNormalAct.setEnabled(not self.tamanoVentanaAct.isChecked())

	def zoomImagen(self, valor):
		self.zoom *= valor
		self.contenedorImagen.resize(self.zoom * self.contenedorImagen.pixmap().size())
 
		self.ajustarDesplazamientoBarra(self.desplazamientoArea.horizontalScrollBar(), valor)
		self.ajustarDesplazamientoBarra(self.desplazamientoArea.verticalScrollBar(), valor)
 
		self.zoomMasAct.setEnabled(self.zoom < 3.0)
		self.zoomMenosAct.setEnabled(self.zoom > 0.333)

	def ajustarDesplazamientoBarra(self, barra, valor):
		barra.setValue(int(valor * barra.value()
				       + ((valor - 1) * barra.pageStep()/2)))
	




if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	mainWindow = MainWindow()
	mainWindow.showMaximized()
	sys.exit(app.exec_())
