#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 23:52:30 2017

@author: fubao
"""

#function for parser dblp xml iterative.  
#do not to read all xml content into memory
import os
import pandas as pd
from blist import blist
from lxml import etree
from unidecode import unidecode

from commons import writeListRowToFileWriterTsv


mediaTypeToNameLstMap = {'www': 'url', 'phdthesis': 'school',  'inproceedings': 'booktitle',
                   'incollection': 'booktitle', 'proceedings':'booktitle', 'book': 'publisher',
                   'mastersthesis': 'school', 'article': 'journal'}              #media type --> its content, conference, journal etc

monthToDigitMap = {"january": "01", "february": "02", "march": "03", "april": "04", "may": "05", "june": "06",
            "july": "07", "august": "08", "september": "09", "october": "10", "november": "11", "december": "12"}

#node type for graph
class nodeTypeCls(object):
   
    commonTypeToIdMap = {"people": 1, "paper": 2, "topic": 3, "time": 4}      # affilType = 5  #author affiliation
    mediaTypesToIdMap = {sorted(list(mediaTypeToNameLstMap.keys()))[j-1]:j+4 for j in range(1, len(mediaTypeToNameLstMap)+1)}   # mediatype to id
   

class parserDblpXmlCls:
    startNodeId = 1                      #graph node Id starting from 1
    graphNodeNameToIdMap  = {}           #store node name+type -> ID map
    gNodeIdToNameMap  = {}               #store node id -> name  map
    
    graNodeTypeMap = {}                 #node id to type
    edgeList = blist()                       #graph edge list  "nodeId, nodeId, edge"
    
    
    def __init__(self):
      pass
    
    
    #Parser dblp xml file
    def readParserXMl(self, context):
        authors = blist()             
        title = ""                    
        mediaType = ""                
        mediaName = ""
        
        year = ""
        month = ""
        
        #parse the tags
        for event, elem in context:
            if elem.tag == 'author':
                authors.append(unidecode(elem.text).lower().strip())
                
            if elem.tag == 'title':
                if elem.text:
    	               title = unidecode(elem.text).lower().strip() 
            if elem.tag in mediaTypeToNameLstMap:
                if elem.tag:
                    mediaType= unidecode(elem.tag).lower().strip()                 #specific conference, journal name
            
            if mediaType in mediaTypeToNameLstMap:
                mediaNameTag = mediaTypeToNameLstMap[mediaType]
                if elem.tag == mediaNameTag:
                    mediaName = unidecode(elem.text).lower().strip() 
            
            if elem.tag == "month":
                if elem.text:
                    month = unidecode(elem.text).lower().strip() 
            if elem.tag == "year":
                if elem.text:
                    year = unidecode(elem.text).lower().strip() 
            
            if elem.tag in mediaTypeToNameLstMap:
                #print ("media Name: ", mediaName, elem.tag)
                
                if len(authors) is not 0 and title is not '':
                    #get relations of author <--> paper
                    for a in authors:
                        # author <--> paper
                        nodeA = a + "+++"+ str(nodeTypeCls.commonTypeToIdMap["people"])
                        nodeTitle = title + "+++"+ str(nodeTypeCls.commonTypeToIdMap["paper"])
                        
                        if nodeA not in parserDblpXmlCls.graphNodeNameToIdMap:
                            parserDblpXmlCls.graphNodeNameToIdMap[nodeA] = parserDblpXmlCls.startNodeId
                            parserDblpXmlCls.startNodeId += 1
                        if nodeTitle not in parserDblpXmlCls.graphNodeNameToIdMap:
                            parserDblpXmlCls.graphNodeNameToIdMap[nodeTitle] = parserDblpXmlCls.startNodeId
                            parserDblpXmlCls.startNodeId += 1
                        
                        edgeProp = 'same'             #same level of hierarchical relation
                        parserDblpXmlCls.edgeList.append([parserDblpXmlCls.graphNodeNameToIdMap[nodeA], parserDblpXmlCls.graphNodeNameToIdMap[nodeTitle], edgeProp])
                        parserDblpXmlCls.edgeList.append([parserDblpXmlCls.graphNodeNameToIdMap[nodeTitle], parserDblpXmlCls.graphNodeNameToIdMap[nodeA], edgeProp])
                    
                    #get cooperation relations of author <--> author 
                    for a1 in authors:
                        for a2 in authors:
                            if a1 != a2:
                                nodeA1 = a1 + "+++"+ str(nodeTypeCls.commonTypeToIdMap["people"])
                                nodeA2 = a2 + "+++"+ str(nodeTypeCls.commonTypeToIdMap["people"])
                                                       
                                if nodeA1 not in parserDblpXmlCls.graphNodeNameToIdMap:
                                    parserDblpXmlCls.graphNodeNameToIdMap[nodeA1] = parserDblpXmlCls.startNodeId
                                    parserDblpXmlCls.startNodeId += 1
                                if nodeA2 not in parserDblpXmlCls.graphNodeNameToIdMap:
                                    parserDblpXmlCls.graphNodeNameToIdMap[nodeA2] = parserDblpXmlCls.startNodeId
                                    parserDblpXmlCls.startNodeId += 1
                        
                                edgeProp = 'same'             #lower hierarchical relation
                                parserDblpXmlCls.edgeList.append([parserDblpXmlCls.graphNodeNameToIdMap[nodeA1], parserDblpXmlCls.graphNodeNameToIdMap[nodeA2], edgeProp])
                                parserDblpXmlCls.edgeList.append([parserDblpXmlCls.graphNodeNameToIdMap[nodeA2], parserDblpXmlCls.graphNodeNameToIdMap[nodeA1], edgeProp])
                    

                #get relations of paper title <--> mediaTypeName
                if len(mediaType) is not 0 and len(mediaName) is not 0 and title is not '':
                    nodeM = mediaName + "+++"+ str(nodeTypeCls.mediaTypesToIdMap[mediaType])
                    nodeTitle = title + "+++"+ str(nodeTypeCls.commonTypeToIdMap["paper"])
                    if nodeM not in parserDblpXmlCls.graphNodeNameToIdMap:
                        parserDblpXmlCls.graphNodeNameToIdMap[nodeM] = parserDblpXmlCls.startNodeId
                        parserDblpXmlCls.startNodeId += 1
                    if nodeTitle not in parserDblpXmlCls.graphNodeNameToIdMap:
                        parserDblpXmlCls.graphNodeNameToIdMap[nodeTitle] = parserDblpXmlCls.startNodeId
                        parserDblpXmlCls.startNodeId += 1
                        
                    edgeProp = 'lower'             #lower level of hierarchical relation
                    parserDblpXmlCls.edgeList.append([parserDblpXmlCls.graphNodeNameToIdMap[nodeM], parserDblpXmlCls.graphNodeNameToIdMap[nodeTitle], edgeProp])
                    edgeProp = 'higher'             #higher hierarchical relation
                    parserDblpXmlCls.edgeList.append([parserDblpXmlCls.graphNodeNameToIdMap[nodeTitle], parserDblpXmlCls.graphNodeNameToIdMap[nodeM], edgeProp])
                    
                   
                    #delete and reinitiate
                    mediaName = ""
                    mediaType = ""
                    del authors[:]
                #get relations of node time <--> paper title
                if len(year) is not 0 and title is not '':
                    month = monthToDigitMap[month] if month in monthToDigitMap else month            #if month value is missing
                    nodeTime = month + '/' + year + '+++' + str(nodeTypeCls.commonTypeToIdMap["time"]) 
                    nodeTitle = title + "+++"+ str(nodeTypeCls.commonTypeToIdMap["paper"])
                    if nodeTime not in parserDblpXmlCls.graphNodeNameToIdMap:
                        parserDblpXmlCls.graphNodeNameToIdMap[nodeTime] = parserDblpXmlCls.startNodeId
                        parserDblpXmlCls.startNodeId += 1
                    if nodeTitle not in parserDblpXmlCls.graphNodeNameToIdMap:
                        parserDblpXmlCls.graphNodeNameToIdMap[nodeTitle] = parserDblpXmlCls.startNodeId
                        parserDblpXmlCls.startNodeId += 1
                        
                    edgeProp = 'same'             #same level of hierarchical relation
                    #inList = [parserDblpXmlCls.graphNodeNameToIdMap[nodeA], parserDblpXmlCls.graphNodeNameToIdMap[nodeTitle], edgeProp]
                    parserDblpXmlCls.edgeList.append([parserDblpXmlCls.graphNodeNameToIdMap[nodeTime], parserDblpXmlCls.graphNodeNameToIdMap[nodeTitle], edgeProp])
                    parserDblpXmlCls.edgeList.append([parserDblpXmlCls.graphNodeNameToIdMap[nodeTitle], parserDblpXmlCls.graphNodeNameToIdMap[nodeTime], edgeProp])
                    year = ""
                    month = ""
                    title = ""
            elem.clear()
        
        del context
    
        
    #print element in the console
    def printElementPair(self, elem, fout):
        print ("printing ... " + elem)
        print (fout, elem)
    
    #write graphNodeNameToIdMap, graNodeTypeMap, and edgeList
    def writeIntoFile(self, outNodeTypeFile, outNodeNameToIdFile, outEdgeListFile):
        #write node type file
        #os.remove(outNodeTypeFile) if os.path.exists(outNodeTypeFile) else None
        print ("nodeTypeCls.mediaTypesToIdMapxxxxx: ", nodeTypeCls.commonTypeToIdMap, nodeTypeCls.mediaTypesToIdMap)
        fd = open(outNodeTypeFile, 'w')
        for tp, tpId in nodeTypeCls.commonTypeToIdMap.items():
            writeListRowToFileWriterTsv(fd, [tp, tpId], '\t')
        
        for tp, tpId in nodeTypeCls.mediaTypesToIdMap.items():
            writeListRowToFileWriterTsv(fd, [tp, tpId], '\t')
    
        fd.close()
        
        #write into outNodeNameToIdFile
        os.remove(outNodeNameToIdFile) if os.path.exists(outNodeNameToIdFile) else None
        df = pd.DataFrame.from_dict(parserDblpXmlCls.graphNodeNameToIdMap, orient='index')
        df.to_csv(outNodeNameToIdFile, header = ["node_id"], sep='\t', index=True)
        
        #write into outEdgeListFile
        os.remove(outEdgeListFile) if os.path.exists(outEdgeListFile) else None
        df = pd.DataFrame(list(parserDblpXmlCls.edgeList))
        df.to_csv(outEdgeListFile, header = ["node_src_id", "node_dst_id", "edge_prop"], sep='\t', index=False)
        

    
def main():
    
    parseDblpXmlObj = parserDblpXmlCls()
    
    #outEdgeListFile = "output/outEdgeListFile.tsv"
    #os.remove(outEdgeListFile) if os.path.exists(outEdgeListFile) else None
    #fd = open(outEdgeListFile, 'a')
    
    context = etree.iterparse('../../dblp12012016/dblpPart2.xml', load_dtd=True, html=True)
    #context = etree.iterparse('../dblp12012016/dblp-2016-12-01.xml', load_dtd=True, html=True)
    parseDblpXmlObj.readParserXMl(context)
    
    
    outNodeTypeFile = "../output/outNodeTypeFile.tsv"
    outNodeNameToIdFile = "../output/outNodeNameToIdFile.tsv"
    outEdgeListFile = "../output/outEdgeListFile.tsv"
    
    parseDblpXmlObj.writeIntoFile(outNodeTypeFile, outNodeNameToIdFile, outEdgeListFile)
    
    
if __name__== "__main__":
  main()
  
