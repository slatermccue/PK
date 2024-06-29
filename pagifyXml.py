import os
import sys
import zipfile
import lxml.etree as ET

#usage: pagifyXml.py inputSlideDB.xml
#requires: CS-Blank.odp (pick from safeCopy folder)

#Program outline:
#This program will read from the temp xlm file and append
#each page found in it to the CS-Blank.odp slide deck
#The first page of the CS-Blank slide deck will be left alone,
# which means the appended pages will start with 'page2' and increase
# from there.

#open the temp page xml file indicated as argument to program
#note: the file may contain multiple slides, each of which needs to
# have its page number modified in two locations
input_file_path = sys.argv[1]
with open(input_file_path)) as newSlide:
    newSlideXml = newSlide.read()

slideParser = ET.XMLParser(remove_blank_text=True)
slideRoot = ET.fromstring(newSlideXml, parser=slideParser)