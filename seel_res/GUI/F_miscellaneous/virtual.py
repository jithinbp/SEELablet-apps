#!/usr/bin/python
'''
Virtual Lab using PubNub
'''

from __future__ import print_function
import os

from PyQt4 import QtCore, QtGui
import time,sys
from templates import remote
import sys,json,string
import numpy as np

from json import encoder
json.JSONEncoder.FLOAT_REPR = lambda f: ("%.2f" % f)

class NumpyEncoder(json.JSONEncoder): # Answered by SO user http://stackoverflow.com/users/3768982/tlausch
	def default(self, obj):
		"""If input object is an ndarray it will be converted into a dict 
		holding dtype, shape and the data, base64 encoded.
		"""
		if isinstance(obj, np.ndarray):
			return list(obj)
		# Let the base class default method raise the TypeError
		return obj#json.JSONEncoder(self, obj)


params = {
'image' : 'mf522.png',
'helpfile': '',
'name':'Virtual\nLab',
'hint':'This listens on a PubNub channel <incoming> on\<br>pub-c-22260663-a169-4935-9c74-22925f4398af<br>sub-c-3431f4ba-2984-11e6-a01f-0619f8945a4f<br> and responds with data after executing received commands.'
}

class AppWindow(QtGui.QMainWindow, remote.Ui_MainWindow):
	def __init__(self, parent=None,**kwargs):
		super(AppWindow, self).__init__(parent)
		self.setupUi(self)
		self.I=kwargs.get('I',None)
		self.setWindowTitle(self.I.H.version_string+' : '+params.get('name','').replace('\n',' ') )
		self.res = self.resultWriter(self.results)
		self.pubEdit.setText("pub-c-22260663-a169-4935-9c74-22925f4398af")
		self.subEdit.setText("sub-c-3431f4ba-2984-11e6-a01f-0619f8945a4f")
		self.channelLabel.setText(self.I.hexid)
		self.resetKeys() #Connect to pubnub
		import inspect

		funcs=dir(self.I)
		self.methods={}
		self.function_list=[]
		for a in funcs:
			fn=getattr(self.I,a)
			try:
				args=inspect.getargspec(fn).args
			except:
				args=[]

			if len(args)>0:
				if inspect.ismethod(fn):
					self.methods[a]=(fn,args)		#list of tuples of all methods in device handler
					if args[0]=='self': self.function_list.append([a,args[1:] ])


	class resultWriter:
		def __init__(self,results):
			self.results = results
		def write(self,txt):
			self.results.append('abc')#txt)

	def callback(self,message, channel):
		self.results.append('[' + channel + ']: ' + str(message))
		
		try:
			fn_name=message.split('(')[0]

			args = message[message.find("(")+1:message.find(")")].strip().split(',')
			total_args=[]
			for t in args:
				if not len(t):continue
				if t[0]=="'" or t[0]=='"':total_args.append(t[1:-1])
				else:total_args.append(string.atoi(t))
			
			method = self.methods.get(fn_name)[0]
			if method == None :
				print ('no such command :',fn_name)
				return 'no such command : %s'%fn_name
			else:
				#while self.hw_lock and self.active: pass
				#self.hw_lock=True
				result=method(*total_args)		
				#self.hw_lock=False
				jsonres = json.dumps(result,cls=NumpyEncoder)
				print (method,total_args,type(jsonres),len(jsonres),jsonres,self.I.hexid+'response',file=self.res)
				self.pubnub.publish(channel = self.I.hexid+'response',message = jsonres)
		except Exception,e:
			self.responseLabel.setText (e.message)


	def execRemote(self):
		self.pubnub.publish(channel = hex(0x1000000000000000|int(str(self.sendID.text()),16)),message = str(self.cmdEdit.text()))

	def setListenState(self,state):
		if state: #Enable listen
			try:
				self.pubnub.subscribe(self.I.hexid,callback = self.callback)
			except Exception,e:
				self.responseLabel.setText (e)
		else:
			self.pubnub.unsubscribe(self.I.hexid)			
			
	def resetKeys(self):
		try:
			from pubnub import Pubnub
			self.pubnub = Pubnub(
				publish_key = str(self.pubEdit.text()),
				subscribe_key = str(self.subEdit.text()))
		except Exception,e:
			self.responseLabel.setText (e)



	def __del__(self):
		try:self.pubnub.stop()
		except:pass
		print ('bye')

	def closeEvent(self, event):
		try:self.pubnub.unsubscribe(self.I.hexid)
		except:pass
		self.finished=True


if __name__ == "__main__":
    from SEEL import interface
    app = QtGui.QApplication(sys.argv)
    myapp = AppWindow(I=interface.connect())
    myapp.show()
    sys.exit(app.exec_())

