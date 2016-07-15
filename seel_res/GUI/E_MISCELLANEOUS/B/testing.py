#!/usr/bin/python

"""

::

	This program loads calibration data from a directory, processes it, and loads it into a connected device
	Not for regular users!
	Maybe dont include this in the main package

"""
from __future__ import print_function
from SEEL_Apps.utilitiesClass import utilitiesClass
from SEEL_Apps.utilityApps.templates import ui_testing as testing

import numpy as np
from PyQt4 import QtGui,QtCore
import pyqtgraph as pg
import sys,functools,os,random,struct,time

params = {
'image' : '',
'name':'Device\nTesting',
'hint':"A utility to test the device's features.\n These include digital I/O, analog I/O, capacitance measurement, and I2C port."

}



class AppWindow(QtGui.QMainWindow, testing.Ui_MainWindow,utilitiesClass):
	RESISTANCE_ERROR = 10
	CAPACITANCE_ERROR = 20e-12 #20pF
	def __init__(self, parent=None,**kwargs):
		super(AppWindow, self).__init__(parent)
		self.setupUi(self)
		self.I=kwargs.get('I',None)
		self.hexid = hex(self.I.device_id())
		self.setWindowTitle(self.I.generic_name + ' : '+self.I.H.version_string.decode("utf-8")+' : '+self.hexid)
		for a in range(50):
			for b in range(3):
				item = QtGui.QTableWidgetItem();self.tbl.setItem(a,b,item);	item.setText('')
		self.tests = [
		['I2C scan',[96],self.I2CScan],
		['SQR-ID',1e6,self.SQRID],
		['SEN',1e3,self.SEN],
		['CAP',680e-12,self.CAP],
		['PV1-CH1','graph',self.PV1CH1],
		['PV2-CH2','graph',self.PV2CH2],
		['PV3-CH3','graph',self.PV3CH3],
		#group 2 begins
		['W1-CH1',1e3,self.W1CH1],
		['W2-CH2',1e3,self.W2CH2],
		['PCS-CH3','graph',self.PCSCH3],
		]
		self.tbl.setVerticalHeaderLabels([row[0] for row in self.tests])
		self.tbl.setHorizontalHeaderLabels(['Expected','read',''])
		for n in range(len(self.tests)) :
			self.tbl.item(n,0).setText(str(self.tests[n][1]))
			################# make readback buttons ##############
			item = QtGui.QPushButton();item.setText('test'); item.clicked.connect(functools.partial(self.tests[n][2],n))
			self.tbl.setCellWidget(n, 2, item)



		self.plot=self.add2DPlot(self.plot_area)
		labelStyle = {'color': 'rgb(255,255,255)', 'font-size': '11pt'}
		self.plot.setLabel('left','Error -->', units='V',**labelStyle)
		self.plot.setLabel('bottom','Actual Voltage -->', units='V',**labelStyle)
		self.plot.setYRange(-.06,.06)

	def setSuccess(self,item,val):
		if val : item.setBackground(QtCore.Qt.green);
		else:item.setBackground(QtCore.Qt.red);

	def I2CScan(self,row):
		res = self.I.I2C.scan()
		item = self.tbl.item(row,1)
		item.setText(str(res))
		if 96 in res : self.setSuccess(item,1) #DAC found
		else :
			self.setSuccess(item,0) #dac not detected
			item.setText('DAC missing')

	def SQRID(self,row):
		self.I.map_reference_clock(7,'SQR1','SQR2','SQR3','SQR4')
		res = [self.I.get_freq(a) for a in ['ID1','ID2','ID3','ID4','CNTR'] ]
		self.I.set_state(SQR1=0,SQR2=0,SQR3=0,SQR4=0)	
		item = self.tbl.item(row,1)
		try:
			avg = np.average(res)
			item.setText('%.3e'%avg)
			if abs(avg-float(self.tbl.item(row,0).text() ))<20:	 self.setSuccess(item,1)
			else:	 self.setSuccess(item,1)				
		except Exception as e:
			print (e)
			item.setText('failed'); self.setSuccess(item,0)

	def eval1(self):
		self.SQRID(1)

	def eval2(self):
		self.SQRID(1)

	def SEN(self,row):
		res = self.I.get_resistance()
		item = self.tbl.item(row,1)
		item.setText(self.applySIPrefix(res,u"\u03A9"))
		if abs(res-float(self.tbl.item(row,0).text() ))<self.RESISTANCE_ERROR : self.setSuccess(item,1) #resistance within error margins
		else :
			self.setSuccess(item,0) 

	def CAP(self,row):
		res = self.I.get_capacitance()
		print (res)
		item = self.tbl.item(row,1)
		item.setText(self.applySIPrefix(res,'F'))
		if abs(res-float(self.tbl.item(row,0).text() ))<self.CAPACITANCE_ERROR : self.setSuccess(item,1) #capacitance within error margins
		else :
			self.setSuccess(item,0) 

	def PV1CH1(self,row):
		pass
	def PV2CH2(self,row):
		pass
	def PV3CH3(self,row):
		pass
	def W1CH1(self,row):
		pass
	def W2CH2(self,row):
		pass
	def PCSCH3(self,row):
		pass


	def __del__(self):
		print ('bye')




if __name__ == "__main__":
    from SEEL import interface
    app = QtGui.QApplication(sys.argv)
    myapp = AppWindow(I=interface.connect(load_calibration=False,verbose=True))
    myapp.show()
    sys.exit(app.exec_())

