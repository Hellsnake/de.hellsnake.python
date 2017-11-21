import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from firstgui import BaseGUI
import visa
 
class MyFirstGuiProgram(BaseGUI):


	def __init__(self, dialog):
		BaseGUI.__init__(self)
		self.setupUi(dialog)
		self._visa_rm = visa.ResourceManager()
		self._visa_list = self._visa_rm.list_resources()
		self.initList()
		self.refreshBtn.clicked.connect(self.initList)
		self.sendCommandBtn.clicked.connect(self.sendCommand)

	def initList(self):
		self.listWidget.clear()
		for dev in self._visa_list:
			self.addItemToListbox(dev)


	def addItemToListbox(self, item):
		self.listWidget.addItem(item)

	def sendCommand(self, command):
		command = self.myTextInput.text()
		response = str()

		if len(command) == 0 or len(self.listWidget.selectedItems()) == 0:
			return

		visa_dev = self._visa_rm.open_resource(self.listWidget.selectedItems()[0].text())
		visa_dev.write_termination = '\n'
		visa_dev.write(command)
		visa_dev.wait_for_srq()
		response = visa_dev.read()
		print("Response: {0:s}".format(response))
		self.responseLabel.setText("Response: " + response)
		self.responseLabel.adjustSize()
		visa_dev.close()

 
if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	dialog = QtWidgets.QDialog()
 
	prog = MyFirstGuiProgram(dialog)
 
	dialog.show()
	sys.exit(app.exec_())