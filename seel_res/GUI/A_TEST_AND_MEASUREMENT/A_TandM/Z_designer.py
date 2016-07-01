#!/usr/bin/python
'''
design experiments

'''
from __future__ import print_function
from SEEL_Apps.utilitiesClass import utilitiesClass

from SEEL_Apps.templates import ui_designer as designer
from SEEL_Apps.templates.widgets.ui_sweep import Ui_Form as ui_sweep
from SEEL_Apps.templates.widgets.ui_customFunc import Ui_Form as ui_custom

import pyqtgraph as pg
import time,random,functools,numbers
import numpy as np


from PyQt4 import QtCore, QtGui

params = {
'image' : 'sensors.png',
'name':'Experiment\nDesigner',
'hint':'''
	Design your own experiment layout by choosing channels to sweep/monitor/plot.
	'''
}

class AppWindow(QtGui.QMainWindow, designer.Ui_MainWindow,utilitiesClass):
	def __init__(self, parent=None,**kwargs):
		super(AppWindow, self).__init__(parent)
		self.setupUi(self)
		self.I=kwargs.get('I',None)
		self.setWindowTitle(self.I.H.version_string+' : '+params.get('name','').replace('\n',' ') )

		self.sweeps={}
		self.statics=[]
		self.monitors={}
		self.staticMap = {'W1':self.addW1,'W2':self.addW2,'PV1':self.addPV1,'PV2':self.addPV2,'PV3':self.addPV3,'PCS':self.addPCS,'SQR1':self.addSQR1,'VOLTMETER':self.addVoltmeter,'OHMMETER':self.addRes}
		self.widgets={}
		self.customWidgetCount=0
		self.evalGlobals={}
		self.evalGlobals = {k: getattr(self.I, k) for k in dir(self.I)}
		self.evalGlobals['CH1']=self.I.get_version()#functools.partial(self.I.get_voltage,'CH1')
		#print (self.evalGlobals)
		#eval('print(CH1)',globals(),self.evalGlobals)
		
		###################################POPULATE MONITORS LIST################################
		mons = self.I.allAnalogChannels
		mons.remove('MIC')
		num=0
		self.monitorLayout.setAlignment(QtCore.Qt.AlignTop)
		for a in mons:
			box=QtGui.QCheckBox('%s'%a)
			box.setChecked(False)
			#action.setStyleSheet("background-color:rgb%s;"%(str(curves[a].opts['pen'].color().getRgb())))
			self.sampleReadbacks.addWidget(box,num%3,num/3)
			self.monitors[a] = [box,'voltage']
			self.evalGlobals[a]=functools.partial(self.I.get_voltage,a)
			num+=1
		
		self.addParamButton = QtGui.QPushButton(); self.addParamButton.setText('Create New Parameter');self.monitorLayout.addWidget(self.addParamButton)
		self.addParamButton.clicked.connect(self.addCustom)

		
		self.columnFuncs=[]  #A collection of tuples on how to evaluate each column
		self.maxrows = 0
		self.maxcols = 0
		self.evaluatorLocation = None
		self.timer = self.newTimer()
		self.timer.timeout.connect(self.evaluator)

		###################################POPULATE STATIC OUTPUTS LIST##########################
		self.outputs['PV1']['func'] = self.I.set_pv1
		self.outputs['PV2']['func'] = self.I.set_pv2
		self.outputs['PV3']['func'] = self.I.set_pv3
		self.outputs['PCS']['func'] = self.I.set_pcs
		self.outputs['W1']['func'] = self.I.set_w1
		self.outputs['W2']['func'] = self.I.set_w2
		self.outputs['SQR1']['func'] = self.I.sqr1

		for a in self.outputs.keys()+['VOLTMETER','OHMMETER']:
			box=QtGui.QCheckBox('%s'%a)
			box.setChecked(False)
			#action.setStyleSheet("background-color:rgb%s;"%(str(curves[a].opts['pen'].color().getRgb())))
			self.staticLayout.addWidget(box)
			self.statics.append(box)

		###################################POPULATE SWEEP LIST##################################
		for a in self.outputs:
			out = self.outputs[a]
			box=self.sweepHandler(title=a,**out)
			self.sweepLayout.addWidget(box)
			self.sweeps[a]=box

		###################################CREATE PLOT#########################################
		self.plot=self.add2DPlot(self.plot_area)
		self.plot.getAxis('left').setLabel('Time',units='S')
		self.plot.getAxis('left').setLabel('VL', units='V')
		self.curves=[]; self.curveLabels=[]


		###################################   LOAD A PRESET LIST  #########################
		preset = kwargs.get('preset',[])
		for p in preset:
			cstm = self.addCustom()
			cstm.cmd.setText(p['cmd'])
			cstm.name.setText(p['name'])
			cstm.enable.setChecked(True)

	class customHandler(QtGui.QFrame,ui_custom):
		def __init__(self,**kwargs):
			super(AppWindow.customHandler, self).__init__()
			self.setupUi(self)
			self.I = kwargs.get('I',None)
			self.evalGlobals = kwargs.get('evalGlobals',None)

		def remove(self):
			self.setParent(None)

		def getFunc(self):
			tx = self.cmd.text()
			def fn():
				return eval(tx,globals(),self.evalGlobals)
			return fn

		def isChecked(self):
			return self.enable.isChecked()

		def text(self):
			return self.name.text()

	def addCustom(self):
		cstm = self.customHandler(I = self.I,evalGlobals = self.evalGlobals)
		self.monitorLayout.addWidget(cstm)
		self.monitors['CSTM'+str(self.customWidgetCount)] = [cstm,'custom']
		self.customWidgetCount+=1
		return cstm




	def prepare(self):
		self.eTabs.setCurrentIndex(2) #Switch to experiment tab
		self.columnFuncs=[] 		  #Reset the collection of tuples on how to evaluate each column

		for a in range(self.maxcols+1):  ## clear the table
			for b in range(self.maxrows):
				self.tbl.setItem(b,a,None)
				self.tbl.setCellWidget(b,a,None)
		self.maxcols = 0
		self.maxrows = 0
		
		for a in self.widgets:
			self.widgets[a].setParent(None)
		self.widgets={}


		##########################################  PREPARATION  #########################################################
		tblheaders = []
		#Sweep inputs
		for a in self.sweeps:
			if self.sweeps[a].title.isChecked():
				tblheaders.append(a)
				self.columnFuncs.append([1,self.outputs[a]['func']])  # 1= output , function to use
			
		#############    prepare monitor readback commands    ################ 
		for a in self.monitors:
			widget = self.monitors[a][0]
			if self.monitors[a][1]=='voltage': func =  functools.partial(self.I.get_voltage,a)
			if self.monitors[a][1]=='custom':  func =  widget.getFunc()
			
			if widget.isChecked():
				tblheaders.append(str(widget.text()))
				self.columnFuncs.append([0,func])  # 0= input , function to use
		tblheaders.append('Evaluate')
		self.tbl.setColumnCount(len(tblheaders))  #Last column will have push buttons for each row
		self.tbl.setHorizontalHeaderLabels(tblheaders)
		###################################################################################################################


		##############    populate sweep columns    #############
		for a in self.sweeps:
			if self.sweeps[a].title.isChecked():
				vals = np.linspace(self.sweeps[a].startBox.value(),self.sweeps[a].stopBox.value(),self.sweeps[a].numBox.value() )				
				self.maxrows = max(len(vals),self.maxrows)
				self.tbl.setRowCount(self.maxrows)				
				for num in range(len(vals)):
					item = QtGui.QTableWidgetItem();item.setText('%.4f'%(vals[num]));self.tbl.setItem(num, self.maxcols, item)#;item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
				self.maxcols+=1

		if self.maxcols == 0:  #No sweeps were selected
			reply = QtGui.QMessageBox.question(self, 'Connection', 'No sweep channels were selected!\nReturn to editor?', QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
			if reply == QtGui.QMessageBox.Yes:
				self.eTabs.setCurrentIndex(1) #Go back to editing
				return
		##############   populate monitor columns    #############
		for a in self.monitors:
			widget = self.monitors[a][0]
			if widget.isChecked():
				for b in range(self.maxrows):
					item = QtGui.QTableWidgetItem();item.setText('');self.tbl.setItem(b, self.maxcols, item)#;item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
				self.maxcols+=1

		################# make readback buttons ##############
		for a in range(self.maxrows):
			item = QtGui.QPushButton();item.setText('Calc'); item.clicked.connect(functools.partial(self.evaluateRow,a))
			self.tbl.setCellWidget(a, self.maxcols, item)#;item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)


		###################  Make the static widgets  ######################
		row=0;col=0
		for a in self.statics:
			if a.isChecked():
				print (a.text())
				widget = self.staticMap[str(a.text())](self.I)
				self.controlsLayout.addWidget(widget,row,col)
				self.widgets[str(a.text())] = widget
				col+=1
				if col==3:
					col=0;row+=1


	def evaluateRow(self,row):
		for a in range(self.maxcols):
			tp = self.columnFuncs[a]
			if tp[0]:  #Set output
				try:
					item = self.tbl.item(row,a)
					item.setText('%.3f'%tp[1](float(item.text())) )
				except:
					pass
			else:  #read input
				try:
					val = tp[1]()
					item = self.tbl.item(row,a); 
					if isinstance(val,numbers.Number):item.setText('%.4f'%val)
					else: item.setText(val)
				except:pass

	def clearColumn(self):
		pass

	def runAll(self):
		self.evaluatorLocation = 0
		self.timer.start(self.delayBox.value())

	def evaluator(self):
		if self.evaluatorLocation==None:
			print ('evaluation finished')
			self.timer.stop()
			return
		self.tbl.selectRow(self.evaluatorLocation)
		self.evaluateRow(self.evaluatorLocation)
		self.evaluatorLocation+=1
		if self.evaluatorLocation==self.maxrows:
			self.evaluatorLocation=None
			self.timer.stop()


	class sweepHandler(QtGui.QFrame,ui_sweep):
		def __init__(self,**kwargs):
			super(AppWindow.sweepHandler, self).__init__()
			self.setupUi(self)
			self.title.setText(kwargs.get('title','Not Set'))
			self.startBox.setMinimum(kwargs.get('min',0));self.startBox.setMaximum(kwargs.get('max',1));self.startBox.setValue(kwargs.get('min',0))
			self.stopBox.setMinimum(kwargs.get('min',0));self.stopBox.setMaximum(kwargs.get('max',1));self.stopBox.setValue(kwargs.get('max',0))
			self.setToolTip(kwargs.get('tooltip',''))

		

	#Just a little something to enable copying data from the table
	def keyPressEvent(self, e):
		if (e.modifiers() & QtCore.Qt.ControlModifier):
			if e.key() == QtCore.Qt.Key_C: #copy
				self.copyTable()

	def copyTable(self):
			selected = self.tbl.selectedRanges()
			s = '\t'+"\t".join([str(self.tbl.horizontalHeaderItem(i).text()) for i in xrange(selected[0].leftColumn(), selected[0].rightColumn()+1)])
			s = s + '\n'

			for r in xrange(selected[0].topRow(), selected[0].bottomRow()+1):
				#Add vertical headers
				try: s += self.tbl.verticalHeaderItem(r).text() + '\t'
				except:	s += str(r)+'\t'
				
				for c in xrange(selected[0].leftColumn(), selected[0].rightColumn()+1):
					try:
						s += str(self.tbl.item(r,c).text()) + "\t"
					except AttributeError:
						s += "\t"
				s = s[:-1] + "\n" #eliminate last '\t'
			self.clip = QtGui.QApplication.clipboard()
			self.clip.setText(s)


	def plotColumns(self):
		selected = self.tbl.selectedRanges()
		x=[]
		y=[]
		if len(selected)==0:
			self.displayDialog('Please Select at least two columns')
			return

		if len(selected)==1:
			if selected[0].leftColumn() == selected[0].rightColumn():
				self.displayDialog('Please Select at least two columns')
				return
			for a in xrange(selected[0].topRow(), selected[0].bottomRow()+1): x.append(float(self.tbl.item(a,selected[0].leftColumn()).text()))
			for a in xrange(selected[0].topRow(), selected[0].bottomRow()+1): y.append(float(self.tbl.item(a,selected[0].leftColumn()+1).text()))
			name = str(self.tbl.horizontalHeaderItem(selected[0].leftColumn()).text())+' vs '+ str(self.tbl.horizontalHeaderItem(selected[0].leftColumn()+1).text())
		elif len(selected)==2:
			for a in xrange(selected[0].topRow(), selected[0].bottomRow()+1): x.append(float(self.tbl.item(a,selected[0].leftColumn()).text()))
			for a in xrange(selected[1].topRow(), selected[1].bottomRow()+1): y.append(float(self.tbl.item(a,selected[1].leftColumn()).text()))
			name = str(self.tbl.horizontalHeaderItem(selected[0].leftColumn()).text())+' vs '+ str(self.tbl.horizontalHeaderItem(selected[1].leftColumn()).text())

		AllItems = [self.plotList.itemText(i) for i in range(self.plotList.count())]
		num=1
		while name+' #'+str(num) in AllItems:
			num+=1
		name = name+' #'+str(num)
		self.eTabs.setCurrentIndex(3) #Switch to plot tab
		curve = self.addCurve(self.plot,name)
		curve.setData(x,y)
		txt='<div style="text-align: center"><span style="color: #FFF;font-size:8pt;">%s</span></div>'%(name)
		text = pg.TextItem(html=txt, anchor=(0,0), border='w', fill=(0, 0, 255, 100))
		self.plot.addItem(text)
		text.setPos(x[-1],y[-1])
		self.plotList.addItem(name)  
		self.curveLabels.append(text)
		self.curves.append(curve)
		self.plot.autoRange()



	def deleteCurve(self):
		c = self.plotList.currentIndex()
		if c>-1:
			self.plotList.removeItem(c)
			self.removeCurve(self.plot,self.curves[c]);
			self.plot.removeItem(self.curveLabels[c]);
			self.curves.pop(c);self.curveLabels.pop(c);
			if len(self.curves)==0: # reset counter for plot numbers
				self.plotnum=0
	
	def saveData(self):
		self.saveDataWindow(self.curves,self.plot)


	def saveProfile(self):
		from SEEL_Apps import saveProfile
		from os.path import expanduser
		path = QtGui.QFileDialog.getSaveFileName(self, 'Save Profile',  expanduser("./"), 'INI(*.ini)')
		if path:
			sections = path.split('.')
			if(sections[-1]!='ini'):path+='.ini'
			saveProfile.guisave(self.selectTab, QtCore.QSettings(path, QtCore.QSettings.IniFormat))
		
	def __del__(self):
		self.timer.stop()
		print ('bye')

	def closeEvent(self, event):
		self.timer.stop()
		self.finished=True
		

if __name__ == "__main__":
	from SEEL import interface
	import sys
	app = QtGui.QApplication(sys.argv)
	#P=[{'name':'res','cmd':'CH1'}]  #An array of dictionaries defining custom functions
	myapp = AppWindow(I=interface.connect())#,preset = P)
	myapp.show()
	sys.exit(app.exec_())
