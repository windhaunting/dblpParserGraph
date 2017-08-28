#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 23:17:12 2017

@author: fubao
"""

import os
import pandas as pd
from blist import blist

from commons import writeListRowToFileWriterTsv
from dblpParser import nodeTypeCls
from getTopic import confTopicClass
from shutil import copyfile


#join and combine the dblp graph node (from file) and the conference topic nodefrom list/set 
class graphCombNodesCls(object):
    startNodeId = 1                      #graph node Id starting from 1
    graphNodeNameToIdMap  = {}           #store node name+type -> ID map
    gNodeIdToNameMap  = {}               #store node id -> name  map
    
    graNodeTypeMap = {}                 #node id to type
    edgeList = blist()                       #graph edge list  "nodeId, nodeId, edge"
    
    
    def __init__(self):
      pass
    
        #write type and type Id 
    def readEdgeListFile(self, oldNodeNameToIdFile, oldEdgeListFile, newOutNodeNameToIdFile, newOutEdgeListFile):
        df = pd.read_csv(oldNodeNameToIdFile, delimiter = '\t')
        
        graphNodeMaxNodeIdCurrent = len(df)         #node number
        print ("graphNodeMaxNodeIdCurrent: ", graphNodeMaxNodeIdCurrent)
                
        #remove file first
        os.remove(newOutNodeNameToIdFile) if os.path.exists(newOutNodeNameToIdFile) else None

        #cp old into file into file first
        copyfile(oldNodeNameToIdFile, newOutNodeNameToIdFile)
        copyfile(oldEdgeListFile, newOutEdgeListFile)

        #get conference topic nodeName
        confTopicClass.executeMainFunction()
        #for row in df.itertuples():
        #    nodeName = row[0]
        #    nodeId = row[1]
        #    graphNodeNameToIdMap


def main():
    
    graphCombNodesObj = graphCombNodesCls()
    oldNodeNameToIdFile = "../output/outNodeNameToIdFile.tsv" 
    oldEdgeListFile = "../output/outEdgeListFile.tsv"
    
    newOutNodeNameToIdFile = "../output/finalOutput/newOutNodeNameToIdFile.tsv"
    newOutEdgeListFile = "../output/finalOutput/newOutEdgeListFile.tsv"
    graphCombNodesObj.readEdgeListFile(oldNodeNameToIdFile, oldEdgeListFile, newOutNodeNameToIdFile, newOutEdgeListFile)
    
    
    
    
if __name__== "__main__":
  main()