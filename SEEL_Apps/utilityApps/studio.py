#!/usr/bin/python

"""

::

    This experiment is used to study non-inverting amplifiers

"""

from __future__ import print_function
from SEEL_Apps.utilitiesClass import utilitiesClass
from SEEL_Apps.utilityApps.handler import Handler
from SEEL_Apps.templates import simpleTemplate

from PyQt4 import QtGui,QtCore
import pyqtgraph as pg
import sys,functools,time
import numpy as np

params = {
'image' : 'halfwave.png',
'name':'Ramp\nGenerator',
'hint':'''
	An Op-Amp based linear ramp generator that integrates a step signal issued via SQR1 to make a smooth ramp output.<br>
	'''

}

class AppWindow(QtGui.QMainWindow, simpleTemplate.Ui_MainWindow,utilitiesClass):
	def __init__(self, parent=None,**args):
		super(AppWindow, self).__init__(parent)
		self.setupUi(self)
		self.I=args.get('I',None)
		self.setWindowTitle(self.I.H.version_string+' : '+params.get('name','').replace('\n',' ') )
		self.running=True;self.fit = False

		#Add a plot and some curves
		self.plot = Handler(I=self.I,xLabel='Time',yLabel='Voltage',xLabelUnits='S',yLabelUnits='V',curveNames=['INPUT(CH1)','OUTPUT(CH2)'],layout=self.plot_area,samples=2000,crossHairs=True)#,gain={'CH1':0,'CH2':0})

		#Add widgets to the top
		self.addWG(self.I,{'type':'W1','name':'sine1'},self.WidgetLayout)
		self.addWG(self.I,{'type':'W2','name':'sine2'},self.WidgetLayout)
		self.timer = self.newTimer()
		self.timer.singleShot(100,self.run)

	def run(self):
		if not self.running: return
		try:
			self.I.__fetch_channel__(1)
			self.I.__fetch_channel__(2)
			
			self.plot.curves[0].setData(self.I.achans[0].get_xaxis()*1e-6,self.I.achans[0].get_yaxis(),connect='finite')
			self.plot.curves[1].setData(self.I.achans[1].get_xaxis()*1e-6,self.I.achans[1].get_yaxis(),connect='finite')
			self.plot.updateCrossHairs()
			
			self.I.capture_traces(2,self.plot.samples,self.plot.tg)
			if self.running:self.timer.singleShot(self.plot.samples*self.I.timebase*1e-3+100,self.run)
		except Exception,e:
			print (e)

	def closeEvent(self, event):
		self.timer.stop()
		self.running=False

	def __del__(self):
		self.timer.stop()
		print('bye')


if __name__ == "__main__":
    from SEEL import interface
    app = QtGui.QApplication(sys.argv)
    I = interface.connect()
    myapp = AppWindow(I=I)
    myapp.show()
    sys.exit(app.exec_())

