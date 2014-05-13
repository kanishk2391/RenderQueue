import os
import shutil
import maya.cmds as cmds


class RenderQueue(object):
    #Default Paths
    PROJ_ROOT      = "E:\PythonStuff\RenderQueue"
    UI_FILE         = PROJ_ROOT+"\RenderQueue_UI.ui"

    
    def __init__(self):
        self._objectList    = []

        self._windowName = "RenderQueue"
        self._assetGrid     = ""
        self._importedList  = ""
    def abc(self):
        print "dummy"
   
    def _getUI(self,name):
        items = cmds.lsUI(dumpWidgets=True)
        for item in items:
            if self._windowName in item:
                self._objectList.append(item)
        for item in self._objectList:
            if item.endswith(name):
                return item
        print self._objectList
                 
    def showQueue(self):
    	win = cmds.loadUI(f = UI_FILE)
    	cmds.button(self._getUI("submit_button"), e=True, command="self.abc()")
    	cmds.showWindow(win)