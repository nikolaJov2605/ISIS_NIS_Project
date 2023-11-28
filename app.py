import sys
from ui.main_view import MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication

# .\.env\Scripts\activate

app = QApplication(sys.argv)
mainWindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainWindow)
widget.setFixedWidth(1082)
widget.setFixedHeight(747)
widget.show()
sys.exit(app.exec_())