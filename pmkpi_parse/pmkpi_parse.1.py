#!/usr/bin/python
#-*- coding: utf-8 -*-
 
import sys
#tree = ET.parse(sys.argv[1])
import xml.dom.minidom

DOMTree = xml.dom.minidom.parse(sys.argv[1])
collection = DOMTree.documentElement
if collection.hasAttribute("shelf"):
   print("Root element : %s" % collection.getAttribute("type"))
# get attribute of an element

measInfos = collection.getElementsByTagName("measInfo")
# get child elements' collection by tag name    

for measInfo in measInfos:
    print "======================measInfo======================"
    
    # get granPeriod 
    granPeriod = measInfo.getElementsByTagName('granPeriod')[0]
    print "granPeriod",
    if granPeriod.hasAttribute("duration"):
        print "duration=%s" % granPeriod.getAttribute("duration"),
    
    if granPeriod.hasAttribute("endTime"):
        print "endTime=%s" % granPeriod.getAttribute("endTime")
    
    # get measType name in loop 
    measTypeList = measInfo.getElementsByTagName('measType')
    for measTypeItem in measTypeList:
        print "measType: %s" % measTypeItem.childNodes[0].data
    
    # get measType value in loop
    measValueList = measInfo.getElementsByTagName('measValue')
    for measValueItem in measValueList:
        if measValueItem.hasAttribute("measObjLdn"):
            print "measValue measObjLdn=%s" % measValueItem.getAttribute("measObjLdn")
        rvalueList = measValueItem.getElementsByTagName('r')
        for rvalueItem in rvalueList:
            if rvalueItem.hasAttribute("p"):
                print "r p=%s" % rvalueItem.getAttribute("p"),
                print "rvalue=%s" % rvalueItem.childNodes[0].data


   
   #parser.parse(sys.argv[1])