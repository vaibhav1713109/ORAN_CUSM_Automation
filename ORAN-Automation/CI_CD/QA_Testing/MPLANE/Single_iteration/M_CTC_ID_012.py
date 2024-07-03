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
 * @file     M_CTC_ID_012.py
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

###############################################################################
## Package Imports 
###############################################################################

import socket, sys, os, warnings, time, xmltodict, xml.dom.minidom, paramiko, lxml.etree
from ncclient import manager
from ncclient.operations.rpc import RPC, RPCError
from ncclient.transport import errors
from paramiko.ssh_exception import NoValidConnectionsError
from ncclient.operations.errors import TimeoutExpiredError
from ncclient.transport.errors import SessionCloseError
from configparser import ConfigParser
from scapy.all import *

###############################################################################
## Directory Path
###############################################################################
dir_name = os.path.dirname(os.path.abspath(__file__))
parent = os.path.dirname(dir_name)
# print(parent)
sys.path.append(parent)

########################################################################
## For reading data from .ini file
########################################################################
configur = ConfigParser()
configur.read('{}/require/inputs.ini'.format(parent))

###############################################################################
## Related Imports
###############################################################################
from require.Notification import *
from require.Configuration import *
from require.calnexRest import calnexInit, calnexGet, calnexSet, calnexCreate, calnexDel,calnexGetVal



class M_CTC_ID_012(PDF,Configuration,netopeer_connection,genrate_pdf_report):
   
    # init method or constructor 
    def __init__(self):
        PDF.__init__(self)
        netopeer_connection.__init__(self)
        Configuration.__init__(self)
        genrate_pdf_report.__init__(self)
        PDF.PDF_CAP(self)
        self.ptp_port = configur.get('SPlane','port_num')
        self.P_NEO_IP = configur.get('SPlane','paragon_ip')
        self.summary = []
        self.sync_filter = '''<filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                <sync xmlns="urn:o-ran:sync:1.0">
                </sync>
                </filter>
                '''

    ###############################################################################
    ## Test Procedure
    ###############################################################################
    def test_execution(self,cmd,ethtool_out,ping_output):
        try:
            netopeer_connection.session_login(self,timeout=60,username=self.username, password=self.password)
            if self.session:
                Test_Desc = 'Test Description : The minimum functions of the TER described in section 2.1 that support validation of the M-Plane are operational, configured and connected to the O-RU.'
                Configuration.append_data_and_print(self,'Netopeer Connection || Successful')
                Test_Desc = '''Test Description : This scenario is MANDATORY for an O-RU supporting the Hybrid M-plane architecture model.
                        This test validates that the O-RU correctly implements NETCONF Access Control user privileges.
                        The scenario corresponds to the following chapters in [3]:
                        3.4 NETCONF Access Control '''   
                
                Result = netopeer_connection.add_test_description(self,Test_Description=Test_Desc, Test_Case_name='M_CTC_ID_012')
                if len(Result) > 2:
                    self.running_sw, self.running_false_sw, self.inactive_slot = Result[0], Result[1], Result[2]

                print(self.username,self.password)
                PDF.STORE_DATA(self,'{}'.format(cmd).center(100),Format=True,)
                PDF.STORE_DATA(self,ethtool_out,Format=False)
                PDF.STORE_DATA(self,'{}'.format("ping -c 5 {}".format(self.hostname)).center(100),Format=True,)
                PDF.STORE_DATA(self,ping_output,Format=False)

                netopeer_connection.add_netopeer_connection_details(self)
                netopeer_connection.hello_capability(self)
                ###############################################################################
                ## Test Procedure 1 : Connect to netopeer server with fm-pm user
                ###############################################################################
                Test_Step1 = 'STEP 1 TER NETCONF client establishes a connection using a user account with fm-pm privileges.'
                PDF.STORE_DATA(self,"{}".format(Test_Step1), Format='TEST_STEP')
                ###############################################################################
                ## Create_subscription
                ###############################################################################
                fm_filter = """<filter type="xpath" xmlns="urn:ietf:params:xml:ns:netconf:notification:1.0" xmlns:fm="urn:o-ran:fm:1.0" select="/fm:*"/>"""
                cmd = '> subscribe --filter-xpath /o-ran-fm:*'
                netopeer_connection.create_subscription(self,filter=fm_filter,cmd=cmd)


                ###############################################################################
                ## Initial Get
                ###############################################################################
                PDF.add_page(self)
                PDF.STORE_DATA(self,"\t\t########### Initial Get#####################",Format='TEST_STEP')
                cmd = "> get --filter-xpath /o-ran-sync:sync"
                xml_pretty_sync, dict_data_sync = netopeer_connection.get(self,filter=self.sync_filter,cmd=cmd)
                PDF.STORE_DATA(self,xml_pretty_sync,Format='XML')
                sync_state = dict_data_sync['data']['sync']['sync-status']['sync-state']
                if sync_state != 'FREERUN':
                    Configuration.append_data_and_print(self,f'Test_Execution Error || Sync State is {sync_state}')
                
                ###############################################################################
                ## Test Procedure 1: get filter of Locked state
                ###############################################################################
                xml_pretty_str = ''
                PDF.add_page(self)
                Test_Step1 = 'Step 1 The TER NETCONF Client periodically tests O-RU\'s sync-status until the LOCKED state is reached.'
                PDF.STORE_DATA(self,"\t\t{}".format(Test_Step1),Format='TEST_STEP')
                PDF.STORE_DATA(self,'\n>get --filter-xpath /o-ran-sync:sync',Format=True)
                start_time = time.time() + 480
                while time.time() < start_time:
                    xml_pretty_sync, dict_data_sync = netopeer_connection.get(self,filter=self.sync_filter,cmd='')
                    state = dict_data_sync['data']['sync']['sync-status']['sync-state']
                    if state == 'LOCKED':
                        PDF.STORE_DATA(self,xml_pretty_sync,Format='XML')
                        break
                else:
                    PDF.STORE_DATA(self,xml_pretty_sync,Format='XML')
                    return 'Sync-State "LOCKED" || Fail'
                Configuration.append_data_and_print(self,'Sync-State "LOCKED" || Success')

                ########################### Turn Off the PTP & SYNCE ############################
                calnexSet(f"app/mse/master/Master{self.ptp_port}/stop")
                calnexSet(f"app/generation/synce/esmc/Port{self.ptp_port}/stop")


                ########################### Check The Alarm No 17 ############################
                PDF.add_page(self)
                xml_pretty_str = ''
                PDF.STORE_DATA(self,'######## NOTIFICATIONS ########',Format=True)
                while True:
                    n = self.session.take_notification(timeout = 60)
                    if n == None:
                        return 1
                    notify=n.notification_xml
                    dict_n = xmltodict.parse(str(notify))
                    try:
                        notf = dict_n['notification']['alarm-notif']['fault-id']
                        type(notf)
                        if notf == '17':
                            ###############################################################################
                            ## Test Procedure 2
                            ###############################################################################
                            Test_Step2 = '\t\tStep 2 After a while (time depends on implementation) the O-RU NETCONF SERVER sends a notification for  alarm 17: No external sync source.'
                            PDF.STORE_DATA(self,"{}".format(Test_Step2),Format='TEST_STEP')
                            x = xml.dom.minidom.parseString(notify)
                            xml_pretty_str = x.toprettyxml()
                            PDF.STORE_DATA(self,xml_pretty_str,Format='XML')
                            break
                        else:
                            x = xml.dom.minidom.parseString(notify)
                            xml_pretty_str = x.toprettyxml()
                            PDF.STORE_DATA(self,xml_pretty_str,Format='XML')
                            pass
                    except:
                        pass
                Configuration.append_data_and_print(self,'Alarm notification with "fault-id 17" captured || Success')
            return True
        
        ###############################################################################
        ## Check Access Denied
        ###############################################################################
        except RPCError as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            PDF.STORE_DATA(self,f"Error occured in line number {exc_tb.tb_lineno}", Format=False)
            rpc_error_element = etree.ElementTree(e.xml)
            rpc_error = etree.tostring(rpc_error_element).decode()
            rpc_error = xml.dom.minidom.parseString(rpc_error).toprettyxml()
            PDF.STORE_DATA(self,rpc_error,Format='XML')
            return rpc_error
        except Exception as e:
            PDF.STORE_DATA(self,'Test_execution Error : {}'.format(e), Format=True)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            PDF.STORE_DATA(self,f"Error occured in line number {exc_tb.tb_lineno}", Format=False)
            return e

        finally:
            calnexSet(f"app/mse/master/Master{self.ptp_port}/stop")
            calnexSet(f"app/generation/synce/esmc/Port{self.ptp_port}/stop")
            try:
                self.session.close_session()
                print(f'Test_execution : Session {self.session.session_id} is closed..')
            except Exception as e:
                print('Test_execution Error : {}'.format(e))
    
    
    ###############################################################################
    ## Main Function
    ###############################################################################
    def Main_Function(self):
        Output = Configuration.Link_detction_and_check_ping(self)
        #print(Output)
        if Output[-1]!=True:
            return Output[0]
        self.hostname = Output[-2]
        
        paragon_ip_ping_status = Configuration.check_ping_status(self,self.P_NEO_IP)
        # print(type(Check1 and Check2))
        if paragon_ip_ping_status != True:
            return f'Paragon_ip_ping_status {self.P_NEO_IP} Failed'
            
        sys.path.append(f'//{self.P_NEO_IP}/calnex100g/RemoteControl/')
        calnexInit(f"{self.P_NEO_IP}")
        calnexSet(f"app/mse/master/Master{self.ptp_port}/start")
        calnexSet(f"app/generation/synce/esmc/Port{self.ptp_port}/start")

        time.sleep(5)

        try:
            time.sleep(10)
            netopeer_connection.delete_system_log(self,host= self.hostname)
            Result1 = self.test_execution(Output[2],Output[0],Output[1])
            return Result1


        ###############################################################################
        ## Exception
        ###############################################################################
        except Exception as e:
            PDF.STORE_DATA(self,'Main_Function Error : {}'.format(e), Format=True)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            PDF.STORE_DATA(self,f"Error occured in line number {exc_tb.tb_lineno}", Format=False)
            return e
        

    def api_call(self):
        start_time = datetime.fromtimestamp(int(time.time()))
        Test_procedure = [f"{'='*100}\nTest case *M_CTC_ID_012* Started!! Status: Running\n{'='*100}",'** Test Coverage **'.center(50),'DHCP/STATIC IP Ping',
                    'Netopeer Connection', 'Capability exchange','Create-subscription filter', 'Pre Get Filter Sync Manager', 'Wait unltil the sync state locked',
                    'Disable PTP', 'Captured alarm 17', 'Start Time : {}'.format(start_time),'='*100]
        notification('\n'.join(Test_procedure))
        Result = self.Main_Function()
        Configuration.Result_Declartion(self,'O-RU Alarm Notification Generation',Result, 'M_CTC_ID_012')
        end_time = datetime.fromtimestamp(int(time.time()))
        st_time = 'Start Time : {}'.format(start_time)
        en_time = 'End Time : {}'.format(end_time)
        execution_time = 'Execution Time is : {}'.format(end_time-start_time)
        print('-'*100)
        print(f'{st_time}\n{en_time}\n{execution_time}')
        self.summary.insert(0,'******* Result *******'.center(50))
        self.summary.insert(0,'='*100)
        notification('\n'.join(self.summary[:-1]))
        notification(f'{st_time}\n{en_time}\n{execution_time}')
        notification(f"{'='*100}\n{self.summary[-1]}\n{'='*100}")
        if Result !=True:
            sys.exit(1)
        pass
        

if __name__ == "__main__":
    obj = M_CTC_ID_012()
    obj.api_call()

