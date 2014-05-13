import xml.dom.minidom as xd
path = "E:\PythonStuff\RenderQueue\queue.xml"
xFile = xd.parse(path)
xmlElements = xFile.getElementsByTagName("File")
x=xmlElements[0].attributes["FilePath"].value
print x