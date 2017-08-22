#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 23:52:30 2017

@author: fubao
"""

#main function for parser
import os
import numpy as np
import pandas as pd
from blist import blist

from readCityState import readcitySatesExecute
from extractweatherData import readUSAStationIdToNameMap

class nodeType:
    placeType = 1
    timeType = 2             #time type, year, month or day time
    tempType = 3             #temperature range
    prcpType = 4             #precipation
    snowType = 5             #snow depth
    
class graphCreationClass:
    startNodeId = 1            #graph node Id starting from 1
    graphNodeNameToIdMap  = {}            #store node name+type -> ID map
    gNodeIdToNameMap  = {}               #store node id -> name  map
    
    graNodeTypeMap = {}                 #node id to type
    edgeList = blist()                       #graph edge list  "nodeId, nodeId, edge"
    def __init__(self):
      pass
      