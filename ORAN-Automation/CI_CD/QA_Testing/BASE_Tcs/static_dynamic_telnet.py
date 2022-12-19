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
 * @file     Static_Dynamic_telnet.py
 * @part_of  CICD M PLANE O-RAN CONFORMANCE
 * @scope    Throughout the CD process
 * @author   CD Core Team. (Sebu Mathew, Vaibhav Dhiman,Vikas Saxena)
 *             (sebu.mathew@vvdntech.in,vaibhav.dhiman@vvdntech.in,vikas.saxena@vvdntech.in)
 * 
 *
 *
 */
 """
###############################################################################
import configparser,subprocess, re
import pexpect
import sys,os,time

dir_name = os.path.dirname(os.path.abspath(__file__))
parent = os.path.dirname(dir_name)
print(parent)


def send_and_receive_telnet_commands(child, command):
    child.sendline(command)
    child.expect('CLI:/>')
    output = child.before.decode().strip()
    return output

def Telnet_connection(host_ip, port_id, username, password):
    child = pexpect.spawn(f'telnet {host_ip} {port_id}')
    child.expect('Username :')
    child.sendline(username)
    child.expect('Password :')
    child.sendline(password)
    child.expect('CLI:/>')
    output = child.before.decode().strip()
    print(output)
    return child

def read_output_for_matching_string(output, match_string):
    lines = output.split('\n')
    for line in lines:
        if match_string in line:
            return True
    return False

def check_ping_status(ip_address):
    response = subprocess.Popen(f"ping -c 5 {ip_address}", shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = response.communicate()
    Response = stdout.decode()
    print(Response)
    pattern = '[1-5] received'
    ans  = re.search(pattern,Response)
    if ans:
        return True
    else:
        return False

def get_ip_address(ru_mac):
    Result = subprocess.getoutput(f'sudo journalctl -u isc-dhcp-server.service | grep "{ru_mac}" | grep "DHCPACK"')
    Result = Result.split('\n')
    dhcp_ip = ''
    pattern = '(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    ans = re.findall(pattern,Result[-1])
    if len(ans) > 0:
        dhcp_ip = ans[0]
        return dhcp_ip
    return ''

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('{}/inputs.ini'.format(parent))
    ru_mac = config.get('INFO', 'ru_mac')
    ru_name = config.get('INFO', 'ru_name')
    host_ip = config.get('INFO', 'static_ip')
    port_id = config.get('Telnet', 'port_id')
    username = config.get('Telnet', 'telnet_user')
    password = config.get('Telnet', 'telnet_password')
    dhcp_ip = get_ip_address(ru_mac)
    dhcp_ping = check_ping_status(dhcp_ip)
    if dhcp_ping == True:
        print(f'DHCP IP {dhcp_ip} ping || Successful, no need to run telnet')
        sys.exit(0)
    elif 'LPRU' in ru_name:
        ping_status = check_ping_status(host_ip)
        if ping_status == True:
            print(f'Static IP {host_ip} ping || Successful')
            child = Telnet_connection(host_ip, port_id, username, password)
            iface_status = send_and_receive_telnet_commands(child, 'get-IfaceStatus')
            print(iface_status)
            match_string = 'dhcp'
            if read_output_for_matching_string(iface_status, match_string):
                pass
                # if sys.argv[1] == "Dynamic":
                #     child.sendline('exit')
                #     sys.exit(0)
                # else:
                #     child.sendline('set-Ipv4Static 192.168.4.50 255.255.255.0 192.168.4.1')
                #     print("RU_Configured in Static")
                #     sys.exit(0)
            else:
            #     if sys.argv[1] == "Static":
            #         child.sendline('exit')
            #         sys.exit(0)
                # else:
                    child.sendline('set-IfaceDhcp')
                    print("RU is configured Dynamic.... Need to wait some time")
                    time.sleep(10)
                    sys.exit(0)
        else:
            print('Neither DHCP ip ping nor static ip ping')
        

