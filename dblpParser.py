#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 23:52:30 2017

@author: fubao
"""

#function for parser dblp xml
import os
import numpy as np
import pandas as pd
from blist import blist
from lxml import etree
from unidecode import unidecode

class nodeType:
    peopleType = 1
    topicType = 2             #topic
    titleType = 3             #title
    venueType = 4             #venue
    PaperType = 5             #paper
    TimeType = 6
    
class parserDblpXmlCls:
    startNodeId = 1                      #graph node Id starting from 1
    graphNodeNameToIdMap  = {}            #store node name+type -> ID map
    gNodeIdToNameMap  = {}               #store node id -> name  map
    
    graNodeTypeMap = {}                 #node id to type
    edgeList = blist()                       #graph edge list  "nodeId, nodeId, edge"
    
    def __init__(self):
      pass
     
        
    def readParserXMl(context):
        collaborations = [u'www', u'phdthesis', u'inproceedings', u'incollection', u'proceedings', u'book', u'mastersthesis', u'article']
        author_array = blist()
        title = ""
        venues = [u'note', u'journal', u'publisher', u'url']
        for event, elem in context:
            if elem.tag == 'author':
                author_array.append(unidecode(elem.text))
            if elem.tag == 'title':
                if elem.text:
    	               title = unidecode(elem.text)  
        if elem.tag in collaborations:
            if len(author_array) is not 0 and title is not '':
                func(a+"||"+title, *args, **kwargs)
                
def main():
    
    parseDblpXmlObj = parserDblpXmlCls()
    
if __name__== "__main__":
  main()
  