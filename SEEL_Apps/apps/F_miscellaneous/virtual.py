#!/usr/bin/python
'''
Use the MF522 RFID Reader via the SPI port.
uses chip select 1
'''

from __future__ import print_function
import os

from PyQt4 import QtCore, QtGui
import time,sys
from templates import remote
import sys


params = {
'image' : 'mf522.png',
'helpfile': '',
'name':'Virtual\nLab',
'hint':'For now this simply hosts a CherryPy based web server that can be used to remotely call functions via the device IP'
}

class AppWindow(QtGui.QMainWindow, remote.Ui_MainWindow):
	def __init__(self, parent=None,**kwargs):
		super(AppWindow, self).__init__(parent)
		self.setupUi(self)
		self.I=kwargs.get('I',None)
		self.setWindowTitle(self.I.H.version_string+' : '+params.get('name','').replace('\n',' ') )


	def start(self):
		pass

	def stop(self):
		pass

	def __del__(self):
		self.looptimer.stop()
		print ('bye')

	def closeEvent(self, event):
		self.looptimer.stop()
		self.finished=True


if __name__ == "__main__":
    from SEEL import interface
    app = QtGui.QApplication(sys.argv)
    myapp = AppWindow(I=interface.connect())
    myapp.show()
    sys.exit(app.exec_())

