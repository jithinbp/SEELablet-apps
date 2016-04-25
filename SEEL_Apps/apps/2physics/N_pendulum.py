#!/usr/bin/python

"""

::

"""

from __future__ import print_function
from SEEL_Apps.utilitiesClass import utilitiesClass
from SEEL.analyticsClass import analyticsClass

from templates import template_transient

import numpy as np
from PyQt4 import QtGui,QtCore
import pyqtgraph as pg
import sys

params = {
'image' : 'transient.png',
#'helpfile': 'https://en.wikipedia.org/wiki/LC_circuit',
'name':'Simple Pendulum',
'hint':'''
	Study Simple pendulum's velocity oscillations.<br>
	Connect a pendulum to the shaft of a simple DC motor.<br>
	Connect one terminal of the motor to GND, and the other to CH3.<br>
	The voltage output from the motor due to the rotating shaft has low amplitude, so connect a 100 ohm resistor from Rg to GND.<br>
	This sets a gain of around 100x, and allows clear visualization of oscillations
	'''

}

class AppWindow(QtGui.QMainWindow, template_transient.Ui_MainWindow,utilitiesClass):
	def __init__(self, parent=None,**kwargs):
		super(AppWindow, self).__init__(parent)
		self.setupUi(self)
		self.I=kwargs.get('I',None)
		self.CC = analyticsClass()
		
		self.setWindowTitle(self.I.H.version_string+' : '+params.get('name','').replace('\n',' ') )

		self.plot1=self.add2DPlot(self.plot_area)
		labelStyle = {'color': 'rgb(255,255,255)', 'font-size': '11pt'}
		self.plot1.setLabel('left','Voltage -->', units='V',**labelStyle)
		self.plot1.setLabel('bottom','Time -->', units='S',**labelStyle)

		self.plot1.setYRange(-8.5,8.5)
		self.tg=100
		self.tgLabel.setText(str(5000*self.tg*1e-3)+'S')
		self.x=[]

		self.looptimer=QtCore.QTimer()
		self.curveCH1 = self.addCurve(self.plot1,'CH3',(255,255,255))
		self.CH1Fit = self.addCurve(self.plot1,'CH3 Fit',(0,255,255))
		self.region = pg.LinearRegionItem([self.tg*50*1e-6,self.tg*800*1e-6])
		self.region.setZValue(-10)
		self.plot1.addItem(self.region)		
		self.lognum=0
		self.msg.setText("Fitting fn :\noff+amp*exp(-damp*x)*sin(x*freq+ph)")
		self.running=True
		self.Params=[]
		
	def run(self):
		if not self.running:return
		self.I.__capture_fullspeed__('CH3',5000,self.tg)
		self.CH1Fit.setData([],[])
		self.loop=self.delayedTask(5000*self.I.timebase*1e-3+10,self.plotData)

	def plotData(self):	
		self.x,self.VMID=self.I.__retrieveBufferData__('CH3',self.I.samples,self.I.timebase)#self.I.fetch_trace(1)
		self.curveCH1.setData(self.x*1e-6,self.VMID)

	def setTimebase(self,T):
		self.tgs = [100,200,300,500,800,1000,2000,3000,5000,10000]
		self.tg = self.tgs[T]
		self.tgLabel.setText(str(5000*self.tg*1e-3)+'mS')

	def fit(self):
		if(not len(self.x)):return
		start,end=self.region.getRegion()
		print (start,end,self.I.timebase)
		if(start>0):start = int(round(1.e6*start/self.I.timebase ))
		else: start=0
		if(end>0):end = int(round(1.e6*end/self.I.timebase ))
		else:end=0
		guess = self.CC.getGuessValues(self.x[start:end]-self.x[start],self.VMID[start:end],func='damped sine')
		Csuccess,Cparams,chisq = self.CC.arbitFit(self.x[start:end]-self.x[start],self.VMID[start:end],self.CC.dampedSine,guess=guess)

		if Csuccess:
			self.CLabel.setText("CH1:\nA:%.2f V\tF:%.4f Hz\tDamp:%.3e"%(Cparams[0],1e6*abs(Cparams[1])/(2*np.pi),Cparams[4]))
			self.CH1Fit.setData(self.x[start:end]*1e-6,self.CC.dampedSine(self.x[start:end]-self.x[start],*Cparams))
			self.CParams=Cparams
		else:
			self.CLabel.setText("CH1:\nFit Failed. Change selected region.")
			self.CH1Fit.clear()

	def closeEvent(self, event):
		self.running=False

	def showData(self):
		self.lognum+=1
		b=self.CParams
		res =  'FIT:\nAmp:%.1fV\tFreq:%.1fHz\tPhase:%.1f\nOffset:%.2fV\tDamping:%.2e'%(b[0],1e6*abs(b[1])/(2*np.pi),b[2]*180/np.pi,b[3],b[4])
		self.displayDialog(res)
		
if __name__ == "__main__":
	from SEEL import interface
	app = QtGui.QApplication(sys.argv)
	myapp = AppWindow(I=interface.connect())
	myapp.show()
	sys.exit(app.exec_())

