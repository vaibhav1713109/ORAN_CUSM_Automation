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
 * @file     M_CTC_ID_019.py
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

import sys, os, time, xmltodict, xml.dom.minidom, lxml.etree, socket
from lxml import etree
from ncclient import manager
from ncclient.operations.rpc import RPC, RPCError
from ncclient.transport import errors
from paramiko.ssh_exception import NoValidConnectionsError
from ncclient.operations.errors import TimeoutExpiredError
from ncclient.transport.errors import SessionCloseError
from ncclient.xml_ import to_ele
from configparser import ConfigParser

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
# from require.Vlan_Creation import *
# from require import STARTUP, Config
from require.Configuration import *

class M_CTC_ID_019(PDF,Configuration,netopeer_connection,genrate_pdf_report):
   
    # init method or constructor 
    def __init__(self):
        PDF.__init__(self)
        netopeer_connection.__init__(self)
        Configuration.__init__(self)
        genrate_pdf_report.__init__(self)
        PDF.PDF_CAP(self)
        self.summary = []
        self.u_name = '''
                <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                <users xmlns="urn:o-ran:user-mgmt:1.0">	
                </users>
                </filter>
                '''


    ###############################################################################
    ## Test Procedure
    ###############################################################################
    def test_execution(self):
        try:
            ###############################################################################
            ## Test Procedure 1 : Connect to netopeer server
            ###############################################################################
            Test_Step1 = 'STEP 1. The TER NETCONF Client establishes a connection with the O-RU NETCONF Server.'
            PDF.STORE_DATA(self,"{}".format(Test_Step1), Format='TEST_STEP')
            ###############################################################################
            ## Create_subscription
            ###############################################################################
            filter = """<filter type="xpath" xmlns="urn:ietf:params:xml:ns:netconf:notification:1.0" xmlns:notf_c="urn:ietf:params:xml:ns:yang:ietf-netconf-notifications" select="/notf_c:*"/>"""
            cmd = '> subscribe --filter-xpath /ietf-netconf-notifications:*'
            netopeer_connection.create_subscription(self,filter=filter,cmd=cmd)

            ###############################################################################
            ## Initial Get Filter
            ###############################################################################
            PDF.add_page(self)
            

            ###############################################################################
            ## Test Procedure 2 and 3 : O-RU NETCONF server replies by silently omitting data nodes
            ###############################################################################
            Test_STEP1 = "########### Step 2 and 3 O-RU NETCONF server replies by silently omitting data nodes #####################"
            PDF.STORE_DATA(self,'{}'.format(Test_STEP1),Format='TEST_STEP')
            xml_pretty_str, dict_data = netopeer_connection.get(self,filter=self.u_name,cmd=cmd)
            PDF.STORE_DATA(self,xml_pretty_str,Format='XML')
            try:
                pswrd = dict_data['data']['users']['user'][1]['password']  
                if pswrd:
                    Configuration.append_data_and_print(self,'NETCONF server replies by silently omitting data nodes || Fail')
                    return pswrd
            except:
                Configuration.append_data_and_print(self,'NETCONF server replies by silently omitting data nodes || Successful')
                return True

        except RPCError as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            PDF.STORE_DATA(self,f"Error occured in line number {exc_tb.tb_lineno}", Format=False)
            rpc_error_element = etree.ElementTree(e.xml)
            rpc_error = etree.tostring(rpc_error_element).decode()
            rpc_error = xml.dom.minidom.parseString(rpc_error).toprettyxml()
            PDF.STORE_DATA(self,rpc_error,Format='XML')
            # print(rpc_error,'test_execution')
            return rpc_error

                

    ###############################################################################
    ## Main Function
    ###############################################################################
    def Main_Function(self):
        Output = Configuration.Link_detction_and_check_ping(self)
        if Output[-1]!=True:
            return Output[0]
        self.hostname = Output[-2]

        try:
            time.sleep(10)
            netopeer_connection.delete_system_log(self,host= self.hostname)

            ###############################################################################
            ## Establishing netopeer connetion
            ###############################################################################
            self.session_login(timeout=60,username = self.username,password=self.password)
            
            if self.session:
                Configuration.append_data_and_print(self,'Netopeer Connection || Successful')
                Test_Desc = '''Test Description : This scenario is MANDATORY for an O-RU supporting the Hybrid M-plane architecture model.
                This test validates that the O-RU correctly implements NETCONF Access Control security aspects.
                The scenario corresponds to the following chapters in [3]:
                3.3 SSH Connection Establishment
                3.4 NETCONF Access Control'''
                Result = netopeer_connection.add_test_description(self,Test_Description=Test_Desc, Test_Case_name='M_CTC_ID_019')
            
                if len(Result) > 2:
                    self.running_sw, self.running_false_sw, self.inactive_slot = Result[0], Result[1], Result[2]

                self.STORE_DATA('{}'.format(Output[2]).center(100),Format=True,)
                self.STORE_DATA(Output[0],Format=False)
                self.STORE_DATA('{}'.format("ping -c 5 {}".format(self.hostname)).center(100),Format=True,)
                self.STORE_DATA(Output[1],Format=False)

                time.sleep(5)
                netopeer_connection.add_netopeer_connection_details(self)
                netopeer_connection.hello_capability(self)
                result = self.test_execution()
                print(result)
                if result == True:
                    return True
                else:
                    return result
                

        ###############################################################################
        ## Exception
        ###############################################################################
        except socket.timeout as e:
            Error = '{} : Call Home is not initiated, SSH Socket connection lost....'.format(e)
            PDF.STORE_DATA(self,Error, Format=True)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            PDF.STORE_DATA(self,f"Error occured in line number {exc_tb.tb_lineno}", Format=False)
            return Error
            
        except RPCError as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            PDF.STORE_DATA(self,f"Error occured in line number {exc_tb.tb_lineno}", Format=False)
            rpc_error_element = etree.ElementTree(e.xml)
            rpc_error = etree.tostring(rpc_error_element).decode()
            rpc_error = xml.dom.minidom.parseString(rpc_error).toprettyxml()
            PDF.STORE_DATA(self,rpc_error,Format='XML')
            return rpc_error

        except Exception as e:
            PDF.STORE_DATA(self,'{}'.format(e), Format=True)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            PDF.STORE_DATA(self,f"Error occured in line number {exc_tb.tb_lineno}", Format=False)
            return e
        
        finally:
            try:
                self.session.close_session()
            except Exception as e:
                print(e)
                
    def api_call(self):
        start_time = datetime.fromtimestamp(int(time.time()))
        Test_procedure = [f"{'='*100}\nTest case *M_CTC_ID_019* Started!! Status: Running\n{'='*100}",'** Test Coverage **'.center(50),'DHCP/STATIC IP Ping',
                    'Netopeer Connection','Capability exchange','Create-subscription filter','Get Filter User Management', 'Start Time : {}'.format(start_time),'='*100]
        notification('\n'.join(Test_procedure))
        Result = self.Main_Function()
        Configuration.Result_Declartion(self,'Access Control Sudo (negative case)',Result, 'M_CTC_ID_019')
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
    obj = M_CTC_ID_019()
    obj.api_call()

