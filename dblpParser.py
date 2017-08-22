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

class nodeType:
    peopleType = 1
    topicType = 2             #topic
    titleType = 3             #title
    venueType = 4             #venue
    PaperType = 5             #paper
    TimeType = 6
    
class parserDblpXml:
    startNodeId = 1                      #graph node Id starting from 1
    graphNodeNameToIdMap  = {}            #store node name+type -> ID map
    gNodeIdToNameMap  = {}               #store node id -> name  map
    
    graNodeTypeMap = {}                 #node id to type
    edgeList = blist()                       #graph edge list  "nodeId, nodeId, edge"
    
    def __init__(self):
      pass
     
        
    def readParserXMl():
        collaborations = [u'www', u'phdthesis', u'inproceedings', u'incollection', u'proceedings', u'book', u'mastersthesis', u'article']
        