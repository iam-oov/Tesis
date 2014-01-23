# -*- coding: utf-8 *-*
import sys
from PySide import QtGui, QtCore


from Botones import Botones
from Visualizador import Visualizador

class MainWindow(QtGui.QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()

		####### INSTANCIAMOS LAS CLASES DE LA INTERFAZ #######
		# instanciamos los botones
		self.bot = Botones()
		# instanciamos el visualizador
		self.vis = Visualizador()
		######################################################

		self.conexionesEventos()

		self.centralWidget()
		self.setWindowTitle('Tesis v1.0')

	def centralWidget(self):
		pestana = QtGui.QTabWidget()

		divisor = QtGui.QSplitter(QtCore.Qt.Vertical)
		divisor.addWidget(self.bot.wig)
		divisor.addWidget(self.vis.wig)

		divisor.setSizes([10, 350])

		pestana.addTab(divisor, 'Osvaldo Hinojosa')
		self.setCentralWidget(pestana)

	def conexionesEventos(self):
		##### clase: Botones ####
		self.bot.btnCargarImagen.clicked[bool].connect(self.cargar)
		self.bot.btnAgregarLinea.clicked[bool].connect(self.agregar)

	def cargar(self):
		print 'Cargar imagen'
		archivo = QtGui.QFileDialog.getOpenFileName(self, 'Abrir imagen',
														QtCore.QDir.currentPath())
		# validamos que haya escogido algo en el fileDialog
		if archivo:
			# madar la imagen al visualizador
			self.vis.abrir(archivo)




	def agregar(self):
		print 'Agregar linea'
	




if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	mainWindow = MainWindow()
	mainWindow.showMaximized()
	sys.exit(app.exec_())