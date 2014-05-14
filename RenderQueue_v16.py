import os
import shutil
import subprocess
import maya.cmds as cmds
from xml.dom.minidom import Document
import xml.dom.minidom as xd
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as ET

PROJ_ROOT      = "E:\PythonStuff\RenderQueue"
UI_FILE        = PROJ_ROOT+"\RenderQueue_UI_v6.ui"
xmlPath        = "E:\PythonStuff\RenderQueue\queue.xml"
lightxmlPath   = "E:\PythonStuff\RenderQueue\light_queue.xml"
today          = str(cmds.date(t=True))

class RenderQueue(object):
  
    def __init__(self):
        self._objectList    = []
        self._windowName = "RenderQueue"
        
        
        
    #Add files to the list...............................................................   
    def submitFile(self):
        fileName=cmds.file(query=True,shn=True, l=True)[0]
        filePath=cmds.file(query=True, l=True)[0]
        frames = cmds.playbackOptions(q=True, max=True)
        playblastFlag = "Yes"
        imagePlaneFlag = "No"
        playblastPath = filePath[:-3]+"_plbl"
        cmds.playblast(f=playblastPath,fmt="movie",v=False)
        
        #SubmitImagePlane............
        x=cmds.getPanel(wf=True)
        filecam=cmds.modelEditor(x,q=True,camera=True)
        imageplane = cmds.listConnections('%s.imagePlane'%filecam)
        camfileName = cmds.getAttr('%s.imageName'%imageplane[0])
        camfilePath = cmds.file( q=True, l= True )[0]
        k=camfilePath.rfind('/')
        folderPath=camfilePath[:k]
        tmpSceneName = camfilePath[k+1:]
        sceneName = tmpSceneName[:-3]
        newFileName = folderPath+'/%s'%sceneName+'_LightRef'+camfileName[-4:]
        shutil.copy(camfileName, newFileName)
        
        tree = ET.ElementTree(file=xmlPath)
        file_list = tree.getroot()
        c=ET.Element('File')
        c.attrib['FileName'] = fileName
        c.attrib['FilePath'] = filePath
        c.attrib['Frames'] = str(frames)
        c.attrib['Time'] = str(today)
        c.attrib['ImagePlane'] = imagePlaneFlag
        c.attrib['PlayBlast'] = playblastFlag
        
        file_list.append(c)
        tree.write(xmlPath)
        
        self.refreshList()
        cmds.confirmDialog(title="Done!!!",message="File submitted to queue....",button = ['Ok'])
    
    #View the ImagePlane
    def viewImagePlane(self):
        selectedItem = cmds.textScrollList(self.importedList, q=True, si=True)
        s=selectedItem[0]
        x=s.rfind("||")
        k=s[x+2:]
        l = k.strip()
        path = l[:-3]+"_LightRef.jpg"
        os.startfile(path)
        
    #View the playblast
    def viewPlayblast(self):
        selectedItem = cmds.textScrollList(self.importedList, q=True, si=True)
        s=selectedItem[0]
        x=s.rfind("||")
        k=s[x+2:]
        l = k.strip()
        path = l[:-3]+"_plbl.avi"
        os.startfile(path)
    #Open the Anim File....................................................................
    def openFile(self):
        self._importedList  = self.getUI("animList")
        selectedFile = cmds.textScrollList(self._importedList, q=True, si=True)
        s=selectedFile[0]
        x=s.rfind("||")
        k=s[x+2:]
        l = k.strip()
        cmds.file( l, open=True,f=True )

   #Refresh the Lighting List..............................................................
    def refreshLightList(self):
        path = lightxmlPath
        xFile = xd.parse(path)
        xmlElements = xFile.getElementsByTagName("File")
        
        cmds.textScrollList(self.getUI("lightList"), e=True,removeAll=True)
        
        for files in xmlElements:
            fName=files.attributes["FileName"].value
            cmds.textScrollList(self.getUI("lightList"), e=True,append =str(fName)) 
  
    #Refresh the list in the UI............................................................ 
    def refreshList(self):
        path = xmlPath
        xFile = xd.parse(path)
        xmlElements = xFile.getElementsByTagName("File")
        
        cmds.textScrollList(self.getUI("animList"), e=True,removeAll=True)
        
        for files in xmlElements:
            
            fName=files.attributes["FileName"].value
            fPath=files.attributes["FilePath"].value
            fTime=files.attributes["Time"].value
            
            
            
            cmds.textScrollList(self.getUI("animList"), e=True,append =str(fName)+"   ||   "+str(fPath))
                  
    #Delete selected item from the Animation List..........................................
    def deleteAnimItem(self):
        self._importedList  = self.getUI("animList")
        selectedFile = cmds.textScrollList(self._importedList, q=True, si=True)
        s=selectedFile[0]
        x=s.rfind("||")
        k=s[:x]
        l = k.strip()
        
        import xml.etree.cElementTree as ET
        tree = ET.ElementTree(file=xmlPath)
        root = tree.getroot()
        for elements in root:
            if str(elements.attrib["FileName"])==l:
                root.remove(elements)
                tree.write(xmlPath)
                break
        
        self.refreshList()
    
    #Delete selected item from the Lighting List............................................
    def deleteLightItem(self):
        self._importedList  = self.getUI("lightList")
        selectedFile = cmds.textScrollList(self._importedList, q=True, si=True)
        s=selectedFile[0]
        
        import xml.etree.cElementTree as ET
        tree = ET.ElementTree(file=lightxmlPath)
        root = tree.getroot()
        for elements in root:
            if str(elements.attrib["FileName"])==s:
                root.remove(elements)
                tree.write(lightxmlPath)
                break
        
        self.refreshLightList()
    
   #ClearLog.................................................................................
    def clearLog(self):
        import xml.etree.cElementTree as ET
        tree = ET.ElementTree(file=lightxmlPath)
        root = tree.getroot()
        l=int(len(root))
        for x in range(0,l):
            del root[0]
            tree.write(lightxmlPath)
            tree.write(lightxmlPath)
        self.refreshLightList()
         
   #OpenFolderLocation........................................................................
    def openFolder(self):
        self.importedList  = self.getUI("animList")
        selectedItem = cmds.textScrollList(self.importedList, q=True, si=True)
        s=selectedItem[0]
        x=s.rfind("||")
        k=s[x+2:]
        l = k.strip()
        m=l.rfind("/")
        path=l[:m]
        os.startfile(path)
         
   #Add to Lighting List......................................................................
    def addToLight(self):
        
        self._importedList  = self.getUI("animList")
        self._importedList_Light  = self.getUI("lightList")
        selectedFile = cmds.textScrollList(self._importedList, q=True, selectItem=True)
        deleteFile = cmds.textScrollList(self._importedList, q=True, sii=True)
        
        tree = ET.ElementTree(file=lightxmlPath)
        file_list = tree.getroot()
        c=ET.Element('File')
        c.attrib['FileName'] = selectedFile[0]
        
        file_list.append(c)
        tree.write(lightxmlPath)
        cmds.textScrollList(self._importedList_Light, e=True,append=selectedFile)
        self.deleteAnimItem()
        self.refreshList()
        
        print selectedFile
   #To find the particular UI Item..............................................................
    def getUI(self,name):
        items = cmds.lsUI(dumpWidgets=True)
        for item in items:
            if self._windowName in item:
                self._objectList.append(item)
        for item in self._objectList:
            if item.endswith(name):
                return item
        print self._objectList
        
    #Add data to labels........................................................................
    def itemSelected(self):
        xFile = xd.parse(xmlPath)
        self.importedList  = self.getUI("animList")
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
        x=xmlElements[tmp].attributes["ImagePlane"].value
        cmds.text(self.getUI("imageplane_label"),e=True,l="ImagePlane = "+str(x))
        
    #Close the current UI.....................................................................   
    def close(self):
        """
        close()
            
            close an existing window
        """

        if cmds.window(self._windowName, q=True, exists=True):
            cmds.deleteUI(self._windowName)
    #Show the UI..............................................................................
    def showQueue(self):
        self.close()
        
    	win = cmds.loadUI(f = UI_FILE)
    	cmds.showWindow(win)