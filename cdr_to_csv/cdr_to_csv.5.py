#!/usr/bin/python
#-*- coding: utf-8 -*-
 
import sys
import time
import datetime
import csv
import codecs
import os
from numpy import *
import random
from optparse import OptionParser


RecordHeader = "Record Header:"
IBCFRecord = "value IMSRecord ::= iBCFRecord :"
serviceDeliveryStartTimeStamp = "serviceDeliveryStartTimeStamp"
serviceDeliveryEndTimeStamp = "serviceDeliveryEndTimeStamp"
trunkGroupID = "trunkGroupID"
trunkGroupIDincoming = "incoming"
trunkGroupIDoutgoing = "outgoing"

RecordHeaderINDEX                       = 0
IBCFRecordINDEX                         = 1
serviceDeliveryStartTimeStampINDEX      = 2
serviceDeliveryEndTimeStampINDEX        = 3
trunkGroupIDINDEX                       = 4
trunkGroupIDincomingINDEX               = 5
trunkGroupIDoutgoingINDEX               = 6
# the above variable count 
RECORD_LIST_LENGTH                      = 7

# check if the list element macth 
def validateRecord(oneRecordList):
    if len(oneRecordList) != RECORD_LIST_LENGTH:
        return -1
    if RecordHeader not in oneRecordList[0]: 
        return -1
    if IBCFRecord not in oneRecordList[1]:
        return -1
    if serviceDeliveryStartTimeStamp not in oneRecordList[2]:
        return -1
    if serviceDeliveryEndTimeStamp not in oneRecordList[3]:
        return -1
    if trunkGroupID not in oneRecordList[4]:
        return -1
    if trunkGroupIDincoming not in oneRecordList[5]:
        return -1
    if trunkGroupIDoutgoing not in oneRecordList[6]:
        return -1
    # validation of the input passed
    return 0

def printRecordList(RecordList): 
    for list_item in RecordList:
        print list_item
    return 

def is_valid_date(str):
    '''check if the input string is in a valide time format: "%Y/%m/%d %H:%M:%S"'''
    try:
        time.strptime(str, "%Y/%m/%d %H:%M:%S")
        return True
    except:
        return False

# serviceDeliveryStartTimeStamp "18/09/04 11:05:44+0530",\n',
def decodeServiceDeliveryStartTimeStamp(inputstring):
    if inputstring.find(serviceDeliveryStartTimeStamp) == -1:
        return
    first_delimiter = inputstring.find('"')
    second_delimiter = inputstring.rfind('+')
    #print first_delimiter,second_delimiter
    if first_delimiter != second_delimiter:
        return_string = '20' + inputstring[first_delimiter+1: second_delimiter]
        if is_valid_date(return_string):
            #print time.strptime(return_string, "%Y/%m/%d %H:%M:%S")
            return return_string
    return ""

def decodeServiceDeliveryEndTimeStamp(inputstring):
    if inputstring.find(serviceDeliveryEndTimeStamp) == -1:
        return
    first_delimiter = inputstring.find('"')
    second_delimiter = inputstring.rfind('+')
    #print first_delimiter,second_delimiter
    if first_delimiter != second_delimiter:
        return_string = '20' + inputstring[first_delimiter+1: second_delimiter]
        if is_valid_date(return_string):
            #print time.strptime(return_string, "%Y/%m/%d %H:%M:%S")
            return return_string
    return ""

def decodetrunkGroupIDincoming(inputstring):
    if inputstring.find(trunkGroupIDincoming) == -1:
        return
    first_delimiter = inputstring.find('"')
    second_delimiter = inputstring.rfind('"')
    #print first_delimiter,second_delimiter
    if first_delimiter != second_delimiter:
        return_string = inputstring[first_delimiter+1: second_delimiter]
        if len(return_string) != 8:
            return (0,0)
        return (int(return_string[0:4]), int(return_string[4:8]))
    return (0,0)

def decodetrunkGroupIDoutgoing(inputstring):
    if inputstring.find(trunkGroupIDoutgoing) == -1:
        return
    first_delimiter = inputstring.find('"')
    second_delimiter = inputstring.rfind('"')
    #print first_delimiter,second_delimiter
    if first_delimiter != second_delimiter:
        return_string = inputstring[first_delimiter+1: second_delimiter]
        if len(return_string) != 8:
            return (0,0)
        return (int(return_string[0:4]), int(return_string[4:8]))
    return (0,0)

def getDecodedVN(inputtuple):
    '''get VN "Virtual Network"'''
    if len(inputtuple) != 2:
        return 0
    return inputtuple[0]

def getDecodedTG(inputtuple):
    '''get TG "Trunk Group"'''
    if len(inputtuple) != 2:
        return 0
    return inputtuple[1]

def calculatePerCallRecordDuriation(start_str_time, end_str_time): 
    '''during in seconds will be returned'''
    starttime = string_toDatetime(start_str_time)
    endtime = string_toDatetime(end_str_time)
    return (endtime - starttime).seconds 

def calculateCallRecordDuriationSum(durationRecordList): 
    '''Sum Call Record Duriation'''
    resultDict = {}
    for listitem in durationRecordList:
        if len(listitem) == 4:
            key = str(listitem[0]) + '-' + str(listitem[1])
            print key
            if key in resultDict.keys():
                tmp = resultDict[key]
                tmp[2] = tmp[2] + listitem[2]
                tmp[3] = tmp[3] + listitem[3]
            else:
                resultDict[key] = listitem
    durationSumRecordList=[]
    for item in resultDict.values():
        durationSumRecordList.append(item)
    return durationSumRecordList

def saveDurtationInfoToCSV(durationRecordList, outputCSVfile):
    ''' used to save per CDR call duration result to CSV '''
    with open(outputCSVfile,"ab+") as csvfile: 
        csvfile.write(codecs.BOM_UTF8)  
        writer = csv.writer(csvfile) 
        writer.writerow(['VN_ID','TG_ID','INCOMING_DURATION','OUTGOING_DURATION'])
        writer.writerows(durationRecordList)   

def decodeRecord(RecordItem):
    if len(RecordItem) != RECORD_LIST_LENGTH:
        return [],[]

    start_time = decodeServiceDeliveryStartTimeStamp(RecordItem[serviceDeliveryStartTimeStampINDEX])
    end_time = decodeServiceDeliveryEndTimeStamp(RecordItem[serviceDeliveryEndTimeStampINDEX])
    callDuriation = calculatePerCallRecordDuriation(start_time, end_time)
    incomingVN = getDecodedVN(decodetrunkGroupIDincoming(RecordItem[trunkGroupIDincomingINDEX]))
    incomingTG = getDecodedTG(decodetrunkGroupIDincoming(RecordItem[trunkGroupIDincomingINDEX]))
    outgoingVN = getDecodedVN(decodetrunkGroupIDoutgoing(RecordItem[trunkGroupIDoutgoingINDEX]))
    outgoingTG = getDecodedTG(decodetrunkGroupIDoutgoing(RecordItem[trunkGroupIDoutgoingINDEX]))
    
    print "VN=%d" % incomingVN, "TG=%d" % incomingTG, "incoming CallDuration=%d" % callDuriation
    print "VN=%d" % outgoingVN, "TG=%d" % outgoingTG, "outgoing CallDuration=%d" % callDuriation

    incomingRecordDurationList = []
    incomingRecordDurationList.append(incomingVN)
    incomingRecordDurationList.append(incomingTG)
    incomingRecordDurationList.append(callDuriation)
    incomingRecordDurationList.append(0)
    
    outgoingRecordDurationList = []
    outgoingRecordDurationList.append(outgoingVN)
    outgoingRecordDurationList.append(outgoingTG)
    outgoingRecordDurationList.append(0)
    outgoingRecordDurationList.append(callDuriation)

    return incomingRecordDurationList,outgoingRecordDurationList
    

def decodeRecordList(RecordList, durationOverAllList):
    ''' used to parse the output of loadCDRdecodedFile() function'''
    for list_item in RecordList:
        #print list_item
        retvalue = decodeRecord(list_item)
        for item in retvalue:
            durationOverAllList.append(item)
    return 

# load input file
def loadCDRdecodedFile(fileName):  
    ''' used to load the CDR decoded raw text file, and then parse records in the file ''' 
    ''' save each record in a list, and save each ist in RecordList ''' 
    # print file name loaded
    print "the file to be processed is:", fileName
    # read lines from the file and print it out to the screen
    RecordList = list()
    temp_record = list()
    with open(fileName, 'rt') as txtData:
        lines=txtData.readlines()
        for line in lines:
            line.strip()
            line.rstrip('\n')
            if line.find(RecordHeader) != -1:
                #print line
                # append 0 -- RecordHeader
                if line in temp_record:
                    if validateRecord(temp_record) != -1:
                        #print "save the previous record to the list"
                        #print temp_record
                        RecordList.append(temp_record)
                    ## reset the list to a new one
                    temp_record = list()
                temp_record.append(line)   

            elif line.find(IBCFRecord) != -1:
                #print line
                temp_record.append(line)
                #print temp_record
            elif line.find(serviceDeliveryStartTimeStamp) != -1:
                #print line
                temp_record.append(line)
                #print temp_record

            elif line.find(serviceDeliveryEndTimeStamp) != -1:
                #print line
                temp_record.append(line)
                #print temp_record
            elif line.find(trunkGroupID) != -1:
                #print line
                temp_record.append(line)
                #print temp_record
            elif line.find(trunkGroupIDincoming) != -1:
                # when not save the "trunkGroupID" block,  so the found incoming is not the right incoming
                if len(temp_record) < 5:
                    #print "has not save the trunkGroupID block,  so the found incoming is not the right incoming"
                    continue
                if trunkGroupID not in temp_record[4]:
                    #print "has not save the trunkGroupID block,  so the found incoming is not the right incoming"
                    continue
                # save the trunkGroupIDincoming
                temp_record.append(line)

            elif line.find(trunkGroupIDoutgoing) != -1:
                # when not save the "trunkGroupID" block,  so the found outgoing is not the right outgoing
                if len(temp_record) < 5:
                    #print "has not save the trunkGroupID block,  so the found outgoing is not the right outgoing"
                    continue
                if trunkGroupID not in temp_record[4]:
                    #print "has not save the trunkGroupID block,  so the found outgoing is not the right outgoing"
                    continue
                # save the trunkGroupIDoutgoing
                temp_record.append(line)

    ## check if the list element macth 
    if validateRecord(temp_record) != -1:
        RecordList.append(temp_record)
    return  RecordList

def CDRFileFormatString_toDatetime(filename):
    '''"mum01-4_-_24.20180816_-_1801+0530.decoded" to "2018/08/16 18:01:00"'''
    #filename[filename.find('.')+1 : filename[filename.rfind('.')]
    print filename
    # time info in filename
    timeinfoinfile = filename[filename.find('.') + 1 : filename.rfind('+')]
    #print timeinfoinfile
    return datetime.datetime.strptime(timeinfoinfile, "%Y%m%d_-_%H%M")

def datetime_toString(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def datetime_string_to_filename_string(dt):
    rt = string_toDatetime(dt)
    return rt.strftime("%Y%m%d_%H%M%S")


def string_toDatetime(st):
    '''convert timestamp in string fromat to datetime format'''
    return datetime.datetime.strptime(st, "%Y/%m/%d %H:%M:%S")

def translateFileNametoTimeString(filename):
    '''"mum01-4_-_24.20180816_-_1801+0530.decoded" to "2018/08/16 18:01:00"'''
    return datetime_toString(CDRFileFormatString_toDatetime(filename))

def checkFileInTimeRange(starttime, endtime, inputfilename):
    ''''''
    starttimeDatetime = string_toDatetime(starttime)
    endtimeDatetime = string_toDatetime(endtime)
    fileDatetime = CDRFileFormatString_toDatetime(inputfilename)
    if (starttimeDatetime < fileDatetime < endtimeDatetime) or fileDatetime == starttimeDatetime:
        print "in range"
        return True
    else:
        print "out of range"
        return False


def main():
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-p", "--path", dest="path",
                      help="list file from the path")
    parser.add_option("-d", "--day", dest="day",
                      help="read day from input, in format 2018/10/11")
    parser.add_option("-s", "--starttime", dest="starttimestamp",
                      help="read start time from input， in format 09:01:00")
    parser.add_option("-e", "--endttime", dest="endtimestamp",
                      help="read end time from input, in format 11:01:35")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose")
    (options, args) = parser.parse_args()
    #if len(args) != 1:
    #    parser.error("incorrect number of arguments")
    #if options.verbose:
    #    print "reading %s..." % options.filename
    if options.path:
        print "options.path: ", options.path
    if options.day:
        print "options.day: ", options.day
    if options.starttimestamp:
        print "options.starttimestamp: ", options.starttimestamp
    if options.endtimestamp:
        print "options.endtimestamp: ", options.endtimestamp

    #resultRecordList = loadCDRdecodedFile(sys.argv[1])
    #printRecordList(resultRecordList)
    #durationOverAllList = []
    #retvalue = decodeRecordList(resultRecordList, durationOverAllList)
    #saveDurtationInfoToCSV(durationOverAllList, "Hello.csv")
    #os.system('dir *')
    #dt = translateFileNametoTimeString('mum01-4_-_24.20180816_-_1801+0530.decoded')
    #print dt
    starttime = options.day + ' ' + options.starttimestamp
    endtime = options.day + ' ' + options.endtimestamp
    #checkFileInTimeRange('2018/08/16 17:59:00','2018/08/16 18:59:00','mum01-4_-_24.20180816_-_1801+0530.decoded')   # 0 - in range
    #checkFileInTimeRange('2018/08/16 17:59:00','2018/08/16 18:59:00','mum01-4_-_24.20180816_-_1811+0530.decoded')   # 1
    #checkFileInTimeRange('2018/08/16 17:59:00','2018/08/16 18:59:00','mum01-4_-_24.20180816_-_1859+0530.decoded')
    #checkFileInTimeRange('2018/08/16 17:59:00','2018/08/16 18:59:00','mum01-4_-_24.20180816_-_1900+0530.decoded')
   # checkFileInTimeRange('2018/08/16 17:59:00','2018/08/16 18:59:00','mum01-4_-_24.20180816_-_1759+0530.decoded')
    #checkFileInTimeRange('2018/08/16 17:59:00','2018/08/16 18:59:00','mum01-4_-_24.20180817_-_1801+0530.decoded')   # out of range
    #checkFileInTimeRange('2018/08/16 17:59:00','2018/08/16 18:59:00','mum01-4_-_24.20180815_-_1801+0530.decoded')   # out of range

    #filelist = os.system('dir *')

    filelist = os.listdir(options.path) 
    durationOverAllList = []

    for filename in filelist:
        if checkFileInTimeRange(starttime, endtime, filename):
            os.system('asnccflsearch ')

            resultRecordList = loadCDRdecodedFile(options.path + '\\' + filename)
            #printRecordList(resultRecordList)
            retvalue = decodeRecordList(resultRecordList, durationOverAllList)

    tosavedFilename =  '/storage/duration_from_cdr/'+duration_' + datetime_string_to_filename_string(options.day + ' ' + options.starttimestamp) + '-' + datetime_string_to_filename_string(options.day + ' ' + options.endtimestamp) + '.csv'
    print "Calculation Result is to be saved in", tosavedFilename
    saveDurtationInfoToCSV(durationOverAllList, 'raw.'+tosavedFilename)
    saveDurtationInfoToCSV(calculateCallRecordDuriationSum(durationOverAllList), tosavedFilename)

if __name__ == "__main__":
    #main()