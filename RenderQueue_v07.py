import os
import shutil
import maya.cmds as cmds
from xml.dom.minidom import Document
import xml.dom.minidom as xd

PROJ_ROOT      = "E:\PythonStuff\RenderQueue"
UI_FILE        = PROJ_ROOT+"\RenderQueue_UI_v4.ui"
xmlPath        = "E:\PythonStuff\RenderQueue\queue.xml"

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
        
        cmds.textScrollList(self.getUI("pathList"), e=True,removeAll=True)
        
        for files in xmlElements:
            fName=files.attributes["FileName"].value
            fPath=files.attributes["FilePath"].value
            fTime=files.attributes["Time"].value
            
            
            
            cmds.textScrollList(self.getUI("pathList"), e=True,append =str(fName)+"   ||   "+str(fPath))
                  
    #Delete selected item from the list 
    def deleteItem(self):
        self._importedList  = self.getUI("renderList")
        selectedFile = cmds.textScrollList(self._importedList, q=True, selectItem=True)
        cmds.textScrollList(self._importedList, e=True,removeItem=selectedFile)
        print selectedFile
   
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
        
    def itemSelected(self):
        xFile = xd.parse(xmlPath)
        self.importedList  = self.getUI("pathList")
        selectedFile = cmds.textScrollList(self.importedList, q=True, selectIndexedItem=True)
        xmlElements = xFile.getElementsByTagName("File")
        tmp = selectedFile[0]-1
        #FrameLabel----------------     
        x=xmlElements[tmp].attributes["Frames"].value
        cmds.text(self.getUI("frame_label"),e=True,l="Frames = "+str(x))
        
        #TimeLabel-----------------
        y=xmlElements[tmp].attributes["Time"].value
        cmds.text(self.getUI("time_label"),e=True,l="Submit Time = "+str(y))
        
        #PlayBlastLabel-----------------
        x=xmlElements[tmp].attributes["PlayBlast"].value
        cmds.text(self.getUI("playblast_label"),e=True,l="Playblast = "+str(x))
        
        #ImagePlaneLabel---------------
        #TimeLabel-----------------
        x=xmlElements[tmp].attributes["ImagePlane"].value
        cmds.text(self.getUI("imageplane_label"),e=True,l="ImagePlane = "+str(x))
        
        
    
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