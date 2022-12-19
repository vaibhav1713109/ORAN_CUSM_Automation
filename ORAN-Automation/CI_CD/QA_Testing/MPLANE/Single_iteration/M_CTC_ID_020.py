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
 * @file     M_CTC_ID_020.py
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

import sys, os, time, xmltodict, xml.dom.minidom, socket
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
from require.Configuration import *
from require.Genrate_User_Pass import *


class M_CTC_ID_020(PDF,Configuration,netopeer_connection,genrate_pdf_report):
    # init method or constructor 
    def __init__(self):
        PDF.__init__(self)
        netopeer_connection.__init__(self)
        Configuration.__init__(self)
        genrate_pdf_report.__init__(self)
        PDF.PDF_CAP(self)
        self.summary = []
        self.new_user = ''
        self.new_pswrd = ''
        self.user_filter = '''
                <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                <users xmlns="urn:o-ran:user-mgmt:1.0">	
                </users>
                </filter>
                '''


    ###############################################################################
    ## ADD NMS User
    ########################################################from Notification import *#######################
    def add_NMS_user(self,cmd,ethtool_out,ping_output):
        try:
            netopeer_connection.session_login(self,timeout=60,username=self.username,password=self.password)
            if self.session :
                Configuration.append_data_and_print(self,'Netopeer Connection || Successful')
                Test_Desc = '''Test Description : TThis scenario is MANDATORY for an O-RU supporting the Hybrid M-plane architecture model.
                This test validates that the O-RU correctly implements NETCONF Access Control user privileges.
                The scenario corresponds to the following chapters in [3]:
                3.4 NETCONF Access Control'''
                Result = netopeer_connection.add_test_description(self,Test_Description=Test_Desc, Test_Case_name='M_CTC_ID_020')
            
                if len(Result) > 2:
                    self.running_sw, self.running_false_sw, self.inactive_slot = Result[0], Result[1], Result[2]

                self.STORE_DATA('{}'.format(cmd).center(100),Format=True,)
                self.STORE_DATA(ethtool_out,Format=False)
                self.STORE_DATA('{}'.format("ping -c 5 {}".format(self.hostname)).center(100),Format=True,)
                self.STORE_DATA(ping_output,Format=False)

                netopeer_connection.add_netopeer_connection_details(self)
                netopeer_connection.hello_capability(self)

                ###############################################################################
                ## Create_subscription
                ###############################################################################
                filter = """<filter type="xpath" xmlns="urn:ietf:params:xml:ns:netconf:notification:1.0" xmlns:notf_c="urn:ietf:params:xml:ns:yang:ietf-netconf-notifications" select="/notf_c:*"/>"""
                cmd = '> subscribe --filter-xpath /ietf-netconf-notifications:*'
                netopeer_connection.create_subscription(self,filter=filter,cmd=cmd)

                ###############################################################################
                ## Initial get filter
                ###############################################################################
                PDF.add_page(self)        
                cmd = "> get --filter-xpath /o-ran-usermgmt:users/user"
                xml_pretty_str, dict_data = netopeer_connection.get(self,filter=self.user_filter,cmd=cmd)
                PDF.STORE_DATA(self,xml_pretty_str, Format='XML')
                Configuration.append_data_and_print(self,'Pre User-mgmt get-filter || Successful')

                ###############################################################################
                ## Merge New User
                ###############################################################################
                Configuration.append_data_and_print(self,"Merging NMS user || Started")
                nms_user_xml = f"""
                    <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                    <users xmlns="urn:o-ran:user-mgmt:1.0">
                        <user>
                            <name>{self.nms_user}</name>
                            <account-type>PASSWORD</account-type>
                            <password>{self.nms_pswrd}</password>
                            <enabled>true</enabled>
                        </user>
                    </users>
                    </config>"""

                
                rpc_reply = netopeer_connection.edit_config(self,nms_user_xml,'merge')
                if rpc_reply != True:
                    Configuration.append_data_and_print(self,"Merging NMS user || Fail")
                    return rpc_reply
                Configuration.append_data_and_print(self,"Merging NMS user || Successful")
                ###############################################################################
                ## Check_Notifications
                ###############################################################################
                while True:
                    
                    n = self.session.take_notification(timeout=10)
                    if n == None:
                        break
                    notify = n.notification_xml
                    dict_n = xmltodict.parse(str(notify))
                    try:
                        sid = dict_n['notification']['netconf-config-change']['changed-by']['session-id']
                        if sid == self.session.session_id:
                            PDF.STORE_DATA(self,"******* NOTIFICATIONS *******",Format=True)
                            x = xml.dom.minidom.parseString(notify)
                            xml_pretty_str = x.toprettyxml()
                            PDF.STORE_DATA(self,xml_pretty_str,Format='XML')
                            Configuration.append_data_and_print(self,"Notification Captured || Successful")
                            break
                    except:
                        pass
                
                ###############################################################################
                ## Configure New User In NACM
                ###############################################################################
                Configuration.append_data_and_print(self,"Give NMS privilege || Started")
                ad_us = f'<user-name>{self.nms_user}</user-name>'
                nacm_file = open('{}/require/Yang_xml/nacm_nms.xml'.format(parent)).read()
                nacm_file = nacm_file.format(add_nms = ad_us)
                
                rpc_reply = netopeer_connection.edit_config(self,nacm_file,'merge')
                if rpc_reply != True:
                    Configuration.append_data_and_print(self,"Give NMS privilege || Fail")
                    return rpc_reply
                Configuration.append_data_and_print(self,"Give NMS privilege || Success")
                ###############################################################################
                ## Check_Notifications
                ###############################################################################
                while True:
                    n = self.session.take_notification(timeout=10)
                    if n == None:
                        break
                    notify = n.notification_xml
                    dict_n = xmltodict.parse(str(notify))
                    try:
                        sid = dict_n['notification']['netconf-config-change']['changed-by']['session-id']
                        if sid == self.session.session_id:
                            PDF.add_page(self)
                            PDF.STORE_DATA(self,"******* NOTIFICATIONS *******",Format=True)
                            x = xml.dom.minidom.parseString(notify)
                            xml_pretty_str = x.toprettyxml()
                            PDF.STORE_DATA(self,xml_pretty_str,Format='XML')
                            Configuration.append_data_and_print(self,"Nacm Notification Captured || Successful")
                            break
                    except:
                        pass

                ###############################################################################
                ## Get Filter of NACM
                ###############################################################################
                cmd = "> get --filter-xpath /ietf-netconf-acm:nacm/groups"
                xml_pretty_str, dict_data = netopeer_connection.get(self,filter=self.user_filter,cmd=cmd)
                PDF.STORE_DATA(self,xml_pretty_str, Format='XML')
                    
                
                PDF.add_page(self)
                cmd = "> get --filter-xpath /o-ran-usermgmt:users/user"
                xml_pretty_str, dict_data = netopeer_connection.get(self,filter=self.user_filter,cmd=cmd)
                PDF.STORE_DATA(self,xml_pretty_str, Format='XML')
                Configuration.append_data_and_print(self,'Post User-mgmt get-filter || Successful')
                
                ###############################################################################
                ## Check whether users are merge
                ###############################################################################
                USERs_info = dict_data['data']['users']['user']
                User_list = []
                for user in USERs_info:
                    User_list.append(user['name'])
                if  self.nms_user not in User_list:
                    PDF.STORE_DATA(self,xml_pretty_str,Format='XML')
                    return "Users didn't merge..."
                else:
                    PDF.STORE_DATA(self,xml_pretty_str,Format='XML')
                Configuration.append_data_and_print(self,"User merge and give NMS privilage || Successful")
                return True
            
        except RPCError as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            PDF.STORE_DATA(self,f"Error occured in line number {exc_tb.tb_lineno}", Format=False)
            rpc_error_element = etree.ElementTree(e.xml)
            rpc_error = etree.tostring(rpc_error_element).decode()
            rpc_error = xml.dom.minidom.parseString(rpc_error).toprettyxml()
            print(rpc_error)
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




    ###############################################################################
    ## Test Procedure
    ###############################################################################
    def test_execution(self):
        try:
            print(self.nms_pswrd,self.nms_user)
            netopeer_connection.session_login(self,timeout=60,username=self.nms_user,password=self.nms_pswrd)
            if self.session :


                ###############################################################################
                ## Test Procedure 1 : Connect to netopeer server with NMS user
                ###############################################################################
                Test_Step1 = 'STEP 1 TER NETCONF client establishes a connection using a user account with nms privileges.'
                PDF.STORE_DATA(self,"{}".format(Test_Step1), Format='TEST_STEP')
                # netopeer_connection.add_netopeer_connection_details(self)
                # netopeer_connection.hello_capability(self)

                ###############################################################################
                ## Create_subscription
                ###############################################################################
                filter = """<filter type="xpath" xmlns="urn:ietf:params:xml:ns:netconf:notification:1.0" xmlns:notf_c="urn:ietf:params:xml:ns:yang:ietf-netconf-notifications" select="/notf_c:*"/>"""
                cmd = '> subscribe --filter-xpath /ietf-netconf-notifications:*'
                netopeer_connection.create_subscription(self,filter=filter,cmd=cmd)

        
        
                ###############################################################################
                ## Test Procedure 2 : Configure new user\password.
                ###############################################################################
                PDF.add_page(self)
                Test_Step2 = 'Step 2 TER NETCONF client attempts to configure a new user/password.'
                PDF.STORE_DATA(self,'{}'.format(Test_Step2), Format='TEST_STEP')
                Configuration.append_data_and_print(self,"Try to configure new user || In progress")

                ###############################################################################
                ## Merge New User
                ###############################################################################
                user_xml = f"""
                        <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                        <users xmlns="urn:o-ran:user-mgmt:1.0">
                            <user>
                                <name>{self.new_user}</name>
                                <account-type>PASSWORD</account-type>
                                <password>{self.new_pswrd}</password>
                                <enabled>true</enabled>
                            </user>
                        </users>
                        </config>"""

                rpc_reply = netopeer_connection.edit_config(self,user_xml,'merge')
                if rpc_reply == True:
                    print(rpc_reply)
                    return 'Addition of new user is successful...'
                    
                ###############################################################################
                ## Check Access Denied
                ###############################################################################
                elif 'access-denied' in str(rpc_reply):
                    Test_Step3 = 'Step 3 NETCONF server replies rejecting the protocol operation with an \'access-denied\' error'
                    PDF.STORE_DATA(self,'{}'.format(Test_Step3), Format='TEST_STEP')
                    PDF.STORE_DATA(self,'RPC ERROR'.center(100), Format=True)
                    PDF.STORE_DATA(self,rpc_reply, Format=False)
                    Configuration.append_data_and_print(self,'Access-denied error captured || Successful')
                    return True
                else:
                    PDF.STORE_DATA(self,'RPC ERROR'.center(100), Format=True)
                    PDF.STORE_DATA(self,rpc_reply, Format=False)
                    return rpc_reply

        
        except RPCError as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            PDF.STORE_DATA(self,f"Error occured in line number {exc_tb.tb_lineno}", Format=False)
            rpc_error_element = etree.ElementTree(e.xml)
            rpc_error = etree.tostring(rpc_error_element).decode()
            rpc_error = xml.dom.minidom.parseString(rpc_error).toprettyxml()
            print(rpc_error)
            return rpc_error

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            PDF.STORE_DATA(self,"\t\tError : {}".format(e), Format=False)
            # new_session.close_session()
            return f"{e} \nError occured in line number {exc_tb.tb_lineno}"

        finally:
            try:
                self.session.close_session()
            except Exception as e:
                print(e)


    ###############################################################################
    ## Main Function
    ###############################################################################
    def Main_Function(self):
        Output = Configuration.Link_detction_and_check_ping(self)
        if Output[-1]!=True:
            return Output[0]
        self.hostname = Output[-2]
        
        
        ###############################################################################
        ## Read User Name and password from Config.INI of Config.py
        ############################################################################### 
        self.nms_user = genrate_username()
        self.nms_pswrd = genrate_password()
        self.new_user = genrate_username()
        self.new_pswrd = genrate_password()
        try:
            time.sleep(10)
            netopeer_connection.delete_system_log(self,host= self.hostname)
            result = self.add_NMS_user(Output[2],Output[0],Output[1])
            if result != True:
                return result
            Result1 = self.test_execution()
            return Result1


        ###############################################################################
        ## Exception
        ###############################################################################
        except Exception as e:
            PDF.STORE_DATA(self,'{}'.format(e), Format=True)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            PDF.STORE_DATA(self,f"Error occured in line number {exc_tb.tb_lineno}", Format=False)
            return e


    def api_call(self):
        start_time = datetime.fromtimestamp(int(time.time()))
        Test_procedure = [f"{'='*100}\nTest case *M_CTC_ID_020* Started!! Status: Running\n{'='*100}",'** Test Coverage **'.center(50),'DHCP/STATIC IP Ping',
                    'Pre Get Filter User Management', 'Netopeer Connection','Capability exchange','Create-subscription filter','Try to Merge new user with nms privilege',
                    'Access denied error', 'Start Time : {}'.format(start_time),'='*100]
        notification('\n'.join(Test_procedure))
        Result = self.Main_Function()
        Configuration.Result_Declartion(self,'Access Control NMS (negative case)',Result, 'M_CTC_ID_020')
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
    obj = M_CTC_ID_020()
    obj.api_call()

