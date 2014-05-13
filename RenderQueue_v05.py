import os
import shutil
import maya.cmds as cmds
from xml.dom.minidom import Document
import xml.dom.minidom as xd

PROJ_ROOT      = "D:\kani\Python\RenderQueue-2014-05-04\RenderQueue"
UI_FILE         = PROJ_ROOT+"\RenderQueue_UI_v2.ui"

class RenderQueue(object):
  
    def __init__(self):
        self._objectList    = []
        self._windowName = "RenderQueue"
        
        
    #Add files to the list    
    def submitFile(self):
        
        
        self._importedList  = self.getUI("renderList")
        cmds.textScrollList(self._importedList, e=True,append = "Hellop || Rendered || WIP || %s"%c)
        c=c+1
    #Refresh the list in the UI  
    def refreshList(self):
        c=0
        path = "D:/kani/Python/RenderQueue-2014-05-04/RenderQueue/queue.xml"
        xFile = xd.parse(path)
        xmlElements = xFile.getElementsByTagName("File")
        #cmds.textScrollList(self.getUI("fileNameList"), e=True,removeAll=True)
        #cmds.textScrollList(self.getUI("filePathList"), e=True,removeAll=True)
        #cmds.textScrollList(self.getUI("timeList"), e=True,removeAll=True)
        for files in xmlElements:
            c=c+1
            fPath=files.attributes["FilePath"].value
            fName=files.attributes["FileName"].value
            fTime=files.attributes["Time"].value
            cmds.textScrollList(self.getUI("fileNameList"), e=True,append =str(fName))
            cmds.textScrollList(self.getUI("filePathList"), e=True,append =str(fPath))
            cmds.textScrollList(self.getUI("timeList"), e=True,append =str(ftime))
        print x
                  
    #Delete selected item from the list 
    def deleteItem(self):
        self._importedList  = self.getUI("renderList")
        selectedFile = cmds.textScrollList(self._importedList, q=True, selectItem=True)
        cmds.textScrollList(self._importedList, e=True,removeItem=selectedFile)
        print selectedFile
        
    
    def abc(self):
        return "assssddsasddas"
   
   #To find the particular UI Item....
    def getUI(self,name):
        items = cmds.lsUI(dumpWidgets=True)
        for item in items:
            if self._windowName in item:
                self._objectList.append(item)
        for item in self._objectList:
            if item.endswith(name):
                return item
        print self._objectList
        
    def close(self):
        """
        close()
            
            close an existing window
        """

        if cmds.window(self._windowName, q=True, exists=True):
            cmds.deleteUI(self._windowName)
    #Show the UI             
    def showQueue(self):
        self.close()
        
    	win = cmds.loadUI(f = UI_FILE)
    	cmds.showWindow(win)