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


#combine the dblp graph node (from file) and the conference topic nodefrom list/set 
#Moreover, it gets the confe name in the outer extracted set from getTopic.py and change file name

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
        confTopicObj = confTopicClass()
        confTopicObj.executeMainFunction()        
        #read conf topic node name  into df
        dfConf = pd.DataFrame(list(confTopicClass.confNameSet), index=None, columns=None)
        
        #seNodeIds = pd.Series([]) #seNodeIds.values
        #get node Id for topic
        dfConf["nodeId"] = [i for i in range(graphNodeMaxNodeIdCurrent+1, len(dfConf)+graphNodeMaxNodeIdCurrent+1)] 
        print ("dfConf: ", dfConf.shape)
        dfConf.to_csv(newOutNodeNameToIdFile, mode='a', sep='\t', header=False, index=False)
        
        #read conf topic edge list into df
        dfConfEdge = pd.DataFrame(confTopicClass.conferenceNameToTopicEdgeLst, index=None, columns=None)
        
        print ("dfConfEdge: ", dfConfEdge)
        dfConfEdge.to_csv(newOutEdgeListFile, mode='a', sep='\t', header=False, index=False)
        
    #given node type in the outer conf, we get the nodeName and node Id
    def getConferenNameFromType(ingetTypeStr = 'article', oldGraphNodeNameSet, confNameSet):
        #get nodeType Id
        nodeTypeId = nodeTypeCls.mediaTypesToIdMap[ingetTypeStr]
        oldtypeNodeIdSet = set()
        for nodeNameType in oldGraphNodeNameSet:
            nodeTpId = int(nodeNameType.split('+')[1].strip())      #node type Id
            if nodeType == nodeTpId:
                oldtypeNodeIdSet.add(nodeNameType.lower())
        
        newconfNameSet = set()
        
        for nodeNameType in confNameSet:
            nodeName = nodeNameType.split('+')[0].lower().strip()
            nodeTypeId = nodeNameType.split('+')[1]
            for nodeNameTypeOld in oldtypeNodeIdSet:
                if nodeName in nodeNameOld:
                    #modify nodeName 
                    nodeNameType = nodeNameTypeOld
                    newconfNameSet.add(nodeNameType)
        return newconfNameSet
    
def main():
    
    graphCombNodesObj = graphCombNodesCls()
    oldNodeNameToIdFile = "../output/outNodeNameToIdFile.tsv" 
    oldEdgeListFile = "../output/outEdgeListFile.tsv"
    
    newOutNodeNameToIdFile = "../output/finalOutput/newOutNodeNameToIdFile.tsv"
    newOutEdgeListFile = "../output/finalOutput/newOutEdgeListFile.tsv"
    graphCombNodesObj.readEdgeListFile(oldNodeNameToIdFile, oldEdgeListFile, newOutNodeNameToIdFile, newOutEdgeListFile)
    
    
    
    
if __name__== "__main__":
  main()