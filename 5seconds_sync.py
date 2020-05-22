#!/usr/bin/python
#-*- coding: utf-8 -*-
#-------------------------------------------------------------------------------------------#
#----The script the created to simulate IBCF 5 seconds mcast sync mechanism to optimize the 
#----factor in th vailable capacity allocation
#-------------------------------------------------------------------------------------------#
# version 1.0 
#-------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------#

'''
Usage:
    python 5seconds_sync.py -c 4000 -n 10 -l 20 -f 0.9

Tips:

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

# if run out of disk, CDR decode will error, could not go further to proceed
Sync_Data_Flag = False

# the five interval multi-cast used
SYNC_INTERVAL = 5

# the global dict to save all instances' local_usage
global_dict_usage = {}

# the global dict to mark if all instances has alreay sync the data and calculate the upper_bound
global_dict_updated = {}

# the global dict to mark if the upper_bound has been run out in the specified instance
global_dict_runout = {}

# the global dict to save local_usage, pre_local_usage, prepre_local_usage for specified instance
global_dict_local_record = {}

class Logger_Handler(object):
    def __init__(self, logger_name):
        '''
            logger_name must in string format
        '''
        try:
            logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                filename=logger_name,
                filemode='w')
            
            self.logger = logging.getLogger('LOG')
            self.logger.setLevel(logging.INFO)

            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(formatter)

            file_handler = logging.FileHandler(logger_name)
            file_handler.setLevel(logging.INFO)
            #file_handler.setFormatter(formatter)

            # create logger
            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)

        except:
            self.logger = None
        return

CDR_LOG = Logger_Handler('5seconds_sync.log').logger

def create_global_dict_local_record(_index):
    global global_dict_local_record
    local_record = {}
    local_record[0] = 0
    local_record[1] = 0
    local_record[2] = 0
    local_record[3] = 0 
    global_dict_local_record[_index] = local_record

def update_global_dict_local_record(_index, _value):
    global global_dict_local_record
    local_record = global_dict_local_record[_index]
    local_record[2] = local_record[1]
    local_record[1] = local_record[0]
    local_record[0] = _value
    
def main():
    '''All parameters are mandatory, please make sure they are used'''
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-c", "--capacity", dest="capacity", default='4000',
                      help="_system_capacity")
    parser.add_option("-n", "--nservers", dest="nservers",
                      help="_nservers: server instance count")
    parser.add_option("-l", "--load_per_s", dest="load_per_s",
                      help="load_per_s: load per second")
    parser.add_option("-f", "--factor", dest="factor",
                      help="factor: factor in formula")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose")
    (options, args) = parser.parse_args()

    if CDR_LOG is None:
        logging.critical("Could not create log handler, exit")
        return

    CDR_LOG.info("system_capacity=%s, nServers=%s, load_per_seconds=%s, formula_factor=%s", options.capacity, options.nservers, options.load_per_s, options.factor)

    system_capacity = int(options.capacity)
    nservers = int(options.nservers)
    load_per_s = int(options.load_per_s)
    factor = float(options.factor)

    global global_dict_updated
    global global_dict_runout
    global global_dict_usage
    global Sync_Data_Flag
    global global_dict_local_record
    # CREATE CHILD THREAD TO MAKE CALLS, SYNC, re-ALLOCATION
    threads_list = []
    instance_index = 0
    while instance_index < int(options.nservers):
        thread_identify = threading.Thread(target=ibcf_call_process_instance,args=(system_capacity, nservers, load_per_s, instance_index, factor, )) 
        threads_list.append(thread_identify)
        global_dict_updated[instance_index] = False
        global_dict_runout[instance_index] = False
        create_global_dict_local_record(instance_index)
        CDR_LOG.debug("create instance_index=%d", instance_index)

        instance_index = instance_index + 1

    for thread_identify in threads_list:
        thread_identify.setDaemon(True)
        thread_identify.start()

    # check diskusage to determine to stop child thread
    Sync_Data_Flag = False
    first_timestamp = datetime.datetime.now()

    internal_interval = (SYNC_INTERVAL-0.2) * 1000

    CDR_LOG.info("start to make call[+++++++++++++++++++++++++++++++++++++++++++]") 
    while True:
        # sleep INTEVAL to let child thread make calls
        if datetime.datetime.now() < first_timestamp + datetime.timedelta(milliseconds = internal_interval):
            continue
        
        # child instance finish making call in one INTERVAL, should let child update its local to global 
        Sync_Data_Flag = True

        # if all instances run out of the allocation capacity
        stop_process_flag = True
        for value in global_dict_runout.values():
            stop_process_flag = stop_process_flag & value
        
        if stop_process_flag == True:
            total_system_usage = 0
            for value in global_dict_usage.values():
                total_system_usage = total_system_usage + value
            CDR_LOG.warning("system_usage=%d, system_capacity=%d, deviation=%f", total_system_usage, system_capacity, total_system_usage/float(system_capacity) - 1.0)
            break

        # check if all instances updation finish

        flag = True
        while flag == True:
            flag = True
            for value in global_dict_updated.values():
                flag = value & flag
            
            if flag == True:
                # update timestamp
                first_timestamp = datetime.datetime.now()
                CDR_LOG.info("sync done! reset sync timer[+++++++++++++++++++++++++++++++++++++++++++]")
                # reset all flags
                Sync_Data_Flag = False
                for key in global_dict_updated.keys():
                    global_dict_updated[key] = False
                break

    # when parent thread quit, the child thread will quit
    for thread_identify in threads_list:
        thread_identify.join()

    return 0

def allocation_algorithm(_system_capacity, _nservers, _local_usage, _system_usage, _factor):
    if _nservers == 0:
        return 0

    if _nservers == 1 or _system_capacity == 0:
        return _system_capacity

    available = _system_capacity - _system_usage

    my_usage_fraction = 1.0
    if _system_usage != 0:
        my_usage_fraction = float(_local_usage) / float(_system_usage)

    my_allocation = my_usage_fraction * available
    if available >= 0:
        my_allocation_fraction = max((_factor * my_usage_fraction), 1.0/_nservers)
        my_allocation = min(my_allocation_fraction, 1.0) * available
    
    upper_bound = _local_usage + my_allocation
    
    CDR_LOG.debug("_system_capacity=%d, _nservers=%d, _local_usage=%d, _system_usage=%d, allocation_upper_bound=%d",_system_capacity, _nservers, _local_usage, _system_usage, upper_bound)
    return upper_bound

def ibcf_call_process_instance(_system_capacity, _nservers, _load_per_s, _thread_index, _factor):
    global Sync_Data_Flag
    global global_dict_runout

    local_usage = 0
    interval_start_timestamp = datetime.datetime.now()
    first_timestamp = datetime.datetime.now()
    up_bound = _system_capacity

    while local_usage < up_bound:
        if global_dict_updated[_thread_index] == True:
            continue
        if Sync_Data_Flag == False:
            if datetime.datetime.now() >= first_timestamp + datetime.timedelta(milliseconds=1000/_load_per_s) :
                first_timestamp = datetime.datetime.now()
                local_usage = local_usage + 1
                CDR_LOG.debug("[instance: %d]: make a new call, local_usage=%d, up_bound=%d", _thread_index, local_usage, up_bound)
                continue

        else:
            # start to sync data
            CDR_LOG.debug("[instance: %d]: %d seconds, start sync", _thread_index, SYNC_INTERVAL)
            global_dict_usage[_thread_index] = local_usage

            # wait for all instance has update local_usage to global
            time.sleep(0.005)

            # system usage for individual instance may be different, but close
            system_usage = 0
            for value in global_dict_usage.values():
                system_usage = system_usage + value
            
            #  need Algorithm to adjust up_bound per SYNC_INTERVAL
            up_bound = allocation_algorithm(_system_capacity, _nservers, local_usage, system_usage, _factor)
            #up_bound = allocation_algorithm_2(_system_capacity, _nservers, local_usage, system_usage, _factor, _thread_index)

            CDR_LOG.info("[instance: %d]: local_usage=%d, system_usage=%d, up_bound=%d, offset=%f", _thread_index, local_usage, system_usage, up_bound, system_usage/float(_system_capacity) - 1.0)
            
            global_dict_updated[_thread_index] = True
            continue

    global_dict_updated[_thread_index] = True
    global_dict_runout[_thread_index] = True
    global_dict_usage[_thread_index] = local_usage
    return # retrn from function: ibcf_call_process_instance

def allocation_algorithm_2(_system_capacity, _nservers, _local_usage, _system_usage, _factor, _index):
    global global_dict_local_record
    update_global_dict_local_record(_index, _local_usage)
    record = global_dict_local_record[_index]
    factor_A = 1.0
    if record[0] == 0 and record[1] == 0 and record[2] == 0:
        factor_A = 1.0
    elif record[1] == 0 and record[2] == 0:
        factor_A = 1.0
        
    else:
        factor_A = (record[1] - record[2]) / float(record[0] - record[1])

    if record[0] != 0:
        #factor_A = factor_A * (_local_usage / float(_system_usage)) * _system_capacity / float(record[0] * _nservers * 100)
        factor_A = factor_A * (_local_usage / float(_system_usage)) * (1 - float((record[0] - record[1]) * _nservers) / _system_capacity)

    #upper_bound = _system_capacity * factor_A
    #upper_bound = (0.005 / _nservers ) * _system_capacity  + _system_capacity / _nservers
    upper_bound = _system_capacity * factor_A
    return upper_bound

if __name__ == "__main__":
    CDR_LOG.info("+++++++++++++++++++++++++++++++START the Script++++++++++++++++++++++++++++++++")
    main()
    CDR_LOG.info("+++++++++++++++++++++++++++++++Quit From the Script++++++++++++++++++++++++++++")
