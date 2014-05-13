from xml.dom.minidom import Document

doc=Document()
root_node = doc.createElement("file_list")
doc.appendChild(root_node)


fileNode = doc.createElement("File")
root_node.appendChild(fileNode)


today = str(cmds.date(t=True))
playblastFlag = "Yes"
imagePlaneFlag = "No"
fileFrames = 65
fileName=cmds.file(shn=True,sn=True,q=True)
filePath=cmds.file(sn=True,q=True)
fileNode.setAttribute("FileName",fileName)
fileNode.setAttribute("FilePath",filePath)
fileNode.setAttribute("Frames",fileFrames)
fileNode.setAttribute("Time",today)
fileNode.setAttribute("PlayBlast",playblastFlag)
fileNode.setAttribute("ImagePlane",imagePlaneFlag)

xml_file = open("E:\PythonStuff\RenderQueue\queue.xml","w")
xml_file.write(doc.toprettyxml())
xml_file.close()
print doc.toprettyxml()