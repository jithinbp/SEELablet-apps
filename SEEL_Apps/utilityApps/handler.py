
import time,random,functools,pkgutil,importlib,functools,pkg_resources
import numpy as np

import os,numbers
os.environ['QT_API'] = 'pyqt'
import sip
sip.setapi("QString", 2)
sip.setapi("QVariant", 2)

from PyQt4 import QtCore, QtGui
import pyqtgraph as pg
from SEEL_Apps.utilitiesClass import utilitiesClass
from SEEL_Apps.templates.widgets import interactivePlot

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Handler(QtGui.QWidget,interactivePlot.Ui_Form,utilitiesClass):  #Inherit all utilities from this
	"""
	This class contains methods that simplify setting up and running a plot and associated widgets	
	"""
	######################### high level functions ##################################
	def __init__(self, parent=None,**args):
		super(Handler, self).__init__()
		self.setupUi(self)
		self.ControlsLayout.setAlignment(QtCore.Qt.AlignTop)
		self.I = args.get('I',None)

		from SEEL.analyticsClass import analyticsClass
		self.math = analyticsClass()

		self.plot = self.add2DPlot(self.plot_area,enableMenu=args.get('enableMenu',False))
		self.plot.setLabel('bottom',args.get('xLabel','Time'), units=args.get('xLabelUnits','S'))
		self.plot.setLabel('left',args.get('yLabel','Voltage'), units=args.get('yLabelUnits','V'))
		self.plot.setYRange(args.get('yMin',-8.5),args.get('yMax',8.5))
		self.plot.legend = self.plot.addLegend(offset=(-10,30))

		self.curves=[]
		for a in args.get('curveNames',[]):
			self.addCurve(a)		

		self.tg = args.get('tg',1)
		self.max_samples = args.get('samples',2000)
		self.samples = self.max_samples
		
		self.channel = args.get('channel','CH1')
		self.autoRange()

		####################Cross hairs section#########################
		if args.get('crossHairs',False):
			self.plot.setTitle('')
			self.vLine = pg.InfiniteLine(angle=90, movable=False,pen=[100,100,200,200])
			self.plot.addItem(self.vLine, ignoreBounds=True)
			self.hLine = pg.InfiniteLine(angle=0, movable=False,pen=[100,100,200,200])
			self.plot.addItem(self.hLine, ignoreBounds=True)
			self.plot.proxy = pg.SignalProxy(self.plot.scene().sigMouseClicked, rateLimit=60, slot=self.crossHairClicked)
			self.plot.mousePoint=None

		############Fourier##########
		self.fmode = args.get('fourier',False)

		#####################Add widgets####################################
		#Curve Fitting
		self.addRegularButton(self.ControlsLayout,self.fitCurves,'Analyze')

		#Timebase Control
		a1={'TITLE':'TIMEBASE','MIN':0,'MAX':9,'FUNC':self.set_timebase,'UNITS':'S','TOOLTIP':'Set Timebase of the oscilloscope'}
		self.ControlsLayout.addWidget(self.dialIcon(**a1))

		#Gain Control
		if args.get('gain',None):
			chans = args.get('gain',None)
			G = self.gainIcon(FUNC=self.I.set_gain,LINK=self.gainChanged)
			self.ControlsLayout.addWidget(G)
			if 'CH1' in chans:
				G.g1.setCurrentIndex(chans['CH1']);
			else:
				G.g1.setEnabled(False)

			if 'CH2' in chans:
				G.g2.setCurrentIndex(chans['CH2']);
			else:
				G.g2.setEnabled(False)


		#Add self to layout
		args.get('layout').addWidget(self)


	def crossHairClicked(self,evt):
		pos = evt[0].scenePos()  ## using signal proxy turns original arguments into a tuple
		if self.plot.sceneBoundingRect().contains(pos):
			self.plot.mousePoint = self.plot.getPlotItem().vb.mapSceneToView(pos)
			self.vLine.setPos(self.plot.mousePoint.x())
			self.hLine.setPos(self.plot.mousePoint.y())
			self.updateCrossHairs()

	def updateCrossHairs(self):
		if self.plot.mousePoint:
			ylist = [];ylist_colors=[]
			for a in self.curves:
				_,y = a.getData()
				if y!=None:
					ylist.append(y)
					ylist_colors.append(a.opts['pen'].color().getRgb())

			if self.fmode:
				index = int(self.samples*self.plot.mousePoint.x()*self.tg/1e6)
			else:
				index = int(self.plot.mousePoint.x()*1e6/self.tg)

			maxIndex = self.samples			
			if index > 0 and index < maxIndex:
				coords="<span style='color: rgb(255,255,255)'>%s</span>,"%self.applySIPrefix(index*self.tg/1e6,'S')
				for col,a in zip(ylist_colors,ylist):
						try: coords+="<span style='color: rgb%s'>%0.3fV</span>," %(col, a[index])
						except: pass
				#self.coord_label.setText(coords)
				self.plot.plotItem.titleLabel.setText(coords)
			else:
				self.plot.plotItem.titleLabel.setText('')
				self.vLine.setPos(-1)
				self.hLine.setPos(-1)



	def fitCurves(self):
		msg = ''
		for a in self.curves:
			x,y = a.getData()
			name = a.name()
			msg+=name+':\n'
			RES='Could not analyze'
			if x!=None and y!=None:
				if len(x) == len(y):
					try:
						fitres = self.math.sineFit(x*1e6,y) #Convert X axis to uS
						if fitres:
							amp,freq,offset,phase = fitres
							if amp>0.1:RES='Amp=%s\tFreq=%s\tPhase = %s'%(self.applySIPrefix(amp,'V'),self.applySIPrefix(freq,'Hz'),self.applySIPrefix(phase,''))
							else: RES = 'RMS :%s'%self.applySIPrefix(self.math.RMS(y),'V')
					except:
						RES = 'RMS :%s'%self.applySIPrefix(self.math.RMS(y),'V')
			msg+=RES+'\n'
		QtGui.QMessageBox.about(self, 'Measured Paramaters',  msg)

	def autoRange(self):
		xlen = self.tg*self.samples*1e-6
		self.plot.autoRange();
		chan = self.I.analogInputSources[self.channel]
		R = [chan.calPoly10(0),chan.calPoly10(1023)]
		R[0]=R[0]*.9;R[1]=R[1]*.9
		self.plot.setLimits(yMax=max(R),yMin=min(R),xMin=0,xMax=xlen)
		self.plot.setYRange(min(R),max(R))			
		self.plot.setXRange(0,xlen)
		return self.samples*self.tg*1e-6

	def gainChanged(self,g):
		self.autoRange()

	def set_timebase(self,g):
		timebases = [0.5,1,2,4,8,32,128,256,512,1024]
		self.prescalerValue=[0,0,0,0,1,1,2,2,3,3,3][g]
		samplescaling=[1,1,1,1,1,0.5,0.4,0.3,0.2,0.2,0.1]
		self.tg=timebases[g]
		self.samples = int(self.max_samples*samplescaling[g])
		return self.autoRange()


	def addCurve(self,name,**kwargs):
		if(len(name)):curve = pg.PlotDataItem(name=name)
		else:curve = pg.PlotCurveItem(**kwargs)
		self.plot.addItem(curve)
		if self.properties['colorScheme']=='white':
			curve.setPen(kwargs.get('pen',{'color':self.white_trace_colors[len(self.curves)],'width':1}))
		elif self.properties['colorScheme']=='black':
			curve.setPen(kwargs.get('pen',{'color':self.black_trace_colors[len(self.curves)],'width':1}))
		self.curves.append(curve)
		return curve

	def activateMonitors(self,*args):
		self.monitors = {}
		self.monitorTimer=self.newTimer()
		if monitor in args:
			self.addMonitoring(monitor)

	def addMonitoring(self,func,delay):
		self.monitors[func]=delay

	def updateMonitors(self):
		self.monitorTimer.singleShot(100)

	def saveData(self):
		self.saveDataWindow(self.curves,self.plot)

