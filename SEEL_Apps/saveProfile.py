#===================================================================
# Module with functions to save & restore qt widget values
# Written by: Alan Lilly 
# Website: http://panofish.net
#===================================================================

#===================================================================
# Modified by Jithin bp for the SEELablet package. Added support
# for QSlider and....    
# QCombobox ignores itemText. It's not user editable in my use case
#
#===================================================================

import sys
from PyQt4 import QtCore, QtGui
import inspect

#===================================================================
# save "ui" controls and values to registry "setting"
# currently only handles comboboxes editlines & checkboxes
# ui = qmainwindow object
# settings = qsettings object
#===================================================================

def guisave(ui, settings):
	#for child in ui.children():  # works like getmembers, but because it traverses the hierarachy, you would have to call guisave recursively to traverse down the tree
	for name, obj in inspect.getmembers(ui):
		if isinstance(obj, QtGui.QComboBox):
			name   = obj.objectName()      # get combobox name
			index  = obj.currentIndex()    # get current index from combobox
			#text   = obj.itemText(index)   # get the text for current index
			settings.setValue(name, index)   # save combobox selection to registry

		elif isinstance(obj, QtGui.QLineEdit):
			name = obj.objectName()
			value = obj.text()
			settings.setValue(name, value)    # save ui values, so they can be restored next time

		elif isinstance(obj, QtGui.QCheckBox):
			name = obj.objectName()
			state = obj.checkState()
			settings.setValue(name, state)

		elif isinstance(obj, QtGui.QDial):
			name = obj.objectName()
			state = obj.value()
			settings.setValue(name, state)


#===================================================================
# restore "ui" controls with values stored in registry "settings"
# currently only handles comboboxes, editlines &checkboxes
# ui = QMainWindow object
# settings = QSettings object
#===================================================================

def guirestore(ui, settings):
	for name, obj in inspect.getmembers(ui):
		if isinstance(obj, QtGui.QComboBox):
			name   = obj.objectName()
			index = int(settings.value(name))
			if value == "":
				continue
			obj.setCurrentIndex(index)   # preselect a combobox value by index    

		elif isinstance(obj, QtGui.QLineEdit):
			name = obj.objectName()
			value = unicode(settings.value(name))  # get stored value from registry
			obj.setText(value)  # restore lineEditFile

		elif isinstance(obj, QtGui.QCheckBox):
			name = obj.objectName()
			value = int(settings.value(name))
			if value != None:
				obj.setChecked(bool(value))   # restore checkbox

		elif isinstance(obj, QtGui.QDial):
			name   = obj.objectName()
			value = int(settings.value(name))
			if value == "":
				continue
			obj.setValue(value)


################################################################

if __name__ == "__main__":

    # execute when run directly, but not when called as a module.
    # therefore this section allows for testing this module!

    #print "running directly, not as a module!"

    sys.exit() 