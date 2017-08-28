#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 11:53:12 2017

@author: fubao
"""

#get main conference and their topic;
#first focus on the data management conference here 

from os import listdir
from os.path import isfile, join
import pandas as pd

class confTopicClass(object):
   
    #abbreviation name --> to topic edge list
    conferenceWebsites = {}
    
    
    def __init__(self):
      pass
    
    #read conference topic from file
    def readConfTopics(self, fileDir):
        dirs = listdir(fileDir)
        for file in dirs:
            filePath = join(fileDir, file)
            #print ("filePath: ", filePath)
            self.readEachTopicFile(filePath)
        
    def readEachTopicFile(self, fileIn):
        df = pd.read_csv(fileIn, delimiter = '\t')
        print (df.columns[0])
       #print (df.values)
        
        for val in df.values:
            x = 1

    #write type and type Id 
    def writeTypeFile(self, outFile):
        x = 1
    

def main():
    
    confTopicObj = confTopicClass()
    
    filePaths = "/home/fubao/workDir/ResearchProjects/GraphQuerySearchRelatedPractice/Data/dblpParserGraph/input/conferenceTopicFile/"
    confTopicObj.readConfTopics(filePaths)
    
    

    
    
if __name__== "__main__":
  main()
