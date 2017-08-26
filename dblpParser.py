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


mediaTypeLst = [u'www', u'phdthesis', u'inproceedings', u'incollection', u'proceedings', u'book', u'mastersthesis', u'article']


class nodeType:
    peopleType = 1
    PaperType = 3             #paper title
    topicType = 3             #topic
    #venueType = 4             #venue
    TimeType = 4              #Time  month/year
    affilType = 5             #author affiliation
    mediaTypes = {mediaTypeLst[j-1] : j+TimeType for j in range(1, len(mediaTypeLst)+1)}
   

class parserDblpXmlCls:
    startNodeId = 1                      #graph node Id starting from 1
    graphNodeNameToIdMap  = {}            #store node name+type -> ID map
    gNodeIdToNameMap  = {}               #store node id -> name  map
    
    graNodeTypeMap = {}                 #node id to type
    edgeList = blist()                       #graph edge list  "nodeId, nodeId, edge"
    
    def __init__(self):
      pass
    
    
    #Parser xml    
    def readParserXMl(self, context, fd):
        authors = blist()
        title = ""
        mediaTypeTags =  [u'booktitle', u'journal', u'publisher', ]
        for event, elem in context:
            if elem.tag == 'author':
                authors.append(unidecode(elem.text))
            if elem.tag == 'title':
                if elem.text:
    	               title = unidecode(elem.text) 
            if elem.tags in mediaTypeTags:
                if elem.text:
                    mediaTypeName = unidecode(elem.text)                 #specific conference, journal name
            if elem.tag in mediaTypeLst:
                if len(authors) is not 0 and title is not '':
                    for a in authors:
                        # author <--> paper
                        nodeA = a + "("+ str(nodeType.peopleType) + ")"
                        nodeTitle = title + "("+ str(nodeType.PaperType) + ")"
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
                    if ele.tag in mediaTypeNames:
                        
                    title = ''
                    del authors[:]
            elem.clear()
        
        del context        

    def writeElementPair(self, elem, fout):
        print ("writing ... " + elem)
        print (fout, elem)
    

def main():
    
    parseDblpXmlObj = parserDblpXmlCls()
    
    outEdgeListFile = "output/outEdgeListFile.tsv"
    fd = open(outEdgeListFile, 'w')

    context = etree.iterparse('../dblp/dblp-Part-Test.xml', load_dtd=True, html=True)
    parseDblpXmlObj.readParserXMl(context, fd)
    
    
if __name__== "__main__":
  main()
  
