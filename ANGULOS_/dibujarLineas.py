import sys
import math
from PySide import QtGui, QtCore

class Linea():
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.m = 0

    def pendiente(self):
        y = self.p2[1]-self.p1[1]
        x = self.p2[0]-self.p1[0]
        
        try:
            m = (float(y)/float(x))
            return m
        except:
            return 0 


class Principal(QtGui.QWidget):
    
    def __init__(self):
        super(Principal, self).__init__()
        self.pendientes = list()
        self.initUI()
        self._btnCargarImagen = QtGui.QPushButton('Calcular angulo', self)
        self.conexionesEventos()
        
    def initUI(self):      
        self.setWindowTitle('Lineas')

    def paintEvent(self, e):
        p1 = (50, 100)
        p2 = (150, 200)
        p3 = (40, 210)
        p4 = (120, 50)
        qp = QtGui.QPainter()
        qp.begin(self)

        l = Linea(p1, p2)
        self.pendientes.append(l.pendiente())
        self.dibujarLinea(qp, p1, p2)

        l = Linea(p3, p4)
        self.pendientes.append(l.pendiente())
        self.dibujarLinea(qp, p3, p4)

        qp.end()

    def conexionesEventos(self):
        self._btnCargarImagen.clicked[bool].connect(self.abrir) 
    
    def dibujarLinea(self, qp, p1, p2):
        pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(p1[0], p1[1], p2[0], p2[1]) # 90
        

    def obtenerAngulo(self, m1, m2):
        formula = (m2-m1)/(1+(m2*m1))
        return math.degrees(math.atan(formula))
        
    def abrir(self):
        print self.obtenerAngulo(self.pendientes[0], self.pendientes[1])

        
def main():
    app = QtGui.QApplication(sys.argv)
    pri = Principal()
    pri.showMaximized()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()