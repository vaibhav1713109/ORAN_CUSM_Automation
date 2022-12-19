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
 * @file     TM_2.py
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
import paramiko
import threading
from datetime import datetime
import pyvisa as visa
import os
from configparser import ConfigParser

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
from require.VXT_control import *
from require.genrate_report import genrate_report_dl_ul
from require.Notification import *

if len(sys.argv) < 2:
    print("Usage: python tc_CU_plane.py <tc_no>")
    sys.exit(555)

tc_no = sys.argv[1]
state_file = {"tc4":"TM_2.state"}
screen_shot_file = {"tc4":"TM_2.png"}
testmac_path = {"tc4":"runnr 0 1 100 12100"}
log_file1 = {"tc4":"TM2_ch1.txt"}
log_file2 = {"tc4":"TM2_ch2.txt"}



def send_to_testmac(channel, command):
    try:
        channel.send(command + "\n")
        start_time = time.monotonic()
        while True:
            if time.monotonic() - start_time >= 0.1:
                break
            time.sleep(0.01)
        return 0
    except paramiko.SSHException as e:
        print(f"Error sending command: {e}")
        return 5
    
def receive_until(channel,command, wait_string=None, timeout=None):
    start_time = time.monotonic()
    while True:
        if (time.monotonic() - start_time) < timeout:
            if channel.recv_ready():
                output = channel.recv(1024).decode("utf-8")
                print(output)
                if wait_string in output:
                    return 0
            else:
                if time.monotonic() - start_time < timeout:
                    continue
        else:
            print(f"\nCommand '{command}' timed out after {timeout} seconds\n")
            return 1

def send_and_recieve(channel, command, wait_string=None, timeout=None):
    if timeout or wait_string:
        if send_to_testmac(channel, command) != 0:
            return 5
        status = receive_until(channel,command, wait_string, timeout)
    else:
        print("Neither Check_string nor Timeout is Provided")    
        return 10
    return status

def command_to_testmac(channel, terminal, command, wait_string=None, is_separation=False, timeout=None):
    if is_separation:
        print("\n" + 25 * "*" + "  " + command + " in " + terminal + "  " + 25 * "*" + "\n")
        status = send_and_recieve(channel, command, wait_string, timeout)
        print("\n" + 70 * "*" + "\n")
    else:
        status = send_and_recieve(channel, command, wait_string, timeout)
    return status


def T1_Layer_1_xran(chan1):
    if command_to_testmac(chan1, "T1", "sudo su -", "vvdn:", False, 10) != 0:
        return 1
    if command_to_testmac(chan1, "T1", test_mac_password, "#", False, 10) != 0:
        return 1
    print("Logged in as root user in Terminal 1")    
    if command_to_testmac(chan1, "T1", "/home/vvdn/vf.sh", "root@vvdn:~#", True, 13) != 0:
        return 1
    time.sleep(10)
    if command_to_testmac(chan1, "T1", "cd /home/vvdn/Source/FlexRAN_v22.07_release_pacakge/", "root@vvdn:/home/vvdn/Source/FlexRAN_v22.07_release_pacakge#", False, 5) != 0:
        return 1
    if command_to_testmac(chan1, "T1", "source set_env_var.sh -d", "root@vvdn:/home/vvdn/Source/FlexRAN_v22.07_release_pacakge#", True, 15) != 0:
        return 1
    if command_to_testmac(chan1, "T1", "cd bin/nr5g/gnb/l1/", "root@vvdn:/home/vvdn/Source/FlexRAN_v22.07_release_pacakge/bin/nr5g/gnb/l1#", False, 5) != 0:
        return 1
    if command_to_testmac(chan1, "T1", "./l1.sh -xran", "PHY>welcome to application console", True, 40) != 0:
        return 1
    if command_to_testmac(chan1, "T1", "\n", "PHY>", False, 5) != 0:
        return 1
    return 0

def T2_Layer_2_Testmac(chan2):
    if command_to_testmac(chan2, "T2", "sudo su -", "vvdn:", False, 10) != 0:
        return 1
    if command_to_testmac(chan2, "T2", test_mac_password, "#", False, 10) != 0:
        return 1
    print("Logged in as root user in Terminal 2")    
    if command_to_testmac(chan2, "T2", "cd /home/vvdn/Source/FlexRAN_v22.07_release_pacakge/", "root@vvdn:/home/vvdn/Source/FlexRAN_v22.07_release_pacakge#", False, 5) != 0:
        return 1
    if command_to_testmac(chan2, "T2", "source set_env_var.sh -d", "root@vvdn:/home/vvdn/Source/FlexRAN_v22.07_release_pacakge#", True, 15) != 0:
        return 1
    if command_to_testmac(chan2, "T2", "cd bin/nr5g/gnb/testmac/", "root@vvdn:/home/vvdn/Source/FlexRAN_v22.07_release_pacakge/bin/nr5g/gnb/testmac#", False, 5) != 0:
        return 1
    if command_to_testmac(chan2, "T2", "./l2.sh", "TESTMAC>welcome to application console", True, 60) != 0:
        return 1
    if command_to_testmac(chan2, "T2", "\n", "TESTMAC>", False, 3) != 0:
        return 1
    return 0


def channel1_listener(channel1):
    global STOP_FLAG
    print("\n" + 30 * "*" + "Layer_1" + 30 * "*" + "\n") 
    with open("{}/Results/channel1_log.txt".format(parent_dir), "a") as file:
        while not STOP_FLAG:
            if channel1.recv_ready():
                output1 = channel1.recv(1024).decode("utf-8")
                file.write(output1)
                # print(output1)
            else:
                time.sleep(0.05)

def channel2_listener(channel2):
    global STOP_FLAG
    print("\n" + 30 * "*" + "Testmac" + 30 * "*" + "\n")
    with open("{}/Results/channel2_log.txt".format(parent_dir), "a") as file:
        while not STOP_FLAG:
            if channel2.recv_ready():
                output2 = channel2.recv(1024).decode("utf-8")
                file.write(output2)
                # print(output2)
            else:
                time.sleep(0.05)

def close_and_exit_from_test_mac(chan1,chan2,ssh1,ssh2):
    chan1.close()
    chan2.close()
    ssh1.close()
    ssh2.close()   

if __name__ == "__main__":
    try:
        start_time = datetime.fromtimestamp(int(time.time()))
        Test_procedure = [f"{'='*100}\nTest case *TM_2.py* Started!! Status: Running\n{'='*100}",'Start Time : {}'.format(start_time),'='*100]
        notification('\n'.join(Test_procedure))
        ru_mac = configur.get('INFO','ru_mac')
        ru_name = configur.get('INFO','ru_name')
        img_version = configur.get('INFO','img_version')
        ru_ip_detail = get_ip_address(ru_mac)
        if ru_ip_detail[-1] != True:
                print(ru_ip_detail)
                sys.exit(6000)
        ru_ip = ru_ip_detail[0]
        test_mac_ip = configur.get('CUPlane','test_mac_ip')
        test_mac_username = configur.get('CUPlane','test_mac_username')
        test_mac_password = configur.get('CUPlane','test_mac_password')
        ru_username = configur.get('INFO','super_user')
        ru_password = configur.get('INFO','super_pass')
        vxt_add = configur.get('CUPlane','vxt_add')
        print(test_mac_ip, test_mac_username, test_mac_password)
        chan1 = chan2 = ''
        STOP_FLAG = False
        print("Connecting to the Test-Mac server via T1")
        ssh1 = paramiko.SSHClient()
        ssh1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh1.connect(test_mac_ip, username=test_mac_username, password=test_mac_password)
        chan1 = ssh1.invoke_shell()
        time.sleep(2)
        if T1_Layer_1_xran(chan1) != 0:
            print("Command to Layer_1 Application failed,,, Aborting")
            chan1.close()
            ssh1.close()
            sys.exit(1000)

        print("Connecting to the Test-Mac server via T2")
        ssh2 = paramiko.SSHClient()
        ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh2.connect(test_mac_ip, username=test_mac_username, password=test_mac_password)
        chan2 = ssh2.invoke_shell()
        time.sleep(2)
        if T2_Layer_2_Testmac(chan2) != 0:
            print("Command to Testmac Application failed,,, Aborting")
            close_and_exit_from_test_mac(chan1,chan2,ssh1,ssh2)
            sys.exit(2000)

        # check_RU_Sync_Status()
        print('='*100)
        notification("checking_RU_Sync_State")
        print('='*100)
        time.sleep(2)
        RU_sync_status = check_RU_sync(ru_ip,ru_username,ru_password)
        if RU_sync_status!= True:
            ### Ru is not syncronized....
            print('='*100)
            notification('Ru is not syncronized....')
            print('='*100)
            sys.exit(3000)
        time.sleep(5)

        if command_to_testmac(chan2, "T2", "phystart 4 0 0", "TESTMAC>", False, 5) != 0:
            sys.exit
        #command_to_testmac(chan2, "T2", "runnr 0 0 10 1007", "Sebu", False, 1)
        send_to_testmac(chan2, testmac_path[tc_no])

        t1 = threading.Thread(target=channel1_listener, args=(chan1,))
        t2 = threading.Thread(target=channel2_listener, args=(chan2,))
        t1.start()
        t2.start()

        # check_RU_for_Ontime_Stats()
        time.sleep(30)
        print('='*100)
        print("checking_RU_Stats_for_ontime_count")
        print('='*100)
        # for _ in range(3):
        #     ru_stat_status = verify_ru_stat(ru_ip, ru_username, ru_password)
        #     if ru_stat_status != True:
        #         ### Ru Packets are not on time....
        #         print('='*100)
        #         print('Ru Packets are not on time....')
        #         print('='*100)
        #         pass
        #     else:
        #         print('='*100)
        #         print('Ru Packets are on time....')
        #         print('='*100)

        time.sleep(3)
        print('='*100)
        notification("checking_VXT_for Pass_Or_Fail")
        print('='*100)
        Result = VXT_control(state_file[tc_no],screen_shot_file[tc_no])
        print('='*100)
        report_path = f"{root_dir}/LOGS/{ru_name}/{img_version}/CUPLANE/TestMac/{screen_shot_file[tc_no].split('.')[0]}"
        notification("Stoping Data")
        time.sleep(5)
        
        STOP_FLAG = True
        t1.join()
        t2.join()

        genrate_report_dl_ul([Result[:-1]],report_path,Result[-1])
        if 'Pass' in Result:
            notification('{0}\n####{1}####\n{0}'.format('='*100,'Status :  Pass'.center(92)))
            sys.exit(0)
        else:
            if len(Result)>6 and len(Result)<12:
                notification('{}'.format('Fail Reason :  Low Power or Evm'))
            else:
                notification('{}'.format('Fail Reason :  Data from VXT not captured.'))
            notification('{0}\n####{1}####\n{0}'.format('='*100,'Status :  Fail'.center(92)))
            sys.exit(4000)
    finally:
        if chan2:
            command_to_testmac(chan2, "T2", "\n\n", "TESTMAC>", False, 5)
            command_to_testmac(chan2, "T2", "exit", "root@vvdn:/home/vvdn/Source/FlexRAN_v22.07_release_pacakge/bin/nr5g/gnb/testmac#", False, 5)
        if chan1:
            command_to_testmac(chan1, "T1", "\n\n", "PHY>", False, 5)
            command_to_testmac(chan1, "T1", "exit", "root@vvdn:/home/vvdn/Source/FlexRAN_v22.07_release_pacakge/bin/nr5g/gnb/l1#", False, 5)
        print("Exiting")
        if chan1 and chan2:
            close_and_exit_from_test_mac(chan1,chan2,ssh1,ssh2)
