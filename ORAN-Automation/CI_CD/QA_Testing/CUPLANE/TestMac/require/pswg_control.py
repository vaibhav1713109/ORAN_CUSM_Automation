import sys
import time
import pyvisa as visa
import os
from configparser import ConfigParser

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root_dir = os.path.dirname(parent_dir)
configur = ConfigParser()
configur.read('{}/inputs.ini'.format(parent_dir))

PWSG_add = configur.get('CUPlane','pwsg_add')
vxt_add = configur.get('CUPlane','vxt_add')
rm = visa.ResourceManager()
device = rm.open_resource(PWSG_add)
device.timeout = 2500

def SCPI_PWSG_write(cmnd):
    status = device.write(cmnd)
    print(f"{cmnd} {status}")
    
def pwsg_conf():
    try:
        scp_file = "C:\\Users\\Administrator\\Documents\\CU_Plane_Conf\\CTC_5GNR.scp"
        commands = [
                    ":RADio:SELect NR5G"
                    ,"RAD:NR5G:PRES"
                    ,"RAD:NR5G:PLAY:SEL VXT"
                    ,f'RAD:NR5G:WAV:FILE:IMPort "{scp_file}"'
                    ,"RAD:NR5G:PLAY:VXT:CONN:STAT?"
                    ,f'RAD:NR5G:PLAY:VXT:INST:ADDR "{vxt_add}"'
                    ,"RAD:NR5G:PLAY:VXT:CONN"
                    ,"RAD:NR5G:PLAY:VXT:CONN:STAT?"
                    ,"RAD:NR5G:PLAY:VXT:INST:FREQ 3.54234 GHz"
                    ,"RAD:NR5G:PLAY:VXT:INST:POW -60"
                    ,"RAD:NR5G:PLAY:VXT:INST:TRIG:TYPE CONT"
                    ,"RAD:NR5G:PLAY:VXT:INST:TRIG:TYPE:CONT TRIG"
                    ,"RAD:NR5G:PLAY:VXT:INST:TRIG EXT1"
                    ,"RAD:NR5G:PLAY:VXT:INST:TRIG:EXT:SLOP POS"
                    ,"RAD:NR5G:PLAY:VXT:INST:TRIG:EXT:DEL:STAT ON"
                    ,"RAD:NR5G:PLAY:VXT:INST:TRIG:EXT:DEL 0"
                    ,"RAD:NR5G:WAV:GEN"
        ]
        for cmd in commands:
            SCPI_PWSG_write(cmd)


        print('Complete')
        return True
    except Exception as e:
        print(f'Pwsg_conf Error : {e}')
        return False
    
if __name__ == "__main__":
    pwsg_conf()