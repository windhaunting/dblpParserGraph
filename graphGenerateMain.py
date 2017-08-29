#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 23:17:12 2017

@author: fubao
"""

import os
import pandas as pd
from blist import blist
import numpy as np
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
        dfOldNodeNameId = pd.read_csv(oldNodeNameToIdFile, delimiter = '\t') 
        dfOldNodeNameId.rename(columns={'Unnamed: 0':'node_name'}, inplace=True)

        graphNodeMaxNodeIdCurrent = len(dfOldNodeNameId)         #node number
        print ("graphNodeMaxNodeIdCurrent: ", graphNodeMaxNodeIdCurrent, dfOldNodeNameId.shape, dfOldNodeNameId.columns)
        #remove  newOutNodeNameToIdFile file first
        os.remove(newOutNodeNameToIdFile) if os.path.exists(newOutNodeNameToIdFile) else None
        #remove newOutEdgeListFile file first
        os.remove(newOutEdgeListFile) if os.path.exists(newOutEdgeListFile) else None

        #cp old into file into file first
        copyfile(oldNodeNameToIdFile, newOutNodeNameToIdFile)
        copyfile(oldEdgeListFile, newOutEdgeListFile)

        #get conference topic nodeName
        confTopicObj = confTopicClass()
        confTopicObj.executeMainFunction() 
        
        #read         

        #get from oldNodeNameToIdFile file
        oldGraphNodeNameSet = dfOldNodeNameId.ix[:,0]
        print ("oldGraphNodeNameSet: ", oldGraphNodeNameSet)
        diffconfNameSet, conferNameToOldMap = self.getConferenNameTopicFromType('article', oldGraphNodeNameSet, confTopicObj.confNameSet)
        #read conf topic node name  into df
        dfConf = pd.DataFrame(list(diffconfNameSet), index=None, columns= ["node_name"])
        
        #seNodeIds = pd.Series([]) #seNodeIds.values
        #get node Id for topic
        dfConf["node_id"] = [i for i in range(graphNodeMaxNodeIdCurrent+1, len(dfConf)+graphNodeMaxNodeIdCurrent+1)] 
        print ("dfConf: ", dfConf.shape)
        dfConf.to_csv(newOutNodeNameToIdFile, mode='a', sep='\t', header= None, index=False)
        
        #final nodeNameId df
        dfGraphNodeNameIdFinal = pd.concat([dfOldNodeNameId, dfConf],  ignore_index=True)
        #print ("dfGraphNodeNameIdFinal : ", dfGraphNodeNameIdFinal["node_id"])
        #read old edge list into df
        #dfOldEdgeList = pd.read_csv(oldEdgeListFile, delimiter = '\t')
        
        #write conf topic edge list into df
        
        #print ("bbbbbbbbbbbbbbbbbbbbbb: ",dfOldNodeNameId.shape, dfConf.shape, dfGraphNodeNameIdFinal.shape, dfGraphNodeNameIdFinal[dfGraphNodeNameIdFinal["node_name"] == "pvldb+++5"]["node_id"])

        dfConfEdge = pd.DataFrame(confTopicClass.conferenceNameToTopicEdgeLst, index=None, columns=["node_src_id", "node_dst_id", "edge_prop"])        
        
        dfConfEdge["node_src_id"] = dfConfEdge["node_src_id"].map(lambda x: self.format(x, dfGraphNodeNameIdFinal, conferNameToOldMap))
        dfConfEdge["node_dst_id"] = dfConfEdge["node_dst_id"].map(lambda x: self.format(x, dfGraphNodeNameIdFinal, conferNameToOldMap))
        
        #print ("len(oldEdgeListFile): ", len(oldEdgeListFile), dfConfEdge["node_src_id"], dfConfEdge["node_dst_id"])
        
        dfConfEdge.to_csv(newOutEdgeListFile, mode='a', sep='\t', header=False, index=False)
    
    def format(self, x, dfGraphNodeNameIdFinal, conferNameToOldMap):
        if len(dfGraphNodeNameIdFinal[dfGraphNodeNameIdFinal["node_name"] == x]["node_id"].values) != 0:
            return int(dfGraphNodeNameIdFinal[dfGraphNodeNameIdFinal["node_name"] == x]["node_id"].values[0])
        else:
            if np.isnan(dfGraphNodeNameIdFinal[dfGraphNodeNameIdFinal["node_name"] == conferNameToOldMap[x]]["node_id"].values):
                return -1
            else:
                return int(dfGraphNodeNameIdFinal[dfGraphNodeNameIdFinal["node_name"] == conferNameToOldMap[x]]["node_id"].values[0])
        
    #given node type in the outer conf, we get the new nodeName without previous
    def getConferenNameTopicFromType(self, ingetTypeStr, oldGraphNodeNameSet, confNameSet):
        #get nodeType Id
        nodeTypeId = nodeTypeCls.mediaTypesToIdMap[ingetTypeStr]
        oldtypeNodeIdSet = set()
        for nodeNameType in oldGraphNodeNameSet:
            nodeTpId = int(nodeNameType.split('+++')[1].strip())      #node type Id
            if nodeTypeId == nodeTpId:
                oldtypeNodeIdSet.add(nodeNameType.lower())
        
        newconfNameSet = set()
        
        conferNameToOldMap = {}                #conference type extracted name map to dblp conference name
        for nodeNameType in confNameSet:
            nodeName = nodeNameType.split('+++')[0].lower().strip()
            nodeTypeId = nodeNameType.split('+++')[1]
            for nodeNameTypeOld in oldtypeNodeIdSet:
                if nodeName in nodeNameTypeOld and nodeTypeId == nodeNameTypeOld.split('+++')[1]:                 #get common nodes for joining               
                    #modify nodeName 
                    #nodeNameType = nodeNameTypeOld
                    newconfNameSet.add(nodeNameType)
                    conferNameToOldMap[nodeNameType] = nodeNameTypeOld
                    break
        diffconfNameSet = confNameSet - newconfNameSet
        
        if "database+++3" in confNameSet:
            print ("Yessssssssssssssssssssssssssss")
        if "vldb+++5" in conferNameToOldMap:
            print ("aYesaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", conferNameToOldMap["vldb+++5"])    
        return diffconfNameSet, conferNameToOldMap     #delete duplicates nodenametype
    
    
def main():
    
    graphCombNodesObj = graphCombNodesCls()
    oldNodeNameToIdFile = "../output/outNodeNameToIdFile.tsv" 
    oldEdgeListFile = "../output/outEdgeListFile.tsv"
    
    newOutNodeNameToIdFile = "../output/finalOutput/newOutNodeNameToIdFile.tsv"
    newOutEdgeListFile = "../output/finalOutput/newOutEdgeListFile.tsv"
    graphCombNodesObj.readEdgeListFile(oldNodeNameToIdFile, oldEdgeListFile, newOutNodeNameToIdFile, newOutEdgeListFile)
    
    
    
    
if __name__== "__main__":
  main()