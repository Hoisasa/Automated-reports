import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QListWidgetItem

from GUI.MainWindow import Ui_MainWindow
from GUI.generatorSettingsWidget import Ui_Form

if __name__ == '__main__':

	app = QApplication(sys.argv)
	debug = True

	
	# Create and show the app window
	window = QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(window)
	for i in range(5):
		item = QListWidgetItem()
		ui.listWidget.addItem(item)
		custom_widget = QWidget()
		custom_ui = Ui_Form()
		custom_ui.setupUi(custom_widget)
		ui.listWidget.setItemWidget(item, custom_widget)

	window.setWindowFlags(Qt.FramelessWindowHint)
	window.show()
	sys.exit(app.exec())