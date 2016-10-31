#!/usr/bin/python
'''
Flow based programming
'''
from __future__ import print_function

from SEEL_Apps.utilitiesClass import utilitiesClass
from templates import ui_hackYourOwn as hackYourOwn


import pyqtgraph as pg

try:
    from collections import OrderedDict
except ImportError:
    # fallback: try to use the ordereddict backport when using python 2.6
    from ordereddict import OrderedDict

from pyqtgraph.flowchart import Flowchart, Node
import pyqtgraph.flowchart.library as fclib
from pyqtgraph.flowchart.library.common import CtrlNode

import time,random,functools,sys,numbers
import numpy as np


from PyQt4 import QtCore, QtGui

params = {
'image' : 'sensors.png',
'name':'Make a\nFlow Chart',
'hint':'''
	Hack your own code by dragging and dropping graphical code blocks for rapid prototyping.<br> severely in beta testing mode. <br> Also known as flow based programming.
	'''
}

################################################################################################
#######################--------DEFINE OUR CUSTOM NODE GENERATORS------------####################
################################################################################################
from SEEL_Apps.templates.widgets.ui_dial_free import Ui_Form as dial_free
from SEEL_Apps.templates.widgets.ui_label_free import Ui_Form as label_free
from SEEL_Apps.templates.widgets.ui_combo_free import Ui_Form as combo_free
from SEEL_Apps.templates.widgets.ui_text_free import Ui_Form as text_free
from SEEL_Apps.templates.widgets.ui_button_free import Ui_Form as button_free
from SEEL_Apps.templates.widgets.ui_input_free import Ui_Form as input_free
from SEEL_Apps.templates.widgets.ui_sweep_free import Ui_Form as ui_sweep
from SEEL_Apps.templates.widgets.ui_generic_free import Ui_Form as generic_free

class utils:
	def __init__(self):
		pass

	def applySIPrefix(self,value, unit='',precision=2 ):
			neg = False
			if value < 0.:
				value *= -1; neg = True
			elif value == 0.:  return '0 '  # mantissa & exponnt both 0
			exponent = int(np.log10(value))
			if exponent > 0:
				exponent = (exponent // 3) * 3
			else:
				exponent = (-1*exponent + 3) // 3 * (-3)

			value *= (10 ** (-exponent) )
			if value >= 1000.:
				value /= 1000.0
				exponent += 3
			if neg:
				value *= -1
			exponent = int(exponent)
			PREFIXES = "yzafpnum kMGTPEZY"
			prefix_levels = (len(PREFIXES) - 1) // 2
			si_level = exponent // 3
			if abs(si_level) > prefix_levels:
				raise ValueError("Exponent out range of available prefixes.")
			return '%.*f %s%s' % (precision, value,PREFIXES[si_level + prefix_levels],unit)

class dialIcon(QtGui.QFrame,dial_free,utils):
	def __init__(self,**args):
		super(dialIcon, self).__init__()
		self.setupUi(self)
		self.units = args.get('units','')
		self.dial.setMinimum(args.get('min',0));	self.dial.setMaximum(args.get('max',100))
		self.dial.setEnabled(args.get('enabled',True))

	def setValue(self,retval):
		if isinstance(retval,numbers.Number):
			self.value.setText('%s'%(self.applySIPrefix(retval,self.units) ))
		else: self.value.setText(str(retval))

class labelIcon(QtGui.QFrame,label_free,utils):
	def __init__(self,**args):
		super(labelIcon, self).__init__()
		self.setupUi(self)
		self.units = args.get('units','')

	def setValue(self,retval):
		if isinstance(retval,numbers.Number):
			self.value.setText('%s'%(self.applySIPrefix(retval,self.units) ))
		else: self.value.setText(str(retval))

class comboIcon(QtGui.QFrame,combo_free,utils):
	def __init__(self,**args):
		super(comboIcon, self).__init__()
		self.setupUi(self)
		self.comboBox.addItems(args.get('items',[]))

	def currentText(self):
		return self.comboBox.currentText()

class textIcon(QtGui.QFrame,text_free,utils):
	def __init__(self,**args):
		super(textIcon, self).__init__()
		self.setupUi(self)

	def setText(self,txt):
		self.textBrowser.setText(txt)

class plotTextIcon(QtGui.QFrame,text_free,utils):
	def __init__(self,**args):
		super(plotTextIcon, self).__init__()
		self.setupUi(self)
		self.btn=self.myColorButton(color=(220,250,220,255))
		#self.btn.
		self.btn.sigColorChanging.connect(self.change)
		self.layout.addWidget(self.btn)
		self.curve = None

	class myColorButton(pg.ColorButton):
		'''
		inheriting and overriding paint event to reduce the boundary.
		'''
		def __init__(self,**args):
			super(plotTextIcon.myColorButton, self).__init__(**args)
		def paintEvent(self, ev):
			QtGui.QPushButton.paintEvent(self, ev)
			p = QtGui.QPainter(self)
			rect = self.rect().adjusted(2, 2, -2, -2)
			## reduce white base. It's a bit too much , then texture for indicating transparency, then actual color
			p.setBrush(pg.functions.mkBrush('w'))
			p.drawRect(rect)
			p.setBrush(QtGui.QBrush(QtCore.Qt.DiagCrossPattern))
			p.drawRect(rect)
			p.setBrush(pg.functions.mkBrush(self._color))
			p.drawRect(rect)
			p.end()
		
	def change(self,btn):
		if self.curve is not None: self.curve.setPen(color=btn.color().getRgb()) 
		
	def setText(self,txt):
		self.textBrowser.setText(txt)

class buttonIcon(QtGui.QFrame,button_free,utils):
	def __init__(self,**args):
		super(buttonIcon, self).__init__()
		self.setupUi(self)
		self.pushButton.setText(args.get('text',''))
		self.func = args.get('func',None)

	def run(self,txt):
		self.func()

class inputIcon(QtGui.QFrame,input_free,utils):
	def __init__(self,**args):
		super(inputIcon, self).__init__()
		self.setupUi(self)
		self.func = args.get('func',None)
		self.nameFunc = args.get('nameFunc',None)
		self.nameFunc('STOPPED')
		self.data = True
		self.dataset = []
		self.position = 0

		self.setup_btn.setMenu(QtGui.QMenu(self.setup_btn))
		self.params = self.sweepHandler()
		#self.params.setZValue(1000)
		action = QtGui.QWidgetAction(self.setup_btn)
		action.setDefaultWidget(self.params)
		self.setup_btn.menu().addAction(action)
		
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.singleLoop)

	class sweepHandler(QtGui.QFrame,ui_sweep):
		def __init__(self,**kwargs):
			super(inputIcon.sweepHandler, self).__init__()
			self.setupUi(self)
			self.comboBox.setCurrentIndex(1)
			self.sweepFrame.setVisible(False)
			self.loopType = 1

		def setType(self,val):
			self.continuousFrame.setVisible(True if val == 1 else False)
			self.sweepFrame.setVisible(True if val == 0 else False)
			self.loopType = val #0 if sweep . 1 if continuous



	def checkLoop(self):
		self.func(In=self.params.valueBox.value())
		self.value.setText('%.1e'%(self.params.valueBox.value()))

	def singleLoop(self):
		if not self.params.loopType: #sweep
			if self.position >= self.dataset.size:
				self.stopLoop()
				return
			self.func(In=self.dataset[self.position])
			self.value.setText('%.1e'%(self.dataset[self.position]))
			self.position+=1
		else:                        #continuous			
			self.func(In = self.params.valueBox.value())

	def startLoop(self):
		self.nameFunc('PLAYING')
		if not self.params.loopType: #sweep
			self.dataset = np.linspace(self.params.startBox.value(),self.params.stopBox.value(),self.params.numBox.value())
			self.position = 0
			self.timer.start(10)
		else:
			self.timer.start(self.params.intervalBox.value())
			
	def pauseLoop(self):
		self.nameFunc('PAUSED')
		self.timer.stop()
	def stopLoop(self):
		self.nameFunc('STOPPED')
		self.timer.stop()
	def setupLoop(self):
		pass

class genericIcon(QtGui.QFrame,generic_free,utils):
	def __init__(self,*args,**kwargs):
		super(genericIcon, self).__init__()
		self.setupUi(self)
		self.widgets = []
		self.count = 0
		for a in args:			
			self.widgets.append(a)
			self.widgetLayout.addWidget(a)

def addWidget(parent,widgetType,*args,**kwargs):
	proxy = QtGui.QGraphicsProxyWidget(parent)
	widgets = {'dial':dialIcon,'label':labelIcon,'combo':comboIcon,'text':textIcon,'plotText':plotTextIcon,'button':buttonIcon,'input':inputIcon,'generic':genericIcon}
	wd = widgets.get(widgetType,None)(*args,**kwargs)	
	wd.setStyleSheet('''
	#Form{
    border: 2px solid rgba(255, 255, 255, 90);
    border-radius: 2px;
	background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 178, 102, 100), stop:0.55 rgba(235, 148, 61, 100), stop:0.98 rgba(0, 0, 0, 120), stop:1 rgba(0, 0, 0, 0));
	QLabel {
		color: white;
		background:grey;
		}
	}
	'''
	)
	proxy.setWidget(wd)
	proxy.setZValue(-2)
	#if widgetType=='input':proxy.setZValue(2)
	return wd

################################################################################################
#######################--------DEFINE OUR CUSTOM NODE GENERATORS------------####################
#######################---------------------DONE----------------------------####################
################################################################################################


class AppWindow(QtGui.QMainWindow, hackYourOwn.Ui_MainWindow,utilitiesClass):
	def __init__(self, parent=None,**kwargs):
		super(AppWindow, self).__init__(parent)
		self.setupUi(self)
		print (self.utils)
		self.I=kwargs.get('I',None)
		self.I.set_sine1(5000)
		self.I.configure_trigger(0,'CH1',0)
		self.setWindowTitle('pyqtgraph example: FlowchartCustomNode')
		## Create an empty flowchart with a single input and output
		self.fc = Flowchart(terminals={
			'In': {'io': 'in'},	'dataOut': {'io': 'out'},	
		})
		self.w = self.fc.widget()

		self.ExperimentLayout.addWidget(self.w.chartWidget.view)
		#self.WidgetLayout.addWidget(self.w.chartWidget.selInfo)

		###############MODIFY INPUT NODE#############################
		self.inp = addWidget(self.fc.inputNode.graphicsItem(),'input',func = self.fc.setInput, nameFunc = self.fc.inputNode.graphicsItem().nameItem.setPlainText )

		############### CREATE USER LIBRARY #############################
		self.library = fclib.LIBRARY.copy() # start with the default node set		
		#add our custom nodes to the library
		self.library.addNodeType(self.PlotViewNode, [('Display',)])

		for a in [self.CaptureNode1,self.CaptureNode2,self.DACNode,self.VoltNode,self.GainNode]: a.I = self.I

		self.library.addNodeType(self.ArrayNode, [('Data',)])

		self.library.addNodeType(self.CaptureNode1, [('Acquire',)])
		self.library.addNodeType(self.CaptureNode2, [('Acquire',)])
		self.library.addNodeType(self.VoltNode, [('Acquire',)])

		self.library.addNodeType(self.DACNode, [('Outputs',)])
		self.library.addNodeType(self.MyEvalNode, [('Outputs',)])
		
		self.library.addNodeType(self.GainNode, [('Configure',)])
		self.library.addNodeType(self.ConstantNode, [('Configure',)])

		self.fc.setLibrary(self.library)
		
		#############    LIBRARY HAS BEEN POPULATED. NOW BUILD THE MENU     ###############

		self.menu = self.buildMenu(self.w.chartWidget)
		self.menu.setMinimumHeight(150)
		self.WidgetLayout.addWidget(self.menu)

		self.WidgetLayout.addWidget(self.w)
		self.w.ui.showChartBtn.setParent(None)
		self.w.ui.reloadBtn.setParent(None)

		#############   NEXT UP : add ui elements    ###############

		self.plot = self.add2DPlot(self.ExperimentLayout)
		self.plot.addLegend()
		self.PlotViewNode.plot = self.plot

		## Now we will programmatically add nodes to define the function of the flowchart.
		## Normally, the user will do this manually or by loading a pre-generated
		## flowchart file.

		self.cap = self.fc.createNode('Capture1', pos=(0, 0))

		self.v1Node = self.fc.createNode('2D Curve', pos=(200, -70))
		self.v2Node = self.fc.createNode('2D Curve', pos=(200, 70))


		self.fc.connectTerminals(self.fc['In'], self.cap['In'])
		self.fc.connectTerminals(self.cap['time'], self.v1Node['X'])
		self.fc.connectTerminals(self.cap['voltage'], self.v1Node['Y'])
		self.setStyleSheet("");
		
	def setInterconnects(self,val):
		if val : shape = 'cubic'
		else: shape = 'line'
		for a in self.fc.listConnections():
			for x in a[1]._graphicsItem.getViewBox().allChildren():
				if isinstance(x,pg.flowchart.TerminalGraphicsItem):
					for y in x.term.connections().items():y[1].setStyle(shape=shape)

	def runOnce(self):
		self.fc.setInput(In=True)

	def buildMenu(self, CW):
		def buildSubMenu(node, rootMenu, subMenus):
			for section, node in node.items():
				menu = QtGui.QMenu(section)
				rootMenu.addMenu(menu)
				if isinstance(node, OrderedDict): 
					buildSubMenu(node, menu, subMenus)
					subMenus.append(menu)
				else:
					act = rootMenu.addAction(section)
					act.nodeType = section
					act.pos = None

		class PermanentMenu(QtGui.QMenu):
			def hideEvent(self, event):
				self.show()

		menu = PermanentMenu()
		self.subMenus = []
		buildSubMenu(CW.chart.library.getNodeTree(), menu, self.subMenus)
		menu.triggered.connect(CW.nodeMenuTriggered)
		CW.menuPos = QtCore.QPoint(100,150)
		return menu
		#self.v3Node = self.fc.createNode('PlotView', pos=(300, -150))
		#self.v3Node.setView(self.curve1)
		#self.fc.connectTerminals(self.cap['dataOut'], self.v1Node['data'])

	def __del__(self):
		#self.looptimer.stop()
		print ('bye')

	def closeEvent(self, event):
		self.finished=True
		self.fc._widget.chartWidget.close()



	################################################################################################
	#######################--------Display Function calls start here------------####################
	################################################################################################

	class PlotViewNode(Node,utilitiesClass):
		"""Node that displays plot data in an Plotwidget"""
		nodeName = '2D Curve'
		def __init__(self, name):
			self.view = None
			Node.__init__(self, name, terminals=OrderedDict([  ('X',dict(io='in')),('Y', dict(io='in')),('dY', dict(io='in',optional=True))  ]))
			self.txt = addWidget(self.graphicsItem(),'plotText')			
			self.curveName = self._name
			self.curve = self.addCurve(self.plot,self.curveName) #self.plot is set by the parent prior to initialization
			self.txt.curve = self.curve
			self.sigRenamed.connect(self.renamed)

		def renamed(self, node, oldName):
			print ('renamed from ', oldName,' to ',self._name )
			self.renameLegendItem(self.plot.plotItem.legend,oldName,self._name)

		def process(self, X,Y,dY):
			if X is not None and Y is not None:
				if len(X)==len(Y):
					self.txt.setText('length=%d\nx: %s\ny: [%s]...'%(len(X),str(X[:20])," ".join(format(a, ".1f") for a in Y[:20]) ))
					try:
						if dY is not None and self.plot is not None:
							self.plot.setYRange(dY[0],dY[1])
					except Exception as e:
						print (e)
					self.curve.setData(X,Y)
					return
			self.curve.setData([])

	################################################################################################
	#######################--------Container Function calls start here------------##################
	################################################################################################

	class ArrayNode(CtrlNode):
		nodeName = '1DArray'
		uiTemplate = [
		]
		def __init__(self, name):
			self.A = []
			terminals = {'dataIn': dict(io='in'),'ArrayOut': dict(io='out')	}                              
			CtrlNode.__init__(self, name, terminals=terminals)
			
		def process(self, dataIn, display=False):
			try:
				self.A.append(float(dataIn))
			except Exception as e:
				print (e)
			return {'ArrayOut': np.array(self.A)}

	################################################################################################
	#######################--------Input Function calls start here------------######################
	################################################################################################

	class CaptureNode1(CtrlNode):
		nodeName = 'Capture1'
		uiTemplate = [
			('samples', 'spin', {'value': 1000, 'dec': False, 'step': 10, 'minStep': 1, 'bounds': [0, 10000]}),
			('timegap', 'spin', {'value': 1, 'dec': False, 'step': 10, 'minStep': 1, 'bounds': [0, 100]}),
		]

		def __init__(self, name):
			terminals = OrderedDict([('In',dict(io='in')),('time', dict(io='out')) ,('voltage',dict(io='out')) ,('dV',dict(io='out')) ])
			CtrlNode.__init__(self, name, terminals=terminals)
			self.comboBox = addWidget(self.graphicsItem(),'combo',items = self.I.allAnalogChannels)

		def process(self, In, display=False):
			try:
				x,y = self.I.capture1(self.comboBox.currentText(),int(self.ctrls['samples'].value()),int(self.ctrls['timegap'].value()))
				return {'time': x,'voltage':y,'dV':self.I.achans[0].get_Y_range()}
			except Exception as e:
				print (e)
			return {'time': None,'voltage':None}

	class CaptureNode2(CtrlNode):
		nodeName = 'Capture2'
		uiTemplate = [
			('samples', 'spin', {'value': 1000, 'dec': False, 'step': 10, 'minStep': 1, 'bounds': [0, 5000]}),
			('timegap', 'spin', {'value': 1, 'dec': False, 'step': 10, 'minStep': 1, 'bounds': [0, 100]}),
		]

		def __init__(self, name):
			terminals = OrderedDict([('In',dict(io='in')),('time', dict(io='out')) ,('V_CH1',dict(io='out')) ,('V_CH2',dict(io='out'))])
			CtrlNode.__init__(self, name, terminals=terminals)
			self.comboBox = addWidget(self.graphicsItem(),'combo',items = self.I.allAnalogChannels)

			
		def process(self, In, display=False):
			try:
				x,y1,y2 = self.I.capture2(self.ctrls['samples'].value(),self.ctrls['timegap'].value(), self.comboBox.currentText())
				return {'time': x,'V_CH1':y1,'V_CH2':y2}
			except Exception as e:
				print (e)
			return {'time': None,'V_CH1':None,'V_CH2':None}

	class VoltNode(CtrlNode):
		nodeName = 'AnalogIn'
		uiTemplate = [
			('channel',  'combo', {'values':['CH1','CH2','CH3','AN8','SEN','CAP']}),
		]

		def __init__(self, name):
			terminals = {'trig': dict(io='in'),'V_out': dict(io='out') }                              
			CtrlNode.__init__(self, name, terminals=terminals)
			
		def process(self, trig, display=False):
			if trig!=None:
				try:
					val = self.I.get_voltage(self.ctrls['channel'].currentText())
					return {'V_out':val}
				except Exception as e:
					print (e)
			return {'V_out':None}

	################################################################################################
	#######################-----------Options and settings start here------------###################
	################################################################################################

	class GainNode(CtrlNode,utilitiesClass):
		nodeName = 'AnalogGain'

		def __init__(self, name):
			terminals = {}
			CtrlNode.__init__(self, name, terminals=terminals)
			self.graphicsItem().nameItem.setPlainText('')
			self.wg = self.gainIcon(FUNC = self.I.set_gain)
			self.comboBox = addWidget(self.graphicsItem(),'generic',self.wg)
			
		def process(self, display=False):
			pass#return {'Y_CH1':self.I.achans['CH1'].get_Y_range(),'Y_CH2':self.I.achans['CH2'].get_Y_range()}

	class ConstantNode(CtrlNode):
		nodeName = 'Constant'

		def __init__(self, name):
			terminals = {'value': {'io': 'out',  'multiable': True}}
			CtrlNode.__init__(self, name, terminals=terminals)
			
		def process(self, display=False):
			return {'value':[-4,4]}



	################################################################################################
	#######################----------Output Function calls start here------------###################
	################################################################################################

	class DACNode(CtrlNode):
		nodeName = 'PVx'
		uiTemplate = [
			('channel',  'combo', {'values':['PV1','PV2','PV3']}),
		]

		def __init__(self, name):
			terminals = {'V_in': dict(io='in'),'V_out': dict(io='out') }                              
			CtrlNode.__init__(self, name, terminals=terminals)

		def process(self, V_in, display=False):
			if V_in:
				try:
					val = self.I.DAC.setVoltage(self.ctrls['channel'].currentText(),V_in)
					return {'V_out':val}
				except Exception as e:
					print (e)
			return {'V_out':None}

	class MyEvalNode(Node):
		"""Return the output of a string evaluated/executed by the python interpreter.
		The string may be either an expression or a python script, and inputs are accessed as the name of the terminal. 
		For expressions, a single value may be evaluated for a single output, or a dict for multiple outputs.
		For a script, the text will be executed as the body of a function."""
		nodeName = 'MyPythonEval'
		
		def __init__(self, name):
			Node.__init__(self, name, 
				terminals = {
					'input': {'io': 'in', 'renamable': True, 'multiable': True},
					'output': {'io': 'out', 'renamable': True, 'multiable': True},
				},
				allowAddInput=True, allowAddOutput=True)
			
			self.ui = QtGui.QWidget()
			self.layout = QtGui.QGridLayout()
			self.text = QtGui.QTextEdit()
			self.text.setTabStopWidth(30)
			self.text.setPlainText("# Access inputs as args['input_name']\nreturn {'output': None} ## one key per output terminal")
			self.layout.addWidget(self.text, 1, 0, 1, 2)
			self.ui.setLayout(self.layout)
			
			#QtCore.QObject.connect(self.addInBtn, QtCore.SIGNAL('clicked()'), self.addInput)
			#self.addInBtn.clicked.connect(self.addInput)
			#QtCore.QObject.connect(self.addOutBtn, QtCore.SIGNAL('clicked()'), self.addOutput)
			#self.addOutBtn.clicked.connect(self.addOutput)
			self.text.focusOutEvent = self.focusOutEvent
			self.lastText = None
			
			
		def focusOutEvent(self, ev):
			text = str(self.text.toPlainText())
			if text != self.lastText:
				self.lastText = text
				self.update()
			return QtGui.QTextEdit.focusOutEvent(self.text, ev)
			
		def process(self, display=True, **args):
			l = locals()
			l.update(args)
			## try eval first, then exec
			try:  
				text = str(self.text.toPlainText()).replace('\n', ' ')
				output = eval(text, globals(), l)
			except SyntaxError:
				fn = "def fn(**args):\n"
				run = "\noutput=fn(**args)\n"
				text = fn + "\n".join(["    "+l for l in str(self.text.toPlainText()).split('\n')]) + run
				exec(text)
			except:
				print("Error processing node: %s" % self.name())
				raise
			return output
			
		def saveState(self):
			state = Node.saveState(self)
			state['text'] = str(self.text.toPlainText())
			return state
			
		def restoreState(self, state):
			Node.restoreState(self, state)
			self.text.clear()
			self.text.insertPlainText(state['text'])
			self.restoreTerminals(state['terminals'])
			self.update()


		
if __name__ == "__main__":
	from SEEL import interface
	app = QtGui.QApplication(sys.argv)
	myapp = AppWindow(I=interface.connect())
	myapp.show()
	sys.exit(app.exec_())
