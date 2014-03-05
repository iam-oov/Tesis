import sys
from PySide import QtGui, QtCore

app = QtGui.QApplication(sys.argv)

grview = QtGui.QGraphicsView()
grview.setViewport(QtGui.QGLWidget())
scene = QtGui.QGraphicsScene()
scene.addPixmap(QtGui.QPixmap('hola.jpg'))
grview.setScene(scene)

grview.show()

sys.exit(app.exec_())