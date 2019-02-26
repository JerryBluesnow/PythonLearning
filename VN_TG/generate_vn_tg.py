#!/usr/bin/python
#-*- coding: utf-8 -*-
#-------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------#
# load 1000 x 10 VN & TG into lab
#-------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------#

import sys
import os
from optparse import OptionParser

vn_suffix_str               = "|'peer_vn_auto'|1|0|0|1|1|''|''|'stdn'|0|0|1|1|1|000000|0|0|0000000000000000000000000000000000000000|"
tg_suffix_str               = "|'peer_tg_auto'|1|'173.18.0.2'|1258|00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000|0|0|0|00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000|0|0|2|2|0|0|2|0|0|0|0|0|0|0|0|0000000000000000000000000000000000000000|0|0|1|0|0|0|0|0|0|0|0|0|0|0|0|"
db_data_dir                 = "./" # the directory of appcnfg.ibcf_trunk_group.xdat and appcnfg.ibcf_virtual_network.xdat
virtual_network_file_name   =  "appcnfg.ibcf_virtual_network.xdat"
trunk_group_file_name       = "appcnfg.ibcf_trunk_group.xdat"
DEFAULT_START_VN_ID         = 4
DEFAULT_START_TG_ID         = 1
DEFAULT_MAX_TG_COUNT        = 10000
VN_ID_UP_BOUND              = 2048
TG_ID_UP_BOUND              = 32 # generate_tg_id should not bigger than TG_ID_UP_BOUND, make there is 10 tg in each virtual network
DEFAULT_TG_COUNT_PER_VN     = 10

# check if the input string is a number
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        pass
 
    return False

def scriptMenu():
    '''All parameters are mandatory, please make sure they are used'''
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-s", "--startvn", dest="startvn",
                      help="generate virtual network from start_vn = startvn")
    parser.add_option("-n", "--number", dest="tgnumber",
                      help="how many tg per virtual network")
    parser.add_option("-t", "--total", dest="tgtotal",
                      help="total tg gen_tg_count to be generated")
    parser.add_option("-r", "--recover", dest="recover",
                      help="recover the initial data before the script")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose")
    (options, args) = parser.parse_args()

    options.startvn, options.tgnumber, options.tgtotal

    start_vn        = DEFAULT_START_VN_ID
    tg_count_per_vn = DEFAULT_TG_COUNT_PER_VN
    max_tg_count    = DEFAULT_MAX_TG_COUNT

    if options.recover == 'yes':
        print "==========================Recover=============================================="
        os.system('cp appcnfg.ibcf_virtual_network.xdat.bk appcnfg.ibcf_virtual_network.xdat')
        os.system('cp appcnfg.ibcf_trunk_group.xdat.bk appcnfg.ibcf_trunk_group.xdat')
        os.system('dbload -noversion -u lssdba -p lssdba -table appcnfg.ibcf_virtual_network -rm')
        os.system('dbload -noversion -u lssdba -p lssdba -table appcnfg.ibcf_trunk_group -rm')
        print "========================== Done ==============================================="
        sys.exit(0)

    if is_number(options.startvn) == True:
        start_vn = int(options.startvn)

    if is_number(options.tgnumber) == True:
        tg_count_per_vn =  int(options.tgnumber)

    if is_number(options.tgtotal) == True:
        max_tg_count = int(options.tgtotal)

    print "==========================General Information=================================="
    print "generate Virtual Network from start_vn = %s" % start_vn
    print "generate %s TGs per Virtual Network from DEFAULT_START_TG_ID = 1" % tg_count_per_vn
    print "generate totally %s trunk group" % max_tg_count
    print "==============================================================================="

    return (start_vn, tg_count_per_vn, max_tg_count)

def generate_vn_tg_data(start_vn, tg_count_per_vn, max_tg_count):
    gen_tg_count = 0

    # open appcnfg.ibcf_virtual_network.xdat
    try:
        ibcf_virtual_network_fo = open(db_data_dir +  virtual_network_file_name, "a")
        ibcf_virtual_network_fo.write("\n")
    except IOError:
        print "failed to open", virtual_network_file_name

    # open appcnfg.ibcf_trunk_group.xdat  
    try:
        ibcf_trunk_group_fo = open(db_data_dir +  trunk_group_file_name, "a")
        ibcf_trunk_group_fo.write("\n")

    except IOError:
        print "failed to open", trunk_group_file_name
        return (False, gen_tg_count)
 
    generate_vn_id = start_vn
    while (generate_vn_id <= VN_ID_UP_BOUND) and (gen_tg_count < max_tg_count): 
        # construct vn_data to be inserted
        insert_vn_data = str(generate_vn_id) + vn_suffix_str + "\n"

        # write virtual network data to appcnfg.ibcf_virtual_network.xdat
        try:
            ibcf_virtual_network_fo.write(insert_vn_data)
        except IOError:
            print "failed to write to", virtual_network_file_name
            return (False, gen_tg_count)

        # must initialize generate_tg_id
        generate_tg_id = DEFAULT_START_TG_ID
        tmp_tg_count = 0
        while (generate_tg_id <= TG_ID_UP_BOUND) and (gen_tg_count < max_tg_count) and (tmp_tg_count < tg_count_per_vn):
            # construct tg_data to be inserted
            insert_tg_data = str(generate_vn_id) + "|" + str(generate_tg_id) + tg_suffix_str  + "\n"
            
            # write trunk group data to appcnfg.ibcf_trunk_group.xdat 
            try:
                ibcf_trunk_group_fo.write(insert_tg_data)
            except IOError:
                print "failed to write to", trunk_group_file_name
                return (False, gen_tg_count)

            tmp_tg_count    = tmp_tg_count + 1
            gen_tg_count    = gen_tg_count + 1
            
            generate_tg_id  = generate_tg_id + 1 
        
        generate_vn_id = generate_vn_id + 1

    # close the file obj
    try:
        ibcf_virtual_network_fo.close()
        ibcf_trunk_group_fo.close()
    except IOError:
        print "failed to close the file"
        return (False, gen_tg_count)
    
    # successfully create vn & tg data 
    return (True, gen_tg_count)

if __name__ == "__main__":
    start_vn, tg_count_per_vn, max_tg_count = scriptMenu()    

    #print "==============================================================================="
    #print "create directory to save dump data..."
    #print "create directory to save dump data..."
    #os.system('mkdir -p /storage/')
    #os.system('cd /storage/db_data_download')

    # dump data 
    print "==============================================================================="
    print "dump data to directory..."

    os.system('dbdump -noversion -u lssdba -p lssdba -table appcnfg.ibcf_virtual_network')

    os.system('dbdump -noversion -u lssdba -p lssdba -table appcnfg.ibcf_trunk_group')
    
    os.system('cp appcnfg.ibcf_virtual_network.xdat appcnfg.ibcf_virtual_network.xdat.bk')

    os.system('cp appcnfg.ibcf_trunk_group.xdat appcnfg.ibcf_trunk_group.xdat.bk')

    print "==============================================================================="
    print "start to generate data..."
    
    ret_value , gen_tg_count = generate_vn_tg_data(start_vn, tg_count_per_vn, max_tg_count)

    if ret_value == False:
        print "Error Happens, no need to load table back, as generated data may corrupt"
        print "==============================================================================="
        sys.exit(1)

    print "==============================================================================="
    print "start to load data to db..."

    os.system('dbload -noversion -u lssdba -p lssdba -table appcnfg.ibcf_virtual_network -rm')

    os.system('dbload -noversion -u lssdba -p lssdba -table appcnfg.ibcf_trunk_group -rm')

    print "==============================================================================="
    
    print "Generate %d TGs Successfully..." % gen_tg_count

    print "Warning: please make sure to call WaitForAllServicesInService after the script" 
