#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 11:53:12 2017

@author: fubao
"""

#get main conference and their topic;
#first focus on the data management conference here 

import glob


class getTopicCls:
   
    #abbreviation name --> to website
    conferenceWebsites = 
    
    
    def __init__(self):
      pass
    
    #read conference topic from file
    def readConfTopics(fileDir):
        filePaths = glob.glob(fileDir)
        print (filePaths)
        
    #write type and type Id 
    def writeTypeFile(self, outFile):
        x = 1
    

def main():
    
    getTopicClsObj = getTopicCls()
    
    filePaths = "/home/fubao/workDir/ResearchProjects/GraphQuerySearchRelatedPractice/Data/dblpParserGraph/input/conferenceTopicFile/"
    getTopicClsObj.readConfTopics()
    
    
    
    fd.close()
    
    
if __name__== "__main__":
  main()
