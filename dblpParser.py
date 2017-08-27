#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 23:52:30 2017

@author: fubao
"""

#function for parser dblp xml iterative.  
#do not to read all xml content into memory
import os
import pandas as pd
from blist import blist
from lxml import etree
from unidecode import unidecode

from commons import writeListRowToFileWriterTsv


mediaTypeToNameLstMap = {'www': 'url', 'phdthesis': 'school',  'inproceedings': 'booktitle',
                   'incollection': 'booktitle', 'proceedings':'booktitle', 'book': 'publisher',
                   'mastersthesis': 'school', 'article': 'journal'}              #media type --> its content, conference, journal etc

monthToDigitMap = {"january": "01", "february": "02", "march": "03", "april": "04", "may": "05", "june": "06",
            "july": "07", "august": "08", "september": "09", "october": "10", "november": "11", "december": "12"}

#node type for graph
class nodeType(object):
    peopleType = 1            #people type-- author
    paperType = 2             #paper title
    topicType = 3             #topic
    timeType = 4              #Time  month/year
    #affilType = 5             #author affiliation
    mediaTypesToIdMap = {list(mediaTypeToNameLstMap.keys())[j-1]:j+4 for j in range(1, len(mediaTypeToNameLstMap)+1)}   # mediatype to id
   

class parserDblpXmlCls:
    startNodeId = 1                      #graph node Id starting from 1
    graphNodeNameToIdMap  = {}            #store node name+type -> ID map
    gNodeIdToNameMap  = {}               #store node id -> name  map
    
    graNodeTypeMap = {}                 #node id to type
    edgeList = blist()                       #graph edge list  "nodeId, nodeId, edge"
    
    def __init__(self):
      pass
    
    
    #Parser dblp xml file
    def readParserXMl(self, context, fd):
        authors = blist()             
        title = ""                    
        mediaType = ""                
        mediaName = ""
        
        year = ""
        month = ""
        
        #parse the tags
        for event, elem in context:
            if elem.tag == 'author':
                authors.append(unidecode(elem.text).lower().strip())
                
            if elem.tag == 'title':
                if elem.text:
    	               title = unidecode(elem.text).lower().strip() 
            if elem.tag in mediaTypeToNameLstMap:
                if elem.text:
                    mediaType= unidecode(elem.tag).lower().strip()                 #specific conference, journal name
            
            if mediaType in mediaTypeToNameLstMap:
                mediaNameTag = mediaTypeToNameLstMap[mediaType]
                if elem.tag == mediaNameTag:
                    mediaName = unidecode(elem.text).lower().strip() 
            
            if elem.tag == "month":
                if elem.text:
                    month = unidecode(elem.text).lower().strip() 
            if elem.tag == "year":
                if elem.text:
                    year = unidecode(elem.text).lower().strip() 
            
            if elem.tag in mediaTypeToNameLstMap:
                #print ("media Name: ", mediaName, elem.tag)
                if len(authors) is not 0 and title is not '':
                    for a in authors:
                        # author <--> paper
                        nodeA = a + "+"+ str(nodeType.peopleType)
                        nodeTitle = title + "+"+ str(nodeType.paperType)
                        inList = [nodeA, nodeTitle, "same"]
                        writeListRowToFileWriterTsv(fd, inList, '\t')
                        inList = [nodeTitle, nodeA, "same"]
                        writeListRowToFileWriterTsv(fd, inList, '\t')
                         
                    #author <--> author 
                    for a1 in authors:
                        for a2 in authors:
                            if a1 != a2:
                                nodeA1 = a1 + "+"+ str(nodeType.peopleType)
                                nodeA2 = a2 + "+"+ str(nodeType.peopleType)
                                inList = [nodeA1, nodeA2, 'same']
                                writeListRowToFileWriterTsv(fd, inList, '\t')
                                inList = [nodeA2, nodeA1, 'same']
                                writeListRowToFileWriterTsv(fd, inList, '\t')
                    
                #paper title <--> mediaTypeName
                if len(mediaType) is not 0 and len(mediaName) is not 0 and title is not '':
                    nodeM = mediaName + "+"+ str(nodeType.mediaTypesToIdMap[mediaType])
                    nodeTitle = title + "+"+ str(nodeType.paperType)
                    inList = [nodeM, nodeTitle, 'higher']
                    writeListRowToFileWriterTsv(fd, inList, '\t')
                    inList = [nodeTitle, nodeM, 'lower']
                    writeListRowToFileWriterTsv(fd, inList, '\t')
                   
                    #delete and reinitiate
                    mediaName = ""
                    mediaType = ""
                    del authors[:]
                if len(year) is not 0 and title is not '':
                    month = monthToDigitMap[month] if month in monthToDigitMap else month
                    nodeTime = month + '/' + year + '+' + str(nodeType.timeType) 
                    nodeTitle = title + "+"+ str(nodeType.paperType)
                    inList = [nodeTime, nodeTitle, 'same']
                    writeListRowToFileWriterTsv(fd, inList, '\t')
                    inList = [nodeTitle, nodeTime, 'same']
                    writeListRowToFileWriterTsv(fd, inList, '\t')
             
            
            elem.clear()
        
        del context
    
    #print element in the file
    def printElementPair(self, elem, fout):
        print ("printing ... " + elem)
        print (fout, elem)
    
    #write node info ;  node name-type with nodeId
    def writeNodeInfoFile(self):
        x = 1
    
    #write type and type Id 
    def writeTypeFile(self):
        x = 1
    
    #write edge list fiel with node Id;  source \t dst node Id  \t edge property
    def writeEdgeListFileId(self):
        x = 1
    
def main():
    
    parseDblpXmlObj = parserDblpXmlCls()
    
    outEdgeListFile = "output/outEdgeListFile.tsv"
    os.remove(outEdgeListFile) if os.path.exists(outEdgeListFile) else None
    fd = open(outEdgeListFile, 'a')
    
    #context = etree.iterparse('../dblp/dblp-Part-Test.xml', load_dtd=True, html=True)
    context = etree.iterparse('../dblp12012016/dblpPart.xml', load_dtd=True, html=True)
    parseDblpXmlObj.readParserXMl(context, fd)
    
    
if __name__== "__main__":
  main()
  
