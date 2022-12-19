###############################################################################
"""
 * ---------------------------------------------------------------------------
 *                              VVDN CONFIDENTIAL
 * ---------------------------------------------------------------------------
 * Copyright (c) 2016 - 2023 VVDN Technologies Pvt Ltd.
 * All rights reserved
 *
 * NOTICE:
 *      This software is confidential and proprietary to VVDN Technologies.
 *      No part of this software may be reproduced, stored, transmitted,
 *      disclosed or used in any form or by any means other than as expressly
 *      provided by the written Software License Agreement between
 *      VVDN Technologies and its license.
 *
 * PERMISSION:
 *      Permission is hereby granted to everyone in VVDN Technologies
 *      to use the software without restriction, including without limitation
 *      the rights to use, copy, modify, merge, with modifications.
 *
 * ---------------------------------------------------------------------------
 */

/**
 *
 * @file     TM_1_1.py
 * @part_of  CICD CUPLANE O-RAN CONFORMANCE
 * @scope    Throughout the CD process
 * @author   CD Core Team. (Sebu Mathew, Vaibhav Dhiman,Vikas Saxena)
 *             (sebu.mathew@vvdntech.in,vaibhav.dhiman@vvdntech.in,vikas.saxena@vvdntech.in)
 * 
 *
 *
 */
 """
###############################################################################

import sys
import time
import os
from configparser import ConfigParser
import paramiko
import threading
from datetime import datetime
import pyvisa as visa
import os
from configparser import ConfigParser
from scp import SCPClient

###############################################################################
## Directory Path
###############################################################################
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root_dir = os.path.dirname(parent_dir)

########################################################################
## For reading data from .ini file
########################################################################
configur = ConfigParser()
configur.read('{}/inputs.ini'.format(parent_dir))

###############################################################################
## Related Imports
###############################################################################
sys.path.append(parent_dir)
from require.ru_sync_and_ru_stat import *

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# print(root_dir)
configur = ConfigParser()
configur.read('{}/inputs.ini'.format(root_dir))


def run_xml_parser(host,ru_username,ru_password):
    try:
        local_file_path = f"{root_dir}/CUPLANE/TestMac/test.xml"
        # Define the destination path on the remote server
        remote_file_path = "/home/root/"
        ssh1 = paramiko.SSHClient()
        ssh1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh1.connect(host, username = ru_username, password =ru_password)
        scp = SCPClient(ssh1.get_transport())
        scp.put(local_file_path,remote_file_path)
        stdin, stdout, stderr = ssh1.exec_command('xml_parser test.xml; mw.l a008002c 6; mw.l a0080038 290')
        print(stderr.readlines())
        lines = stdout.readlines()
        print(*lines)
        return True
    except Exception as e:
        print(f'Run_xml_parser error : {e}')
        return False

if  __name__ == "__main__":
    ru_mac = configur.get('INFO','ru_mac')
    ru_username = configur.get('INFO','super_user')
    ru_password = configur.get('INFO','super_pass')
    Result = get_ip_address(ru_mac=ru_mac)
    if Result [-1] == True:
        print(Result[0],ru_username,ru_password)
        if run_xml_parser(Result[0],ru_username,ru_password):
            print('='*100)
            print('File transfer Success'.center(100))
            print('='*100)
            sys.exit(0)
        else:
            print('='*100)
            print('File transfer failed'.center(100))
            print('='*100)
            sys.exit(100)
    else:
        print('='*100)
        print('File transfer failed'.center(100))
        print('='*100)
        sys.exit(100)
