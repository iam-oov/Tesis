
from PySide import QtCore, QtGui 
 
class Visualizador(QtGui.QMainWindow):
    def __init__(self):
    	super(Visualizador, self).__init__()

    	self.wig = QtGui.QListWidget()
    	self.printer = QtGui.QPrinter()
    	self.scaleFactor = 0.0

        self.imagenPanel = QtGui.QLabel()
        self.imagenPanel.setBackgroundRole(QtGui.QPalette.Base)
        self.imagenPanel.setSizePolicy(QtGui.QSizePolicy.Ignored,
                                      QtGui.QSizePolicy.Ignored)
        self.imagenPanel.setScaledContents(True)
        
        panel = QtGui.QHBoxLayout() # contenedor
        panel.addWidget(self.imagenPanel)
        self.wig.setLayout(panel)

    def abrir(self, archivo):
        archivo = archivo[0]
        if archivo:
            image = QtGui.QImage(archivo)
            if image.isNull():
                QtGui.QMessageBox.information(self, "Visualizador",
                                              "El archivo no es un formato de imagen valido.\
                                               %s." % archivo)
                return
            
            self.imagenPanel.setPixmap(QtGui.QPixmap.fromImage(image))
