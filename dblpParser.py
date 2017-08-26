#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 23:52:30 2017

@author: fubao
"""

#function for parser dblp xml iterative.  
#do not to read all xml content into memory
import os
import numpy as np
import pandas as pd
from blist import blist
from lxml import etree
from unidecode import unidecode

from commons import writeListRowToFileWriterTsv


#mediaTypeLst = ['www', 'phdthesis', 'inproceedings', 'incollection', 'proceedings', 'book', 'mastersthesis', 'article']
mediaTypeToNameLstMap = {'www': 'url', 'phdthesis': 'school',  'inproceedings': 'booktitle',
                   'incollection': 'booktitle', 'proceedings':'booktitle', 'book': 'publisher',
                   'mastersthesis': 'school', 'article': 'journal'}              #media type --> its content, conference, journal etc
#node type for graph

class nodeType(object):
    peopleType = 1            #people type-- author
    paperType = 2             #paper title
    topicType = 3             #topic
    #venueType = 4             #venue
    timeType = 4              #Time  month/year
    affilType = 5             #author affiliation
    mediaTypesToIdMap = {mediaTypeToNameLstMap[j-1]:j+5 for j in range(1, len(mediaTypeToNameLstMap)+1)}   # mediatype to id
   

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
        mediaTypeName = ""
        #mediaTypeTags =  [u'booktitle', u'journal', u'publisher', ]
        for event, elem in context:
            if elem.tag == 'author':
                authors.append(unidecode(elem.text).lower().strip())
            if elem.tag == 'title':
                if elem.text:
    	               title = unidecode(elem.text).lower().strip() 
            if elem.tag in mediaTypeLstMap:
                if elem.text:
                    mediaType= unidecode(elem.tage).lower().strip()                 #specific conference, journal name
            
            if mediaTypesToIdMap()
            if elem.tag in mediaTypeToNameLstMap:
                print ("media TypeName: ", mediaTypeName, elem.tag)
                if len(authors) is not 0 and title is not '':
                    for a in authors:
                        # author <--> paper
                        nodeA = a + "("+ str(nodeType.peopleType) + ")"
                        nodeTitle = title + "("+ str(nodeType.paperType) + ")"
                        inList = [nodeA, nodeTitle, "same"]
                        writeListRowToFileWriterTsv(fd, inList, '\t')
                        inList = [nodeTitle, nodeA, "same"]
                        writeListRowToFileWriterTsv(fd, inList, '\t')
                         
                    #author <--> author 
                    for a1 in authors:
                        for a2 in authors:
                            if a1 != a2:
                                nodeA1 = a1 + "("+ str(nodeType.peopleType) + ")"
                                nodeA2 = a2 + "("+ str(nodeType.peopleType) + ")"
                                inList = [nodeA1, nodeA2, 'same']
                                writeListRowToFileWriterTsv(fd, inList, '\t')
                                inList = [nodeA2, nodeA1, 'same']
                                writeListRowToFileWriterTsv(fd, inList, '\t')
                    
                #paper title --> mediaTypeName
                if len(mediaTypeName) is not 0 and title is not '':
                    nodeM = mediaTypeName + "("+ str(nodeType.mediaTypesToIdMap[mediaTypeName]) + ")"
                    nodeTitle = title + "("+ str(nodeType.paperType) + ")"
                    inList = [nodeM, nodeTitle, 'higher']
                    writeListRowToFileWriterTsv(fd, inList, '\t')
                    inList = [nodeTitle, nodeM, 'lower']
                    writeListRowToFileWriterTsv(fd, inList, '\t')
                    
                    title = ''
                    mediaTypeName = ""
                    del authors[:]
            elem.clear()
        
        del context        

    def writeElementPair(self, elem, fout):
        print ("writing ... " + elem)
        print (fout, elem)
    

def main():
    
    parseDblpXmlObj = parserDblpXmlCls()
    
    outEdgeListFile = "output/outEdgeListFile.tsv"
    os.remove(outEdgeListFile) if os.path.exists(outEdgeListFile) else None
    fd = open(outEdgeListFile, 'a')
    
    context = etree.iterparse('../dblp/dblp-Part-Test.xml', load_dtd=True, html=True)
    parseDblpXmlObj.readParserXMl(context, fd)
    
    
if __name__== "__main__":
  main()
  
