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
 * @file     ISC_DHCP_SERVER.py
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
import random, ifcfg, subprocess, os

class test_isc_server_conf():
    def __init__(self) -> None:
        self.IPADDR = ''
        self.SUBNET_M = ''
        self.FLAG = False
        self.INTERFACE_NAME = ''
        self.STATIC_IP = ''
        pass

    ############################################ Return the interface which is detected ############################################
    def test_ethtool_linked(self,interface):
        cmd = "sudo ethtool " + interface
        Output = subprocess.getoutput(cmd).split('\n')
        for line in Output:
            if "Speed" in line and '1000' in line:
                self.INTERFACE_NAME = interface
                return self.INTERFACE_NAME

    ############################################  Test whether link is detected. ############################################
    def test_linked_detected(self):
        self.interfaces_name = ifcfg.interfaces()
        Interface = list(self.interfaces_name.keys())
        # print(Interface)
        for i in Interface:
            if self.test_ethtool_linked(i):
                s = self.test_ethtool_linked(i)


    # Genrate random ip for vlan
    def test_random_ip_genrate(self):
        x = random.randint(1,255)
        y = random.randint(1,255)
        self.IPADDR = '192.168.{}.{}'.format(x,y)

    # Read dhcp configuration and add data in dhcp configurration file.
    def test_read(self,interface,v_id):
        directory_path = os.path.dirname(__file__)
        # print(directory_path)
        file = open(os.path.join(directory_path,'../DATA','ISC_DHCP_SERVER.txt'), 'r+')
        data = file.readlines()
        # Chnage ip address for vlan scanning
        for i in data:
            if 'INTERFACESv4' in i:
                s = i.rstrip()
                if v_id:
                    new_i = f'INTERFACESv4="{interface}.{v_id}"\n'
                else:
                    new_i = f'INTERFACESv4="{interface}"\n'
                index_of_i = data.index(i)
                data[index_of_i] = new_i
                    # print(i)
            
        # for i in data:
        #     print(i)
        file1 = open('/etc/default/isc-dhcp-server', 'w+')
        file1.writelines(data)
        file1.close()

if __name__ == "__main__":
    obj = test_isc_server_conf()
    v_id = random.randint(10,30)
    obj.test_read('eth0',v_id)
    
