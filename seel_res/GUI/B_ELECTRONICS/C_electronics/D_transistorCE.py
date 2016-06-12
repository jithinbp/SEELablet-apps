#!/usr/bin/python
'''
Study Common Emitter Characteristics of NPN transistors.
Saturation currents, and their dependence on base current 
can be easily visualized.

'''

from __future__ import print_function
import time,sys,os

from SEEL_Apps.utilitiesClass import utilitiesClass
from templates import transistorCE
from PyQt4 import QtCore, QtGui
import pyqtgraph as pg

import numpy as np

params = {
'image' : 'transistorCE.png',
'helpfile': 'transistorCE.html',
'name':'Transistor CE\nCharacteristics',
'hint':'Study the dependence of common emitter Characteristics of NPN transistors on base current .\n uses PV2 as the voltage source for setting collector voltage,\n and PV3 with a 200K resistor connected in series as the base current source.\nThe collector voltage is monitored via CH3. '
}

class AppWindow(QtGui.QMainWindow, transistorCE.Ui_MainWindow,utilitiesClass):
	def __init__(self, parent=None,**kwargs):
		super(AppWindow, self).__init__(parent)
		self.setupUi(self)
		self.I=kwargs.get('I',None)

		self.setWindowTitle(self.I.H.version_string+' : '+params.get('name','').replace('\n',' ') )

		self.plot=self.add2DPlot(self.plot_area,enableMenu=False)
		self.sig = self.rightClickToZoomOut(self.plot)
		labelStyle = {'color': 'rgb(255,255,255)', 'font-size': '11pt'}
		self.plot.setLabel('left','Current -->', units='A',**labelStyle)
		self.plot.setLabel('bottom','Voltage -->', units='V',**labelStyle)
		self.totalpoints=2000
		self.X=[]
		self.Y=[]
		
		self.curves=[]
		self.curveLabels=[]
		self.looptimer = QtCore.QTimer()
		self.looptimer.timeout.connect(self.acquire)
		self.running = True

	def savePlots(self):
		self.saveDataWindow(self.curves)


	def run(self):
		self.looptimer.stop()
		self.X=[];self.Y=[]
		self.base_voltage = self.baseV.value()

		self.curves.append( self.addCurve(self.plot ,'Vb = %.3f'%(self.base_voltage))  )

		self.I.set_pv3(self.base_voltage) # set base current. PV3+200K resistor

		self.V = self.startV.value()
		self.I.set_pv2(self.V) 
		time.sleep(0.2)

		P=self.plot.getPlotItem()
		self.plot.setXRange(self.V,self.stopV.value())
		self.plot.setYRange(0,10e-3)
		if len(self.curves)>1:P.enableAutoRange(True,True)

		if self.running:self.looptimer.start(20)

	def acquire(self):
		V=self.I.set_pv2(self.V)
		VC =  self.I.get_average_voltage('CH3',samples=20)
		self.X.append(VC)
		self.Y.append((V-VC)/1.e3) # list( ( np.linspace(V,V+self.stepV.value(),1000)-VC)/1.e3)
		self.curves[-1].setData(self.X,self.Y)

		self.V+=self.stepV.value()
		if self.V>self.stopV.value():
			self.looptimer.stop()
			txt='<div style="text-align: center"><span style="color: #FFF;font-size:8pt;">%.3f V</span></div>'%(self.base_voltage)
			text = pg.TextItem(html=txt, anchor=(0,0), border='w', fill=(0, 0, 255, 100))
			self.plot.addItem(text)
			text.setPos(self.X[-1],self.Y[-1])
			self.curveLabels.append(text)
			self.tracesBox.addItem('Vb = %.3f'%(self.base_voltage))

	def delete_curve(self):
		c = self.tracesBox.currentIndex()
		if c>-1:
			self.tracesBox.removeItem(c)
			self.removeCurve(self.plot,self.curves[c]);
			self.plot.removeItem(self.curveLabels[c]);
			self.curves.pop(c);self.curveLabels.pop(c);
			if len(self.curves)==0: # reset counter for plot numbers
				self.plotnum=0


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

