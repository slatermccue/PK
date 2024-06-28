#!/usr/bin/env python3
# 
# SYNOPSIS: stripgif.py input.odp output.odp
# temp usage: workOnODP.py input.odp
'''
found at:
    <script src="https://gist.github.com/JohannesBuchner/c7ba8f97c6b204cc656a94109f9750eb.js"></script>
'''
# 
# 

import os
import sys
import zipfile
import lxml.etree as ET

# specify the input and output file paths
input_file_path = sys.argv[1]
output_file_path = sys.argv[2]

zin = zipfile.ZipFile(input_file_path, 'r')
zout = zipfile.ZipFile(output_file_path, 'w')
for item in zin.infolist():
    buf = zin.read(item.filename)
    if item.filename != 'content.xml':
        zout.writestr(item, buf)
zout.close()
zin.close()

# open the input ZIP file and extract the XML file
with zipfile.ZipFile(input_file_path, 'r') as input_zip:
    with input_zip.open('content.xml') as xml_file:
        xml_data = xml_file.read()

# define the namespace prefix mapping
nsmap = {
    'draw': 'urn:oasis:names:tc:opendocument:xmlns:drawing:1.0',
    'pres': 'urn:oasis:names:tc:opendocument:xmlns:presentation:1.0',
    'xlink': 'http://www.w3.org/1999/xlink'
}

# parse the XML tree from the input file
parser = ET.XMLParser(remove_blank_text=True)
root = ET.fromstring(xml_data, parser=parser)

#The following was found at:
#https://docs.oasis-open.org/office/v1.2/
#                 cs01/OpenDocument-v1.2-cs01-part1.html
#
# <office:presentation> is the main tag found in <office:body>
#
#The <office:presentation> element has the following child elements: 
#
#<draw:page> 10.2.4, 
#<presentation:date-time-decl> 10.9.3.6, 
#<presentation:footer-decl> 10.9.3.4, 
#<presentation:header-decl> 10.9.3.2, 
#<presentation:settings> 10.9.3.7, 
#<table:calculation-settings> 9.4.1, 
#<table:consolidation> 9.7, 
#<table:content-validations> 9.4.4, 
#<table:database-ranges> 9.4.14, 
#<table:data-pilot-tables> 9.6.2, 
#<table:dde-links> 9.8, 
#<table:label-ranges> 9.4.10, 
#<table:named-expressions> 9.4.11, 
#<text:alphabetical-index-auto-mark-file> 8.8.3, 
#<text:dde-connection-decls> 14.6.2, 
#<text:sequence-decls> 7.4.11, 
#<text:user-field-decls> 7.4.7, 
#<text:variable-decls> 7.4.2

#print(root.xpath("//*[name()='draw:page']"))
found = False

with open('tempXmlData.xml') as newSlide:
    newSlideXml = newSlide.read()

#need to extract the single page from this xml
slideParser = ET.XMLParser(remove_blank_text=True)
slideRoot = ET.fromstring(newSlideXml, parser=slideParser)
thisSlideXml = root.xpath('//draw:page', namespaces=nsmap)
print(slideRoot)


for slide in root.xpath('//draw:page', namespaces=nsmap):
    #print(slide.tag, slide.attrib, slide.attrib.items())
    print(slide.tag)
    for char in slide.attrib.items():
        print('|-->', char)
        if (char[1] == 'page5'):
            slide.getparent().append(slideRoot)
        #if (char[1] == 'page3'):
        #    tempXmlDataSlide = ET.tostring(slide, pretty_print=True, xml_declaration=True, encoding='UTF-8')
        #    with open('tempXmlData.xml', 'wb') as xml_file:
        #        xml_file.write(tempXmlDataSlide)
    print("===========")

# write the modified XML tree to a new file
modified_xml_data = ET.tostring(root, xml_declaration=True, encoding='UTF-8')
with open('modified_content.xml', 'wb') as xml_file:
    xml_file.write(modified_xml_data)

# create a new ZIP file and add the modified XML file to it
with zipfile.ZipFile(output_file_path, 'a') as output_zip:
    output_zip.write('modified_content.xml', 'content.xml')

# delete the temporary XML file
os.remove('modified_content.xml')
