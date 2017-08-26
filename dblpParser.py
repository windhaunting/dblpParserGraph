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


class nodeType:
    peopleType = 1
    topicType = 2             #topic
    PaperType = 3             #paper title
    venueType = 4             #venue
    TimeType = 5              #Time  month/year
    Type = 6
    
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
        collaborations = [u'www', u'phdthesis', u'inproceedings', u'incollection', u'proceedings', u'book', u'mastersthesis', u'article']
        authors = blist()
        title = ""
        venueString = 'url'            #  [u'note', u'journal', u'publisher', u'url']
        for event, elem in context:
            if elem.tag == 'author':
                authors.append(unidecode(elem.text))
            if elem.tag == 'title':
                if elem.text:
    	               title = unidecode(elem.text)  
            if elem.tag in collaborations:
                if len(authors) is not 0 and title is not '':
                    for a in authors:
                        # author <--> paper
                        inList = [a, title, "same"]
                        writeListRowToFileWriterTsv(fd, inList, '\t')
                        inList = [title, a, "same"]
                        writeListRowToFileWriterTsv(fd, inList, '\t')
                         
                    #author <--> author 
                    for a1 in authors:
                        for a2 in authors:
                            if a1 != a2:
                                inList = [a1, a2, 'same']
                                writeListRowToFileWriterTsv(fd, inList, '\t')
                                inList = [a2, a1, 'same']
                                writeListRowToFileWriterTsv(fd, inList, '\t')
                                
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
  
