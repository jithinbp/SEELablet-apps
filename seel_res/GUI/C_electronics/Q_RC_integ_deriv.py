#!/usr/bin/python

"""

::

    This experiment is used to study Half wave rectifiers


"""

from __future__ import print_function
from SEEL_Apps.utilitiesClass import utilitiesClass

from .templates import template_graph

import numpy as np
from PyQt4 import QtGui,QtCore
import pyqtgraph as pg
import sys,time

params = {
'image' : 'RCd.png',
'helpfile': 'http://www.physics.ucla.edu/demoweb/demomanual/electricity_and_magnetism/ac_circuits/rc_integration_and_differentiation.html',
'name':'RC Integrals,\nDerivatives',
'hint':'''
	Study integration and differentiation of square waves using an RC network.
	'''
}

class AppWindow(QtGui.QMainWindow, template_graph.Ui_MainWindow,utilitiesClass):
	def __init__(self, parent=None,**kwargs):
		super(AppWindow, self).__init__(parent)
		self.setupUi(self)
		self.I=kwargs.get('I',None)
		
		self.setWindowTitle(self.I.H.version_string+' : '+params.get('name','').replace('\n',' ') )

		self.plot1=self.add2DPlot(self.plot_area)
		labelStyle = {'color': 'rgb(255,255,255)', 'font-size': '11pt'}
		self.plot1.setLabel('left','Voltage -->', units='V',**labelStyle)
		self.plot1.setLabel('bottom','Time -->', units='S',**labelStyle)
		self.plot1.setYRange(-8.5,8.5)
		self.p1legend = self.plot1.addLegend(offset=(-1,1))
		self.I.set_gain('CH1',1)
		self.I.set_gain('CH2',1)
		self.plot1.setLimits(yMax=8,yMin=-8,xMin=0,xMax=4e-3)


		self.I.configure_trigger(0,'CH1',0)
		self.tg=2
		self.samples=2000
		self.timer = QtCore.QTimer()

		self.curveCH1 = self.addCurve(self.plot1,'INPUT(CH1)')
		self.curveCH2 = self.addCurve(self.plot1,'OUTPUT(CH2)')
		self.WidgetLayout.setAlignment(QtCore.Qt.AlignLeft)

		#a1={'TITLE':'Triangle\n(W1)','MIN':10,'MAX':5000,'FUNC':self.I.set_sine1,'TYPE':'dial','UNITS':'Hz','TOOLTIP':'Frequency of waveform generator #1','LINK':self.updateLabels}
		#self.WidgetLayout.addWidget(self.dialIcon(**a1))
		a1={'TITLE':'SQR1','MIN':10,'MAX':5000,'FUNC':self.I.sqr1,'TYPE':'dial','UNITS':'Hz','TOOLTIP':'Frequency of square wave generator #1','LINK':self.updateLabels}
		self.dial = self.dialIcon(**a1)
		self.WidgetLayout.addWidget(self.dial)
		self.dial.dial.setValue(100)

		self.running=True
		self.timer.singleShot(100,self.run)


	def updateLabels(self,value,units=''):
		if value:self.tg = 1e6*(5./value)/self.samples
		if self.tg<2:self.tg=2
		elif self.tg>200:self.tg=200
		self.setTimeGap(self.tg)
		
	def setTimeGap(self,tg):
		self.tg = tg
		self.plot1.setXRange(0,self.samples*self.tg*1e-6)
		self.plot1.setLimits(yMax=8,yMin=-8,xMin=0,xMax=self.samples*self.tg*1e-6)
		
	def run(self):
		if not self.running:return
		self.I.configure_trigger(0,'CH1',0.2,resolution=10,prescaler=1)
		self.I.capture_traces(2,self.samples,self.tg)
		if self.running:self.timer.singleShot(self.samples*self.I.timebase*1e-3+20,self.plotData)

	def plotData(self): 
		try:
			while(not self.I.oscilloscope_progress()[0]):
				time.sleep(0.1)
				print (self.I.timebase,'correction required',n)
				n+=1
				if n>10:
					self.timer.singleShot(100,self.run)
					return
			self.I.__fetch_channel__(1)
			self.I.__fetch_channel__(2)
			self.curveCH1.setData(self.I.achans[0].get_xaxis()*1e-6,self.I.achans[0].get_yaxis(),connect='finite')
			self.curveCH2.setData(self.I.achans[1].get_xaxis()*1e-6,self.I.achans[1].get_yaxis(),connect='finite')
			self.timer.singleShot(100,self.run)
		except:
			pass

	def closeEvent(self, event):
		self.timer.stop()
		self.finished=True
		self.running=False
		
	def savePlots(self):
		self.saveDataWindow([self.curveCH1,self.curveCH2])
		

	def __del__(self):
		self.timer.stop()
		print ('bye')

if __name__ == "__main__":
    from SEEL import interface
    app = QtGui.QApplication(sys.argv)
    myapp = AppWindow(I=interface.connect())
    myapp.show()
    sys.exit(app.exec_())

