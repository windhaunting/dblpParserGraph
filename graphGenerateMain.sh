#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 00:33:41 2017

@author: fubao
"""


class parserDblpXmlCls:
    startNodeId = 1                      #graph node Id starting from 1
    graphNodeNameToIdMap  = {}           #store node name+type -> ID map
    gNodeIdToNameMap  = {}               #store node id -> name  map
    
    graNodeTypeMap = {}                 #node id to type
    edgeList = blist()                       #graph edge list  "nodeId, nodeId, edge"
    
    
    def __init__(self):
      pass
    
        #write type and type Id 
    def writeTypeFile(self, outFile):
        fd = open(outFile, 'a')
        for tp, tpId in nodeType.commonTypeToIdMap:
            writeListRowToFileWriterTsv(fd, [tp, tpId], '\t')
        
        for tp, tpId in nodeType.mediaTypesToIdMap:
            writeListRowToFileWriterTsv(fd, [tp, tpId], '\t')
    
        fd.close()
    
       #write node info ;  node name-type with nodeId
    def writeNodeInfoEdgeListFile(self, outFileNodeInfo, outFileEdgeListId):
 
        fd = open(outFile, 'a')
 
    
        fd.close()

def main():
    
    parseDblpXmlObj = parserDblpXmlCls()
    
    outEdgeListFile = "output/outEdgeListFile.tsv"
    os.remove(outEdgeListFile) if os.path.exists(outEdgeListFile) else None
    fd = open(outEdgeListFile, 'a')
    
    #context = etree.iterparse('../dblp/dblp-Part-Test.xml', load_dtd=True, html=True)
    context = etree.iterparse('../dblp12012016/dblpPart.xml', load_dtd=True, html=True)
    parseDblpXmlObj.readParserXMl(context, fd)
    
    fd.close()
    
    
if __name__== "__main__":
  main()
