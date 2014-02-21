#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PySide.QtCore import *
from PySide.QtGui import *

import sys


# It's a brush that draws a checkered backbround.
class BackgroundBrush(QBrush):
	def __init__(self):
		bg_pix = self.createBackgroundPixmap()
		
		super(BackgroundBrush, self).__init__(bg_pix)

	def createBackgroundPixmap(self):
		off_white = 4294966265
		light_grey = 4291611852
		
		bg_pix = QPixmap(16, 16) # Hardcoded 16
		bg_pix.fill(off_white)
		
		painter = QPainter(bg_pix)
		pnt_brush = QBrush(light_grey)
		
		painter.setBrush(pnt_brush)
		painter.setPen(Qt.NoPen)
		
		painter.drawRect(0, 0, 8, 8) # Hardcoded 8 (half of 16)
		painter.drawRect(8, 8, 8, 8)
		
		painter.end()

		return bg_pix


# Sets widget size to 640x480 and adds a vbox layout
class CustomWidget(QWidget):
	def __init__(self):
		super(CustomWidget, self).__init__()

		self.setWindowTitle('Test')
		self.resize(640, 480)

		self.vbox = QVBoxLayout()
		self.setLayout(self.vbox)

# Press the + key to zoom in, and the - key to zoom out.
class CustomView(QGraphicsView):
	def __init__(self):
		super(CustomView, self).__init__()
		self.setMouseTracking(True)
		self.setBackgroundRole(QPalette.Dark)

	def keyPressEvent(self, event):
		if event.key() in (Qt.Key_Plus, Qt.Key_Equal):
			print('zoom in.')
			self.scale(2, 2)
		elif event.key() == Qt.Key_Minus:
			print('zoom out.')
			self.scale(0.5, 0.5)

# A stripped down version of the object I'm working with.
class CustomRect(QGraphicsObject):
	def __init__(self):
		super(CustomRect, self).__init__()

		self.rect = QRectF(-20, -20, 680, 520)
		self.draw_rect = QRectF(0, 0, 640, 480)

		self.background_pen = QPen(Qt.black)
		self.background_pen.setCosmetic(True)
		self.background_pen.setJoinStyle(Qt.MiterJoin)
		self.background_pen.setWidth(1)

		self.background_brush = BackgroundBrush()

	def boundingRect(self):
		return self.rect

	def paint(self, painter, option, widget):
		# Calling QGraphicsObject.update() fixes an issue where the background will become
		# distored if the view is zoomed in or out.
		self.update()

		painter.setPen(self.background_pen)
		painter.setBrush(self.background_brush)
		painter.drawRect(self.draw_rect)



app = QApplication(sys.argv)
w = CustomWidget()
view = CustomView()
w.vbox.addWidget(view)

scene = QGraphicsScene()
view.setScene(scene)

rect = CustomRect()
scene.addItem(rect)

w.show()

sys.exit(app.exec_())
