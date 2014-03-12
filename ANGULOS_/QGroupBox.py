from PySide.QtCore import *
from PySide.QtGui import *
app = QApplication([])  # no need to import sys
# ----- start your widget test code ----
groupBox = QGroupBox("Radio Buttons")
radio1 = QRadioButton("Radio button 1")
radio2 = QRadioButton("Radio button 2")
radio3 = QRadioButton("Radio button 3")
radio1.setChecked(True)
vbox = QVBoxLayout()
vbox.addWidget(radio1)
vbox.addWidget(radio2)
vbox.addWidget(radio3)
vbox.addStretch(1)
groupBox.setLayout(vbox)
# optionally white bg with red border (3 pixel wide)
# groupBox.setStyleSheet("QGroupBox { background-color: \
#     rgb(255, 255, 255); border: 3px solid rgb(255, 0, 0); }")
groupBox.show()
# ---- end of widget test code -----
app.exec_()