#!/usr/bin/python
#-*- coding: utf-8 -*-
#-------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------#
# version 1.3 
#             1. in site, will generate 25 CDR files per hour, the size of each file is 15M,
#                version 1.2 need 20 minutes to process 25 files,
#                will need 24*20/60 = 8 hour to process all 24 hour CDR files,
#                introduce multi-thread to handle this.
#                BUG: bug now asnccflsearch only support decode one CDR file in the meantime
#                could not create 24 thread to process the 
#                In order to support above change(section 1), need use asnccflsearch_private
#             2. logging replace of print
#             3. add disk usage check to determine if child thread should be stopped
#-------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------#
# version 1.2 
#             1. take disk into consideration, in this version, the script will decode 1 cdr 
#                raw file and parse it, then delete the .decoded file; then go on to process
#                the new file
#             2. 24 hours will be supported.
#             3. if the output .csv/.raw.csv file exist, will delete it and create a new one
#-------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------#
# version 1.1 add INGRESS_ERLANGS/EGRESS_ERLANGS to replace INGRESS_DURATION/EGRESS_DURATION
#-------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------#

'''
Usage:
    python cdr_to_csv.py -d 2018/10/10 -s 14:00:00 -e 14:59:59 -p /storage/ccfl_app/charging/stream1/primary 2>&1 | tee ~/jerry.2.log
Tips:
    default filename format:
    CCFL0_-_133.20181011_-_1651+0530.decoded
    for UT test, need to: rename mum01-4 CCFL0 /storage/ccfl_app/charging/stream1/primary/*
'''
import sys
import time
import datetime
import csv
import codecs
import os
#from numpy import *
import random
import threading
import logging
import logging.handlers
from optparse import OptionParser

RecordHeader = "Record Header:"
IBCFRecord = "value IMSRecord ::= iBCFRecord :"
serviceDeliveryStartTimeStamp = "serviceDeliveryStartTimeStamp"
serviceDeliveryEndTimeStamp = "serviceDeliveryEndTimeStamp"
trunkGroupID = "trunkGroupID"
trunkGroupIDincoming = "incoming"
trunkGroupIDoutgoing = "outgoing"
PER_ERLANG_INTERVAL = 3600

RecordHeaderINDEX                       = 0
IBCFRecordINDEX                         = 1
serviceDeliveryStartTimeStampINDEX      = 2
serviceDeliveryEndTimeStampINDEX        = 3
trunkGroupIDINDEX                       = 4
trunkGroupIDincomingINDEX               = 5
trunkGroupIDoutgoingINDEX               = 6
# the above variable count 
RECORD_LIST_LENGTH                      = 7

CRITICAL_DISK_USAGE_RATE                = 0.95
WARNING_SECOND_DISK_USAGE_RATE          = 0.90
WARNING_FIRST_DISK_USAGE_RATE           = 0.85

AsnCCFLSearch_Tool  = '/export/home/lss/bin/asnccflsearch'

# if run out of disk, CDR decode will error, could not go further to proceed
Stop_Thread_Flag = False

call_duration_stored_directory = '/storage/duration_from_cdr'
cdr_decoded_directory = '/export/home/lss/ccfl_decode'
cdrDecodedFileDir = '/export/home/lss/ccfl_decode'

class Logger_Handler(object):
    def __init__(self, logger_name):
        '''
            logger_name must in string format
        '''
        try:
            logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                filename=logger_name,
                filemode='w')
            
            self.logger = logging.getLogger('LOG')
            self.logger.setLevel(logging.DEBUG)

            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.WARNING)
            console_handler.setFormatter(formatter)

            file_handler = logging.FileHandler(logger_name)
            file_handler.setLevel(logging.DEBUG)
            #file_handler.setFormatter(formatter)

            # create logger
            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)

        except:
            self.logger = None
        return

CDR_LOG = Logger_Handler('cdr_to_csv.log').logger

def disk_stat(folder):
    """
    """
    hd={}
    disk = os.statvfs(folder)
    #print(disk)
    # left disk
    hd['free'] = disk.f_bavail * disk.f_frsize
    # total disk
    hd['total'] = disk.f_blocks * disk.f_frsize
    # disk used
    hd['used'] = hd['total'] - hd['free']
    # disk usage rate
    hd['used_proportion'] =  float(hd['used']) / float(hd['total'])
    return hd

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
        CDR_LOG.info("%s: %d", sys._getframe().f_code.co_name, list_item)
    return 

def is_valid_cdr_file_string(str):
    '''check if the input string(mum01-4_-_24.20180816_-_1801+0530) is in a valide time format: "%Y%m%d_-_%H%M"'''
    CDR_LOG.info("Verify File Name %s if in good format: mum01-4_-_24.20180816_-_1801+0530", str)

    startpos = str.find('.')
    endpos = str.rfind('+')

    CDR_LOG.info("%s: Date information in filename, startpos: %d, endpos:%d",sys._getframe().f_code.co_name, startpos, endpos)
    if startpos == -1:
        return False
    if endpos == -1: 
        return False
    if (startpos + 1)  > endpos:
        return False
    if (startpos + 1)  == endpos:
        return False
    
    try:
        time.strptime(str[startpos+1:endpos], "%Y%m%d_-_%H%M")
        return True
    except:
        return False

def is_valid_date(str):
    '''check if the input string is in a valide time format: "%Y/%m/%d %H:%M:%S"'''
    try:
        time.strptime(str, "%Y/%m/%d %H:%M:%S")
        return True
    except:
        return False

def is_valid_Day(str):
    '''check if the input string is in a valide time format: "%Y/%m/%dS"'''
    try:
        time.strptime(str, "%Y/%m/%d")
        return True
    except:
        return False

def is_valid_HourMinSec(str):
    '''check if the input string is in a valide time format: "%H:%M:%S"'''
    try:
        time.strptime(str, "%H:%M:%S")
        return True
    except:
        return False


# serviceDeliveryStartTimeStamp "18/09/04 11:05:44+0530",\n',
def decodeServiceDeliveryStartTimeStamp(inputstring):
    if inputstring.find(serviceDeliveryStartTimeStamp) == -1:
        return
    first_delimiter = inputstring.find('"')
    second_delimiter = inputstring.rfind('+')
    #CDR_LOG.info(first_delimiter,second_delimiter
    if first_delimiter != second_delimiter:
        return_string = '20' + inputstring[first_delimiter+1: second_delimiter]
        if is_valid_date(return_string):
            #CDR_LOG.info(time.strptime(return_string, "%Y/%m/%d %H:%M:%S")
            return return_string
    return ""

def decodeServiceDeliveryEndTimeStamp(inputstring):
    if inputstring.find(serviceDeliveryEndTimeStamp) == -1:
        return
    first_delimiter = inputstring.find('"')
    second_delimiter = inputstring.rfind('+')
    #CDR_LOG.info(first_delimiter,second_delimiter
    if first_delimiter != second_delimiter:
        return_string = '20' + inputstring[first_delimiter+1: second_delimiter]
        if is_valid_date(return_string):
            #CDR_LOG.info(time.strptime(return_string, "%Y/%m/%d %H:%M:%S")
            return return_string
    return ""

def decodetrunkGroupIDincoming(inputstring):
    if inputstring.find(trunkGroupIDincoming) == -1:
        return
    first_delimiter = inputstring.find('"')
    second_delimiter = inputstring.rfind('"')
    #CDR_LOG.info(first_delimiter,second_delimiter
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
    #CDR_LOG.info(first_delimiter,second_delimiter
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
            CDR_LOG.info("%s, VN_ID-TG_ID: %s", sys._getframe().f_code.co_name, key)
            if key in resultDict.keys():
                tmp = resultDict[key]
                tmp[2] = tmp[2] + listitem[2]
                tmp[3] = tmp[3] + listitem[3]
            else:
                resultDict[key] = listitem
    for key in resultDict.keys():
        tmp = resultDict[key]
        tmp[2] = format(float(tmp[2]) / PER_ERLANG_INTERVAL, '.2f')
        tmp[3] = format(float(tmp[3]) / PER_ERLANG_INTERVAL, '.2f')

    durationSumRecordList=[]
    for item in resultDict.values():
        durationSumRecordList.append(item)
    return durationSumRecordList

def saveTileInforamtionRowToList(informationRowList, hostname, starttime, endtime, erlang_duration):
    first_row = []
    first_row.append('sbchostname')
    first_row.append('Starttime')
    first_row.append('Endtime')
    informationRowList.append(first_row)

    second_row = []
    second_row.append(hostname)
    second_row.append(starttime)
    second_row.append(endtime)
    informationRowList.append(second_row)
    
    if erlang_duration == 'DURATION':
        informationRowList.append(['VN_ID','TG_ID','INCOMING_DURATION','OUTGOING_DURATION'])
    elif erlang_duration == 'ERLANG':
        informationRowList.append(['VN_ID','TG_ID','INGRESS_ERLANGS','EGRESS_ERLANGS'])

    return

def saveDurtationInfoToCSV(InformationRowList, durationRecordList, outputCSVfile):
    ''' used to save per CDR call duration result to CSV '''
    ''' qa25b_20181011_000000-20181011_235959.raw.csv '''
    '''
    Final csv file format:
    sbchostname,Starttime,Endtime
    qa25b,20181011_000000,20181011_235959
    VN_ID,TG_ID,INCOMING_DURATION,OUTGOING_DURATION
    2,2,0.01,0.00
    1,1,0.00,0.01
    '''
    with open(outputCSVfile,"ab+") as csvfile: 
        csvfile.write(codecs.BOM_UTF8)  
        writer = csv.writer(csvfile) 
        writer.writerows(InformationRowList)   
        writer.writerows(durationRecordList)   

def saveErlangToCSV(InformationRowList, durationRecordList, outputCSVfile):
    ''' used to save per CDR call duration result to CSV '''
    ''' qa25b_20181011_000000-20181011_235959.csv '''
    '''
    Final csv file format:
    sbchostname,Starttime,Endtime
    qa25b,20181011_000000,20181011_235959
    VN_ID,TG_ID,INGRESS_ERLANGS,EGRESS_ERLANGS
    2,2,0.01,0.00
    1,1,0.00,0.01
    '''
    with open(outputCSVfile,"ab+") as csvfile: 
        csvfile.write(codecs.BOM_UTF8)  
        writer = csv.writer(csvfile) 
        #writer.writerow(['VN_ID','TG_ID','INGRESS_ERLANGS','EGRESS_ERLANGS'])
        writer.writerows(InformationRowList)   
        writer.writerows(durationRecordList)   

def decodeRecord(RecordItem):
    '''
    RecordItem is the decoded object for one CDR,
    it is in List format, from below indexs, associating information can be extracted.
    RecordHeaderINDEX                       = 0
    IBCFRecordINDEX                         = 1
    serviceDeliveryStartTimeStampINDEX      = 2
    serviceDeliveryEndTimeStampINDEX        = 3
    trunkGroupIDINDEX                       = 4
    trunkGroupIDincomingINDEX               = 5
    trunkGroupIDoutgoingINDEX               = 6
    '''
    if len(RecordItem) != RECORD_LIST_LENGTH:
        return [],[]

    start_time = decodeServiceDeliveryStartTimeStamp(RecordItem[serviceDeliveryStartTimeStampINDEX])
    end_time = decodeServiceDeliveryEndTimeStamp(RecordItem[serviceDeliveryEndTimeStampINDEX])

    # FIX BUG-13169: if the returned start_time or end_time is invalid, then the sript will be stopped if
    # the fix doesn't enabled
    if is_valid_date(start_time) == False or is_valid_date(end_time) == False:
        CDR_LOG.critical("Drop the record, because of error timestamp in CDR decode files")
        return None
    # FIX BUG-13169: END

    callDuriation = calculatePerCallRecordDuriation(start_time, end_time)
    incomingVN = getDecodedVN(decodetrunkGroupIDincoming(RecordItem[trunkGroupIDincomingINDEX]))
    incomingTG = getDecodedTG(decodetrunkGroupIDincoming(RecordItem[trunkGroupIDincomingINDEX]))
    outgoingVN = getDecodedVN(decodetrunkGroupIDoutgoing(RecordItem[trunkGroupIDoutgoingINDEX]))
    outgoingTG = getDecodedTG(decodetrunkGroupIDoutgoing(RecordItem[trunkGroupIDoutgoingINDEX]))
    
    CDR_LOG.info("VN=%d TG=%d, incoming CallDuration=%d", incomingVN, incomingTG, callDuriation)
    CDR_LOG.info("VN=%d TG=%d, outgoing CallDuration=%d", outgoingVN, outgoingTG, callDuriation)

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
        #CDR_LOG.info(list_item
        retvalue = decodeRecord(list_item)
        if retvalue is None:
            continue
        for item in retvalue:
            durationOverAllList.append(item)
    return 

# load input file
def loadCDRdecodedFile(fileName):  
    ''' used to load the CDR decoded raw text file, and then parse records in the file ''' 
    ''' save each record in a list, and save each ist in RecordList ''' 
    # CDR_LOG.info(file name loaded
    CDR_LOG.info("the file to be processed is: %s", fileName)
    # read lines from the file and CDR_LOG.info(it out to the screen
    RecordList = list()
    temp_record = list()
    with open(fileName, 'rt') as txtData:
        lines=txtData.readlines()
        for line in lines:
            line.strip()
            line.rstrip('\n')
            if line.find(RecordHeader) != -1:
                #CDR_LOG.info(line
                # append 0 -- RecordHeader
                if line in temp_record:
                    if validateRecord(temp_record) != -1:
                        #CDR_LOG.info("save the previous record to the list"
                        #CDR_LOG.info(temp_record
                        RecordList.append(temp_record)
                    ## reset the list to a new one
                    temp_record = list()
                temp_record.append(line)   

            elif line.find(IBCFRecord) != -1:
                #CDR_LOG.info(line
                temp_record.append(line)
                #CDR_LOG.info(temp_record
            elif line.find(serviceDeliveryStartTimeStamp) != -1:
                #CDR_LOG.info(line
                temp_record.append(line)
                #CDR_LOG.info(temp_record

            elif line.find(serviceDeliveryEndTimeStamp) != -1:
                #CDR_LOG.info(line
                temp_record.append(line)
                #CDR_LOG.info(temp_record
            elif line.find(trunkGroupID) != -1:
                #CDR_LOG.info(line
                temp_record.append(line)
                #CDR_LOG.info(temp_record
            elif line.find(trunkGroupIDincoming) != -1:
                # when not save the "trunkGroupID" block,  so the found incoming is not the right incoming
                if len(temp_record) < 5:
                    #CDR_LOG.info("has not save the trunkGroupID block,  so the found incoming is not the right incoming"
                    continue
                if trunkGroupID not in temp_record[4]:
                    #CDR_LOG.info("has not save the trunkGroupID block,  so the found incoming is not the right incoming"
                    continue
                # save the trunkGroupIDincoming
                temp_record.append(line)

            elif line.find(trunkGroupIDoutgoing) != -1:
                # when not save the "trunkGroupID" block,  so the found outgoing is not the right outgoing
                if len(temp_record) < 5:
                    #CDR_LOG.info("has not save the trunkGroupID block,  so the found outgoing is not the right outgoing"
                    continue
                if trunkGroupID not in temp_record[4]:
                    #CDR_LOG.info("has not save the trunkGroupID block,  so the found outgoing is not the right outgoing"
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
    CDR_LOG.info("%s input filename: %s", sys._getframe().f_code.co_name, filename)
    # time info in filename
    timeinfoinfile = filename[filename.find('.') + 1 : filename.rfind('+')]
    #CDR_LOG.info(timeinfoinfile
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
    '''
    checkFileInTimeRange('2018/08/16 17:59:00','2018/08/16 18:59:00','mum01-4_-_24.20180816_-_1801+0530.decoded')   # 0 - in range
    checkFileInTimeRange('2018/08/16 17:59:00','2018/08/16 18:59:00','mum01-4_-_24.20180816_-_1811+0530.decoded')   # 1
    checkFileInTimeRange('2018/08/16 17:59:00','2018/08/16 18:59:00','mum01-4_-_24.20180816_-_1859+0530.decoded')
    checkFileInTimeRange('2018/08/16 17:59:00','2018/08/16 18:59:00','mum01-4_-_24.20180816_-_1900+0530.decoded')
    checkFileInTimeRange('2018/08/16 17:59:00','2018/08/16 18:59:00','mum01-4_-_24.20180816_-_1759+0530.decoded')
    checkFileInTimeRange('2018/08/16 17:59:00','2018/08/16 18:59:00','mum01-4_-_24.20180817_-_1801+0530.decoded')   # out of range
    checkFileInTimeRange('2018/08/16 17:59:00','2018/08/16 18:59:00','mum01-4_-_24.20180815_-_1801+0530.decoded')   # out of range
    '''
    starttimeDatetime = string_toDatetime(starttime)
    endtimeDatetime = string_toDatetime(endtime)
    fileDatetime = CDRFileFormatString_toDatetime(inputfilename)
    if (starttimeDatetime < fileDatetime < endtimeDatetime) or fileDatetime == endtimeDatetime:
        CDR_LOG.info("%s: %s in range", sys._getframe().f_code.co_name, inputfilename) 
        return True
    else:
        CDR_LOG.info("%s: %s out of range", sys._getframe().f_code.co_name, inputfilename)
        return False

def main():
    '''All parameters are mandatory, please make sure they are used'''
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-p", "--path", dest="path", default='/storage/ccfl_app/charging/stream1/primary',
                      help="read the absolute directory/path of cdr raw files stored")
    parser.add_option("-d", "--day", dest="day",
                      help="read the day of cdr raw files to process, in Exact format 2018/10/11")
    parser.add_option("-s", "--starttime", dest="starttimestamp",
                      help="read the start timestamp of cdr raw files to process, in Exact format 09:01:00, don't miss any charactors")
    parser.add_option("-e", "--endttime", dest="endtimestamp",
                      help="read the end timestamp of cdr raw files to process, in Exact format 09:01:00, don't miss any charactors")
    parser.add_option("-t", "--tool", dest="tool", default='/export/home/lss/bin/asnccflsearch',
                      help="the parse tool to be called by the script to parse CDR files")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose")
    (options, args) = parser.parse_args()

    if CDR_LOG is None:
        logging.critical("Could not create log handler, exit")
        return

    if os.path.isdir(options.path):
        CDR_LOG.info("options.path: %s", options.path)
    else:
        CDR_LOG.info("-----------------WARNING:-----------------")
        CDR_LOG.critical("%s is not an absolute directory, please check it...", options.path)
        CDR_LOG.info("quit the script....")
        return -1
    if is_valid_Day(options.day):
        CDR_LOG.info("options.day: %s", options.day)
    else:
        CDR_LOG.info("-----------------WARNING:-----------------")
        CDR_LOG.critical("%s format wrong, good one is e.g. 2018/09/10, please check...", options.day)
        CDR_LOG.info("quit the script....")
        return -1
    if is_valid_HourMinSec(options.starttimestamp):
        CDR_LOG.info("options.starttimestamp: %s", options.starttimestamp)
    else:
        CDR_LOG.info("-----------------WARNING:-----------------")
        CDR_LOG.critical("%s format wrong, good one is e.g. 09:01:00, please check...", options.starttimestamp)
        CDR_LOG.info("quit the script....")
        return -1
    if is_valid_HourMinSec(options.endtimestamp):
        CDR_LOG.info("options.endtimestamp: %s", options.endtimestamp)
    else:
        CDR_LOG.info("-----------------WARNING:-----------------")
        CDR_LOG.critical("%s format wrong, good one is e.g. 09:01:00, please check...",options.endtimestamp)
        CDR_LOG.info("quit the script....")
        return -1

    if not os.path.isfile(options.tool):
        CDR_LOG.info("Could not find %s in current directory, or it's not a file", options.tool)
        return

    # if end timestamp is earlier than start timestamp, return from the script 
    if cmp(options.endtimestamp, options.starttimestamp) != 1:
        CDR_LOG.critical('ERROR: input endtimestamp is not later than start timestamp, return...')
        return -1

    CDR_LOG.info("good parameters input, go for further processing...")
    global AsnCCFLSearch_Tool
    AsnCCFLSearch_Tool = options.tool

    # /storage/ccfl_app/charging/stream1/primary
    # /storage/duration_from_cdr/ folder is used to store the calculation call duration result based on the input CDR folder...

    if os.path.isdir(call_duration_stored_directory):
        CDR_LOG.debug("%s exist, no need to create the directory", call_duration_stored_directory)
    else:
        CDR_LOG.debug("create the folder %s", call_duration_stored_directory)
        os.system('mkdir ' + call_duration_stored_directory)
    
    if os.path.isdir(cdr_decoded_directory):
        CDR_LOG.debug("%s exist, no need to create the directory ",cdr_decoded_directory)
        CDR_LOG.debug("clear up the folder %s", cdr_decoded_directory)
        os.system('rm ' + cdr_decoded_directory + '/*')
    else:
        CDR_LOG.debug("create the folder %s", cdr_decoded_directory)
        os.system('mkdir ' + cdr_decoded_directory)

    start_hour_stamp = string_toDatetime(options.day + ' ' + options.starttimestamp).replace(minute=0, second=0,microsecond=0)
    end_hour_stamp = string_toDatetime(options.day + ' ' + options.endtimestamp).replace(minute=0, second=0,microsecond=0)
    end_hour_stamp = end_hour_stamp + + datetime.timedelta(hours=1)

    hour_stamp = start_hour_stamp

    # version 1.3, add multi-threading, per hour per thread to process
    threads_list = []
    HOURS_STEP = 4
    file_count = 24
    CDR_LOG.info('+ HOURS STEP is defined: %d, %d thread will be created to process the file', HOURS_STEP, 24/HOURS_STEP)
    while end_hour_stamp > hour_stamp:
        thread_identify = threading.Thread(target=cdr_process_per_hours_step,args=(hour_stamp, options.path, HOURS_STEP,)) 
        threads_list.append(thread_identify)
        hour_stamp = hour_stamp + datetime.timedelta(hours=HOURS_STEP)

    CDR_LOG.info('+ Will Generate %d csv files...', file_count)

    for thread_identify in threads_list:
        thread_identify.setDaemon(True)
        thread_identify.start()

    # check diskusage to determine to stop child thread
    while True:
        time.sleep(3)
        hd = disk_stat('./')
        if hd['used_proportion'] > CRITICAL_DISK_USAGE_RATE:
            CDR_LOG.critical('disk usage: %.2f, Will stop processing, please make sure engough disk left for parse CDR',hd['used_proportion'])
            global Stop_Thread_Flag
            Stop_Thread_Flag = True
        elif hd['used_proportion'] > WARNING_SECOND_DISK_USAGE_RATE:
            CDR_LOG.warning('disk usage: %.2f, pay attention to disk usage',hd['used_proportion'])
        elif hd['used_proportion'] > WARNING_FIRST_DISK_USAGE_RATE:
            CDR_LOG.warning('disk usage: %.2f, pay attention to disk usage',hd['used_proportion'])
        else:
            continue

    # when parent thread quit, the child thread will quit
    for thread_identify in threads_list:
        thread_identify.join()

    return 0

def cdr_process_per_hours_step(_hour_stamp, _path, _hours_step):
    step_index = 0
    while _hours_step > step_index and Stop_Thread_Flag == False:
        cdr_process_per_hour_main(_hour_stamp, _path)
        _hour_stamp = _hour_stamp + datetime.timedelta(hours=1)
        step_index = step_index + 1
    return

def cdr_process_per_hour_main(_date_stamp, _path):
    # starttime/endtime in format "2018/10/10 18:59:00"
    starttime_dt = _date_stamp
    endtime_dt = _date_stamp + datetime.timedelta(hours=1)
    #endtime = (string_toDatetime(_day + ' ' + _starttime) + datetime.timedelta(hours=1) ).strftime('%Y/%m/%d %H:%M:%S')

    starttime = starttime_dt.strftime("%Y/%m/%d %H:%M:%S")
    endtime = endtime_dt.strftime("%Y/%m/%d %H:%M:%S")

    CDR_LOG.info('+++++++++++++++++++++++++++++++START+++++++++++++++++++++++++++++++++++++++++++')
    CDR_LOG.info('process cdr files with timestamp in the set (%s, %s]', starttime , endtime)

    filelist = os.listdir(_path) 
    durationOverAllList = []

    for filename in filelist:
        if Stop_Thread_Flag == True:
            return
        # valid the current file
        if is_valid_cdr_file_string(filename) == False:
            CDR_LOG.warning("Invalid file Name Format: %s, ignore it", filename)
            continue
        if checkFileInTimeRange(starttime, endtime, filename):
            CDR_LOG.info("To process the file: %s", filename)
            if _path[len(_path) - 1] == '/':
    	        os.system(AsnCCFLSearch_Tool + ' ' + _path + filename)
            else:
    	        os.system(AsnCCFLSearch_Tool + ' '+ _path + '/' + filename)
            # go on process the decoded file
            # 
            filelist = os.listdir(cdr_decoded_directory)
            # will only decoded file in this loop
            for filename in filelist: 
                if Stop_Thread_Flag == True:
                    return
                if is_valid_cdr_file_string(filename) == False:
                    CDR_LOG.warning("Invalid file Name Format:%s ,ignore it", filename)
                    continue
                if "_tmp_details" in filename:
                    CDR_LOG.debug("%s will not be processed as it is tmp file", filename)
                    continue
                if "_tmp_decoded" in filename:
                    CDR_LOG.debug("%s will not be processed as it is tmp file", filename)
                    continue
                if ".details" in filename:
                    CDR_LOG.debug("%s will not be processed as it is details file", filename)
                    continue
                
                if ".decoded" in filename and checkFileInTimeRange(starttime, endtime, filename):
                    CDR_LOG.info("process the decoded file: %s", filename)
                    resultRecordList = loadCDRdecodedFile( cdr_decoded_directory + '/' + filename)
                    #CDR_LOG.info(ecordList(resultRecordList)
                    retvalue = decodeRecordList(resultRecordList, durationOverAllList)
                    # remove all files in the decoded directory
                    CDR_LOG.debug("clearn up decoded file: %s", filename)
                    os.system('rm '+ cdr_decoded_directory + '/' + filename)
                    time.sleep(1)
                    details_file_name  = filename.replace('decoded', 'details')
                    CDR_LOG.debug("clearn up details file: %s", details_file_name)
                    os.system('rm '+ cdr_decoded_directory + '/' + details_file_name)
                    time.sleep(1)

    #CDR_LOG.info("clearn up decoded file....."
    #os.system('rm '+ cdr_decoded_directory + '/*')

    # get hostname from server, suppose there is '-' in hostname, just use the part before '-'
    hostname = os.popen('hostname').readline().split('-')[0]
    filename_starttime_string = datetime_string_to_filename_string(starttime)
    filename_endtime_string = datetime_string_to_filename_string(endtime)

    # make file name in format hostname_20181010_100000-20181010_105959
    # and will finally append ".csv"
    tosavedFilename = call_duration_stored_directory \
        + '/'  \
        +  hostname \
        + '_'\
        + filename_starttime_string \
        + '-' \
        + filename_endtime_string

    CDR_LOG.info("Calculation Result is to be saved in %s.csv", tosavedFilename)
    #CDR_LOG.info("Calculation Result Temp file is to be saved in %s.raw.csv", tosavedFilename)

    InformationRowList = []
    saveTileInforamtionRowToList(InformationRowList, 
        hostname,
        filename_starttime_string,
        filename_endtime_string,
        'DURATION')

    # if the output file exist, delete it
    if os.path.exists(tosavedFilename + '.raw.csv'):
        CDR_LOG.debug('%s.raw.csv exist, delete it', tosavedFilename)
        os.system('rm ' + tosavedFilename + '.raw.csv')
    
    if os.path.exists(tosavedFilename + '.csv'):
        CDR_LOG.debug('%s.csv exist, delete it', tosavedFilename)
        os.system('rm ' + tosavedFilename + '.csv')

    #saveDurtationInfoToCSV(InformationRowList, durationOverAllList, tosavedFilename + '.raw.csv')
    #CDR_LOG.info('%s.raw.csv Generating Complete!', tosavedFilename)

    InformationRowList = []
    erlangList = calculateCallRecordDuriationSum(durationOverAllList)
    saveTileInforamtionRowToList(InformationRowList,
        hostname,
        filename_starttime_string,
        filename_endtime_string,
        'ERLANG')

    saveErlangToCSV(InformationRowList, erlangList, tosavedFilename+'.csv')
    CDR_LOG.info('%s.csv Generating Complete!',tosavedFilename)
    CDR_LOG.info('+++++++++++++++++++++++++++++++END+++++++++++++++++++++++++++++++++++++++++++++')
    return 0

if __name__ == "__main__":
    main()
    CDR_LOG.info("parse done............... ")
    CDR_LOG.info("please check everything is ok......")
    CDR_LOG.info("+++++++++++++++++++++++++++++++Quit From the Script++++++++++++++++++++++++++++")
