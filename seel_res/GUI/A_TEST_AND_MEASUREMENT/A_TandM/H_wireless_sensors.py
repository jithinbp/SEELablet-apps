#!/usr/bin/python
'''
This Utility allows auto-detection of wireless nodes in the vicinity, as well as the
sensors connected to each. It can then be used to plot data acquired from sensors located 
on the various nodes.

'''
from __future__ import print_function


from SEEL_Apps.utilitiesClass import utilitiesClass
from SEEL_Apps.templates.widgets.ui_nodeList import Ui_Form as nodeWidget
from SEEL_Apps.templates.widgets import ui_wirelessWidget as wirelessWidget

from SEEL.SENSORS import HMC5883L,MPU6050,MLX90614,BMP180,TSL2561,SHT21
from SEEL.SENSORS.supported import supported
from SEEL.sensorlist import sensors as sensorHints
import pyqtgraph as pg
import numpy as np
from PyQt4 import QtCore, QtGui

import SEEL.commands_proto as CP

from templates import ui_wirelessTemplate2 as wirelessTemplate

import time,sys,functools

params = {
'image' : 'ico_sensor_w.png',
'helpfile': 'http://seelablet.jithinbp.in',
'name':'wireless\nsensors',
'persist':True,
'hint':'''
	Plot values returned by sensors connected to the I2C input of wireless nodes.</br>
	Support sensors include MPU6050(3-axis Accel/gyro), TSL2561(luminosity),<br>
	HMC5883L(3-axis magnetometer), SHT21(humidity), BMP180(Pressure,Altitude) etc.
	'''
}


class AppWindow(QtGui.QMainWindow, wirelessTemplate.Ui_MainWindow,utilitiesClass):
	def __init__(self, parent=None,**kwargs):
		super(AppWindow, self).__init__(parent)
		self.setupUi(self)
		self.I=kwargs.get('I',None)
		self.setWindowTitle(self.I.H.version_string+' : '+params.get('name','').replace('\n',' ') )

		self.I.NRF.start_token_manager()
		print (self.I.readLog()	)
		self.plot=self.add2DPlot(self.plot_area)
		self.plot.setLabel('bottom', 'Datapoints')
		self.plot.enableAutoRange(True,True)
		self.plot.setXRange(0,1000)
		self.plot.setLimits(xMin=0,xMax=1000)
		self.curves=[]
		self.nodeWidgets=[]
		self.nodeList=[]
		self.acquireList=[]
		self.POINTS=1000
		self.xdata=range(self.POINTS)
		self.fps=0;self.lastTime=time.time();self.updatepos=0
		self.active_device_counter=0
		self.right_axes=[]
		self.timer = self.loopTask(2,self.updatePlots)
		self.updatepos=0
		self.refreshTimer = self.loopTask(200,self.updateLogWindow)
		self.deviceMenus=[]
		self.actionWidgets=[]

		self.sensorWidgets=[]
		self.availableClasses=[0x68,0x1E,0x5A,0x77,0x39,0x40]
		self.Running =True


		self.colbtn = pg.ColorButton()
		self.colbtn.setMaximumWidth(30);self.colbtn.setMinimumHeight(25);self.colbtn.setStyleSheet("border-radius: 0px;padding: 0px;")
		self.horizontalLayout_3.addWidget(self.colbtn)
		self.colbtn.sigColorChanging.connect(self.setRGB)

	def setRGB(self):
		self.I.NRF.WS2812B([list(self.colbtn.color().getRgb())])


	class plotItem:
		def __init__(self,handle,ydata,curves):
			'''
			Handle must have a getRaw method
			'''
			self.handle = handle
			self.ydata = ydata
			self.curves=curves

	def addPlot(self,newNode,param):
		addr = newNode.ADDRESS
		self.nodeList.append(newNode)
		print ('made link',addr,param)
		#newNode.write_register(self.I.NRF.RF_SETUP,0x0E)
		#self.I.NRF.write_register(self.I.NRF.RF_SETUP,0x0E) #Change to 2MBPS
		cls=False
		cls_module = supported.get(param,None)
		if cls_module:
			cls = cls_module.connect(newNode)
		else:
			cls=None

		if cls:
			if hasattr(cls,'name'):	label = cls.name
			else: label =''
			if not self.active_device_counter:
				if len(label):self.plot.setLabel('left', label)
				curves=[self.addCurve(self.plot,'%s[%s]'%(label[:10],cls.PLOTNAMES[a])) for a in range(cls.NUMPLOTS)]
			else:
				if label:
					colStr = lambda col: hex(col[0])[2:]+hex(col[1])[2:]+hex(col[2])[2:]
					newplt = self.addAxis(self.plot,label=label)#,color='#'+colStr(cols[0].getRgb()))
				else: newplt = self.addAxis(self.plot)
				self.right_axes.append(newplt)
				curves=[self.addCurve(newplt ,'%s[%s]'%(label[:10],cls.PLOTNAMES[a])) for a in range(cls.NUMPLOTS)]
				#for a in range(cls.NUMPLOTS):
				#	self.plotLegend.addItem(curves[a],'%s[%s]'%(label[:10],cls.PLOTNAMES[a]))
			
			self.createMenu(cls,param)
			for a in range(cls.NUMPLOTS):
				curves[a].checked=True
				Callback = functools.partial(self.setTraceVisibility,curves[a])		
				action=QtGui.QCheckBox('%s'%(cls.PLOTNAMES[a])) #self.curveMenu.addAction('%s[%d]'%(label[:12],a)) 
				action.toggled[bool].connect(Callback)
				action.setChecked(True)
				action.setStyleSheet("background-color:rgb%s;"%(str(curves[a].opts['pen'].color().getRgb())))
				self.paramMenus.insertWidget(1,action)
				self.actionWidgets.append(action)
			self.acquireList.append(self.plotItem(cls,np.zeros((cls.NUMPLOTS,self.POINTS)), curves)) 
			self.active_device_counter+=1

	def addCustomPlot(self,fn,labels,axisTitle=''):
			totalplots = len(labels)
			if not self.active_device_counter:
				self.plot.setLabel('left', axisTitle if len(labels)>1 else labels[0])
				curves=[self.addCurve(self.plot,a) for a in labels]
			else:
				colStr = lambda col: hex(col[0])[2:]+hex(col[1])[2:]+hex(col[2])[2:]
				newplt = self.addAxis(self.plot,label=axisTitle if len(labels)>1 else labels[0])#,color='#'+colStr(cols[0].getRgb()))
				self.right_axes.append(newplt)
				curves=[self.addCurve(newplt,a) for a in labels]
			
			for a in range(totalplots):
				curves[a].checked=True
				Callback = functools.partial(self.setTraceVisibility,curves[a])		
				action=QtGui.QCheckBox(labels[a]) 
				action.toggled[bool].connect(Callback)
				action.setChecked(True)
				action.setStyleSheet("background-color:rgb%s;"%(str(curves[0].opts['pen'].color().getRgb())))
				self.paramMenus.insertWidget(1,action)
				self.actionWidgets.append(action)
			self.acquireList.append(self.plotItem(fn,np.zeros((1,self.POINTS)), curves)) 
			self.active_device_counter+=1


	
	def setTraceVisibility(self,curve,status):
		curve.clear()
		curve.setEnabled(status)
		curve.checked=status
	
	class PermanentMenu(QtGui.QMenu):
		def hideEvent(self, event):
			self.show()
        
	def createMenu(self,cls,addr):
		menu = self.PermanentMenu()
		menu.setMinimumHeight(25)
		sub_menu = QtGui.QMenu('%s:%s'%(hex(addr),cls.name[:15]))
		for i in cls.params: 
			mini=sub_menu.addMenu(i) 
			for a in cls.params[i]:
				Callback = functools.partial(getattr(cls,i),a)		
				mini.addAction(str(a),Callback) 
		menu.addMenu(sub_menu)
		self.paramMenus.insertWidget(1,menu)
		self.deviceMenus.append(menu)
		self.deviceMenus.append(sub_menu)
	
	class nrfHandler(QtGui.QWidget,wirelessWidget.Ui_Form):
		def __init__(self,node,I2Cs,evaluator,batLevel,fallbackEvaluator):
			super(AppWindow.nrfHandler, self).__init__()
			self.setupUi(self)
			self.node = node
			self.title.setText(hex(node.ADDRESS)+' %d%%'%(batLevel))
			self.title.setStyleSheet("* {color: white; background: qlineargradient( x1:0 y1:0, x2:2 y2:0, stop:0 green, stop:%.1f red);}"%(batLevel/100.));
			self.cmd = evaluator
			self.cmd2 = fallbackEvaluator
			for i in I2Cs:
				self.items.addItem('I2C:'+hex(i))
			self.items.addItems(['ADC:CS3','ADC:BAT'])

			self.colbtn = pg.ColorButton()
			self.colbtn.setMaximumWidth(30);self.colbtn.setMinimumHeight(25);self.colbtn.setStyleSheet("border-radius: 0px;padding: 0px;")
			self.horizontalLayout.addWidget(self.colbtn)
			self.colbtn.sigColorChanging.connect(self.setRGB)

		class tmp:
			pass
			
		def clicked(self):
			val = self.items.currentText()
			if val[:3]=='I2C':
				self.cmd(self.node,int(str(val[4:]),0))
			if val[:3]=='ADC':
				T = self.tmp()
				T.getRaw = lambda : [self.node.readADC(val[4:])]
				self.cmd2( T , ['%s:ADC(CS3)'%(hex(self.node.ADDRESS))] )

		def setRGB(self):
			self.node.WS2812B([list(self.colbtn.color().getRgb())])
		def setDAC(self,val):
			v=self.node.setDAC(val*3.3/31)
			self.DACLabel.setText('DAC:%.1f V'%(v))
		def setCS1(self,st):
			if(st):st=1  #Qt button state is 0 for unchecked , 2 for checked. 
			self.node.setIO(CS1 = st)
		def setCS2(self,st):
			if(st):st=1
			self.node.setIO(CS2 = st)
		def getFreq(self):
			self.freqBtn.setText('FREQ(CS3): '+CP.applySIPrefix(self.node.readFrequency(),'Hz'))
		def getADC(self):
			self.adcBtn.setText('ADC(CS3): '+CP.applySIPrefix(self.node.readADC('CS3'),'V'))
			
	def ping(self):
		last_state  = self.checkBox.isChecked()
		self.checkBox.setChecked(True); self.toggleListen(True)
		self.I.NRF.broadcastPing()
		time.sleep(0.1)
		self.updateLogWindow()
		self.checkBox.setChecked(last_state); self.toggleListen(last_state)

	def updateLogWindow(self):
		pass
		"""
		x=self.I.readLog()
		if len(x):print ('Log:',x)
		lst = self.I.NRF.get_nodelist()
		T='''
		<style type="text/css" scoped>
		table.GeneratedTable {width:100%;background-color:#FFFFFF;border-collapse:collapse;
		border-width:1px;border-color:#336600;	border-style:solid;	color:#009900;	}
		table.GeneratedTable td, table.GeneratedTable th {
		border-width:1px;border-color:#336600;border-style:solid;padding:1px;}
		table.GeneratedTable thead {background-color:#CCFF99;}
		</style>

		<table class="GeneratedTable"><thead>
		<tr><th>Node Address</th><th>Sensors detected</th>	</tr>
		</thead><tbody>
		'''
		for a in lst:
			T+='<tr><td>'
			T+='''<span style="font-size:11pt">%s %d%%</span>'''%(hex(a),lst[a][1])
			T+='</td><td>'
			for b in lst[a][0]:
				T+='''<span title="%s" style="font-size:11pt">'''%(sensorHints.get(b,'No clue'))+hex(b)+'. </span>'
			T+='</td></tr>'
		
		
		T+='''
		</tbody></table>
		'''
		self.logs.setHtml(T)
		"""
		lst = self.I.NRF.get_nodelist()
		x=self.I.readLog()
		if len(x):print (x)
		for a in self.nodeWidgets:
			a.setParent(None)
		self.nodeWidgets=[]
		for a in lst:
			new = self.I.newRadioLink(address=a)
			newNode=self.nrfHandler(new,lst[a][0],self.addPlot,lst[a][1],self.addCustomPlot)
			self.nodeArea.insertWidget(0,newNode)
			self.nodeWidgets.append(newNode)

	def updatePlots(self):
		if self.pauseBox.isChecked():return	
		for item in self.acquireList:
			need_data=False
			for a in item.curves:
				if a.checked:need_data=True
			if need_data:			
				vals=item.handle.getRaw()
				#print (vals)
				if not vals:continue
				for X in range(len(item.curves)):
					item.ydata[X][self.updatepos] = vals[X]
				if self.updatepos%20==0:
					for a in range(len(item.curves)):
						if item.curves[a].checked:item.curves[a].setData(self.xdata,item.ydata[a])

		if len(self.acquireList):
			self.updatepos+=1
			if self.updatepos>=self.POINTS:self.updatepos=0
		
			now = time.time()
			dt = now - self.lastTime
			self.lastTime = now
			if self.fps is None:
				self.fps = 1.0/dt
			else:
				s = np.clip(dt*3., 0, 1)
				self.fps = self.fps * (1-s) + (1.0/dt) * s
			self.plot.setTitle('%0.2f fps' % (self.fps) )

	def saveData(self):
		self.pauseBox.setChecked(True)
		curvelist = []
		for item in self.acquireList:
			for a in item.curves:
				if a.checked:curvelist.append(a)
		self.saveDataWindow(curvelist,self.plot)
			
	def toggleListen(self,state):
		if state:
			self.widgetScroll.setEnabled(False)
			self.I.NRF.start_token_manager()
			self.refreshTimer.start()
		else: 
			self.widgetScroll.setEnabled(True)
			self.I.NRF.stop_token_manager()
			self.refreshTimer.stop()

	def __del__(self):
		self.timer.stop()
		self.refreshTimer.stop()
		print ('bye')

	def __exit__(self):
		print ('CYA')
		self.timer.stop()

	def closeEvent(self, event):
		self.timer.stop()
		self.I.NRF.stop_token_manager()
		self.refreshTimer.stop()


if __name__ == "__main__":
	from SEEL import interface
	app = QtGui.QApplication(sys.argv)
	myapp = AppWindow(I=interface.connect())
	myapp.show()
	sys.exit(app.exec_())
