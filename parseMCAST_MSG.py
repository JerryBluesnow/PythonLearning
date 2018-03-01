import sys
import struct
import binascii
import ctypes

#read struct by struct, below is the struct length
STRUCT_LENGTH = 36
MCAST_HEADER_LENGTH = 24*2
MSG_HEADER_LENGTH = 4*2

#below is the structure of the struct, the defination
#parse_model = struct.Struct('I3sf')
#prebuffer = ctypes.create_string_buffer(parse_model)
parse_model='IIII'

INTER_LENGTH=4
CHAR_LENGTH=1
SHORT_LENGTH=2
FACTOR_MY=2
#sys.argv.append("D:\NewPC\workingTips\parseMcastMsgPython\Data.txt")

if __name__ == '__main__':

    f=open(sys.argv[1] ,'rb')
    f.seek(0,0)
    #read header
    read_content = f.read(MCAST_HEADER_LENGTH)
    if len(read_content) == MCAST_HEADER_LENGTH:
        pool_type = f.read(CHAR_LENGTH*FACTOR_MY)
        pool_id = f.read(CHAR_LENGTH*FACTOR_MY)
        vg_count = f.read(CHAR_LENGTH*FACTOR_MY)   
        vg_count = f.read(CHAR_LENGTH*FACTOR_MY)+vg_count
        print ("%10s%10s%10s"%('pooltype','poolid','vg_count'))
        print ("%10s%10s%10s"%(int(pool_type,16),int(pool_id,16),int(vg_count,16)))
        print ("%12s%12s%12s%12s%12s%12s%12s%12s%12s%12s"%('vn_id','tg_id','incmSess','outgSess','totalSess','incmBw','outgBw','totalBw','videoBw','audioBw'))
        while True:
            vn_id = f.read(CHAR_LENGTH*FACTOR_MY)                  
            if len(vn_id) == 0:
                break
                    
            vn_id = f.read(CHAR_LENGTH*FACTOR_MY) + vn_id

            tg_id = f.read(CHAR_LENGTH*FACTOR_MY)
            tg_id = f.read(CHAR_LENGTH*FACTOR_MY) + tg_id

            incmSess = f.read(CHAR_LENGTH*FACTOR_MY)
            incmSess = f.read(CHAR_LENGTH*FACTOR_MY) + incmSess
            incmSess = f.read(CHAR_LENGTH*FACTOR_MY) + incmSess
            incmSess = f.read(CHAR_LENGTH*FACTOR_MY) + incmSess  

            outgSess = f.read(CHAR_LENGTH*FACTOR_MY)
            outgSess = f.read(CHAR_LENGTH*FACTOR_MY) + outgSess
            outgSess = f.read(CHAR_LENGTH*FACTOR_MY) + outgSess
            outgSess = f.read(CHAR_LENGTH*FACTOR_MY) + outgSess  
        
            totalSess = f.read(CHAR_LENGTH*FACTOR_MY)
            totalSess = f.read(CHAR_LENGTH*FACTOR_MY) + totalSess
            totalSess = f.read(CHAR_LENGTH*FACTOR_MY) + totalSess
            totalSess = f.read(CHAR_LENGTH*FACTOR_MY) + totalSess  

        
            incmBw = f.read(CHAR_LENGTH*FACTOR_MY)
            incmBw = f.read(CHAR_LENGTH*FACTOR_MY) + incmBw
            incmBw = f.read(CHAR_LENGTH*FACTOR_MY) + incmBw
            incmBw = f.read(CHAR_LENGTH*FACTOR_MY) + incmBw  
        
            outgBw = f.read(CHAR_LENGTH*FACTOR_MY)
            outgBw = f.read(CHAR_LENGTH*FACTOR_MY) + outgBw
            outgBw = f.read(CHAR_LENGTH*FACTOR_MY) + outgBw
            outgBw = f.read(CHAR_LENGTH*FACTOR_MY) + outgBw
        
            totalBw = f.read(CHAR_LENGTH*FACTOR_MY)
            totalBw = f.read(CHAR_LENGTH*FACTOR_MY) + totalBw
            totalBw = f.read(CHAR_LENGTH*FACTOR_MY) + totalBw
            totalBw = f.read(CHAR_LENGTH*FACTOR_MY) + totalBw
        
            videoBw = f.read(CHAR_LENGTH*FACTOR_MY)
            videoBw = f.read(CHAR_LENGTH*FACTOR_MY) + videoBw
            videoBw = f.read(CHAR_LENGTH*FACTOR_MY) + videoBw
            videoBw = f.read(CHAR_LENGTH*FACTOR_MY) + videoBw
        
            audioBw = f.read(CHAR_LENGTH*FACTOR_MY)
            audioBw = f.read(CHAR_LENGTH*FACTOR_MY) + audioBw
            audioBw = f.read(CHAR_LENGTH*FACTOR_MY) + audioBw
            audioBw = f.read(CHAR_LENGTH*FACTOR_MY) + audioBw
        
            #print 
            #try:
            print ("%12d%12d%12d%12d%12d%12d%12d%12d%12d%12d"%(int(vn_id,16),int(tg_id,16),int(incmSess,16),int(outgSess,16),int(totalSess,16),int(incmBw,16),int(outgBw,16),int(totalBw,16),int(videoBw,16),int(audioBw,16)))
            #except Exception,e:
            #    print "Error Happens:" + str(e)
            #print vn_id.ljust(12), tg_id.ljust(12),incmSess.ljust(12),outgSess.ljust(12),totalSess.ljust(12),incmBw.ljust(12),outgBw.ljust(12),totalBw.ljust(12),videoBw.ljust(12),audioBw.ljust(12)
        
    f.close()
    print 'finish'
   
#wait any input to quit the display
raw_input() 
