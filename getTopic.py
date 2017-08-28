#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 11:53:12 2017

@author: fubao
"""

#get main conference and their topic;
#first focus on the data management conference here 

from os import listdir
from os.path import join
import pandas as pd

from dblpParser import nodeTypeCls
class confTopicClass(object):
   
    #abbreviation name --> to topic edge list
    conferenceNameToTopicEdgeLst = []
    confNameSet = set()
    
    def __init__(self):
      pass
    
    #read conference topic from file
    def readConfTopics(self, fileDir):
        dirs = listdir(fileDir)
        for file in dirs:
            filePath = join(fileDir, file)
            #print ("filePath: ", filePath)
            self.readEachConfTopicFile(filePath)
        
        print ("len readEachTopicFile: ", len(confTopicClass.conferenceNameToTopicEdgeLst))
        print ("nodeTypeCls.mediaTypesToIdMap: ", nodeTypeCls.commonTypeToIdMap, nodeTypeCls.mediaTypesToIdMap)
        

    #read every stored topic file
    def readEachConfTopicFile(self, fileIn):
        df = pd.read_csv(fileIn, delimiter = '\t')
        #print (df.columns[0])
       #print (df.values)
        abbreName = df.columns[0].split('-')[0].lower().strip()
        nodeAbbreName = abbreName + "+++" + str(nodeTypeCls.mediaTypesToIdMap["article"])    #conference but in the journal tag
        if nodeAbbreName not in confTopicClass.confNameSet:
            confTopicClass.confNameSet.add(nodeAbbreName)
        for val in df.values:
            #print ("val: ", val)
            nodeTopic = val[0].lower().strip() + "+++" + str(nodeTypeCls.commonTypeToIdMap["topic"])
            edgeProp = "same"
            confTopicClass.conferenceNameToTopicEdgeLst.append([nodeAbbreName, nodeTopic, edgeProp])
            confTopicClass.conferenceNameToTopicEdgeLst.append([nodeTopic, nodeAbbreName, edgeProp])
        
            if nodeTopic not in confTopicClass.confNameSet:
                confTopicClass.confNameSet.add(nodeTopic)
        
    #main function execute
    def executeMainFunction(self):
        filePaths = "/home/fubao/workDir/ResearchProjects/GraphQuerySearchRelatedPractice/Data/dblpParserGraph/input/conferenceTopicFile/"
        self.readConfTopics(filePaths)
        
def main():
    confTopicObj = confTopicClass()
    confTopicObj.executeMainFunction()
    
    
if __name__== "__main__":
  main()
