#!/usr/bin/env python3
# 
# SYNOPSIS: stripgif.py input.odp output.odp
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
	if item.filename != 'content.xml' and not item.filename.endswith('.mp4') and not item.filename.endswith('.gif'):
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
    'xlink': 'http://www.w3.org/1999/xlink'
}
# parse the XML tree from the input file
parser = ET.XMLParser(remove_blank_text=True)
root = ET.fromstring(xml_data, parser=parser)

# find all the animated gif elements and remove them
for gif in root.xpath(".//draw:image[contains(@xlink:href, '.gif')]", namespaces=nsmap):
    gif.getparent().remove(gif)
for gif in root.xpath(".//draw:image[contains(@xlink:href, '.mp4')]", namespaces=nsmap):
    gif.getparent().remove(gif)

# write the modified XML tree to a new file
modified_xml_data = ET.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8')
with open('modified_content.xml', 'wb') as xml_file:
    xml_file.write(modified_xml_data)

# create a new ZIP file and add the modified XML file to it
with zipfile.ZipFile(output_file_path, 'a') as output_zip:
    output_zip.write('modified_content.xml', 'content.xml')

# delete the temporary XML file
os.remove('modified_content.xml')
