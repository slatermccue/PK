import os
import sys
import zipfile
import lxml.etree as ET

#usage: python pagifyXml.py tempXmlData.xml noWayItWillWorkNow.odp
#requires: CS-Blank.odp (pick from safeCopy folder)

#Program outline:
#This program will read from the temp xml file and append
#each page found in it to the CS-Blank.odp slide deck
#The first page of the CS-Blank slide deck will be left alone,
# which means the appended pages will start with 'page2' and increase
# from there.

#we don't need the xpath and namespaces since the xml is just the one element
def updatePageName(inputXml, newNum):
    pageNum = 'page' + str(newNum)
    inputXml.attrib['{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}name'] = pageNum
    stringRoot = ET.tostring(inputXml, encoding="unicode", pretty_print=True)
    noteLoc = stringRoot.find("page-number=\"")
    firstStr = stringRoot[:noteLoc+13]
    secondStr = stringRoot[noteLoc+13:]
    numLoc = secondStr.find("\"")
    secondStr = secondStr[numLoc:]
    outputStr = firstStr + str(newNum) + secondStr
    outputStr = ET.fromstring(stringRoot)
    return outputStr


#open the temp page xml file indicated as argument to program
#note: the input will eventually be a data stream such as a database query result
#for now, it is the first command line argument, tempXmlData.xml
input_file_path = sys.argv[1]
with open(input_file_path) as newSlide:
    newSlideXml = newSlide.read()

# specify the output file path

output_file_path = sys.argv[2]

zin = zipfile.ZipFile('CS-Blank.odp', 'r')
zout = zipfile.ZipFile(output_file_path, 'w')
for item in zin.infolist():
    buf = zin.read(item.filename)
    if item.filename != 'content.xml':
        zout.writestr(item, buf)
zout.close()
zin.close()

# open the input ZIP file and extract the XML file
with zipfile.ZipFile('CS-Blank.odp', 'r') as input_zip:
    with input_zip.open('content.xml') as xml_file:
        xml_data = xml_file.read()

# define the namespace prefix mapping
nsmap = {
    'draw': 'urn:oasis:names:tc:opendocument:xmlns:drawing:1.0',
    'pres': 'urn:oasis:names:tc:opendocument:xmlns:presentation:1.0',
    'xlink': 'http://www.w3.org/1999/xlink'
}



slideParser = ET.XMLParser(remove_blank_text=True)
masterRoot = ET.fromstring(xml_data, parser=slideParser)



#the following retrieves the xml slide to be added, modifies
#the page number and thumbnail number, then appends
#to the CS-Blank presentation
#
#while testing, we are attempting to add 5 identical slides to CS-Blank
#
for pageNum in list(range(2,7)):
    #we will change the newSlideXml later; for now, it is always the same
    slideRoot = ET.fromstring(newSlideXml, parser=slideParser)
    updatedRoot = updatePageName(slideRoot,pageNum)
    for slide in masterRoot.xpath('//draw:page', namespaces=nsmap):
        slide.getparent().append(updatedRoot)

modified_xml_data = ET.tostring(masterRoot, xml_declaration=True, encoding='UTF-8')
with open('modified_content.xml', 'wb') as xml_file:
    xml_file.write(modified_xml_data)

# create a new ZIP file and add the modified XML file to it
with zipfile.ZipFile(output_file_path, 'a') as output_zip:
    output_zip.write('modified_content.xml', 'content.xml')


# delete the temporary XML file
os.remove('modified_content.xml')
#print(updatedRoot)