import os
import shutil
import maya.cmds as cmds
from xml.dom.minidom import Document
import xml.dom.minidom as xd

PROJ_ROOT      = "E:\PythonStuff\RenderQueue"
UI_FILE         = PROJ_ROOT+"\RenderQueue_UI_v3.ui"

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
        path = "E:/PythonStuff/RenderQueue/queue.xml"
        xFile = xd.parse(path)
        xmlElements = xFile.getElementsByTagName("File")
        
        #cmds.textScrollList(self.getUI("fileNameList"), e=True,removeAll=True)
        cmds.textScrollList(self.getUI("pathList"), e=True,removeAll=True)
        #cmds.textScrollList(self.getUI("timeList"), e=True,removeAll=True)
        #cmds.textScrollList(self.getUI("playblastList"), e=True,removeAll=True)
        #cmds.textScrollList(self.getUI("imageplaneList"), e=True,removeAll=True)
        
        for files in xmlElements:
            fName=files.attributes["FileName"].value
            fPath=files.attributes["FilePath"].value
            fTime=files.attributes["Time"].value
            fPlayblast = files.attributes["PlayBlast"].value
            fImagePlane = files.attributes["ImagePlane"].value
            
            #cmds.textScrollList(self.getUI("fileNameList"), e=True,append =str(fName))
            cmds.textScrollList(self.getUI("pathList"), e=True,append =str(fPath))
            #cmds.textScrollList(self.getUI("timeList"), e=True,append =str(fTime))
            #cmds.textScrollList(self.getUI("playblastList"), e=True,append =str(fPlayblast))
            #cmds.textScrollList(self.getUI("imageplaneList"), e=True,append =str(fImagePlane))
        
                  
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