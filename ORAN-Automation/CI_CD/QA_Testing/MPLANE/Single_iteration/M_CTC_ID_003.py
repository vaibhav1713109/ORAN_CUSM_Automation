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
 * @file     M_CTC_ID_003.py
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
import ifcfg, sys, os, time, subprocess, socket, xmltodict
from ncclient import manager
from ncclient.operations.rpc import RPCError
from paramiko.ssh_exception import NoValidConnectionsError
from ncclient.transport import errors
from  ncclient.transport.errors import TransportError, SSHUnknownHostError
from tabulate import tabulate
from scapy.all import *
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
from Single_iteration.vlan_scan import *

###############################################################################
## Initiate PDF
###############################################################################

class Transport_and_Handshake_in_IPv4_Environment_negative_case_3_1_1_2_flow_2(vlan_scan):

    def __init__(self):
        super().__init__()

    def add_test_description_and_software_detail(self,ethtool_cmd,ethtool_out,ping_output):
        try:
            netopeer_connection.session_login(self,timeout=60,username=self.username,password=self.password)
            if self.session :
                    Test_Desc = '''Test Description : This scenario validates that the O-RU properly executes the session establishment procedure with VLANs and a DHCPv4 server. This test is applicable to IPv4 environments. Two negative flows are included in this test:
        The TER NETCONF Client uses improper credentials when trying to establish a SSH session with the RU NETCONF Server.'''
                    Result = netopeer_connection.add_test_description(self,Test_Description=Test_Desc, Test_Case_name='Transport_and_Handshake_in_IPv4_Environment_negative_case_3_1_1_2_flow_2')
                    if len(Result) > 2:
                        self.running_sw, self.running_false_sw, self.inactive_slot = Result[0], Result[1], Result[2]

                    self.STORE_DATA('{}'.format(ethtool_cmd).center(100),Format=True,)
                    self.STORE_DATA(ethtool_out,Format=False)
                    self.STORE_DATA('{}'.format("ping -c 5 {}".format(self.hostname)).center(100),Format=True,)
                    self.STORE_DATA(ping_output,Format=False)
                    self.fingerprint = self.login_info.split('\n')[3].rsplit(' ',1)[-1]
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
    ## Performing Call home
    ###############################################################################
    def Call_Home(self,user,pswrd):
        try:
            LISTEN = f'''> listen --ssh --login {user }\nWaiting 60s for an SSH Call Home connection on port 4334...'''
            PDF.STORE_DATA(self,LISTEN,Format=False)
            SSH_AUTH = f'''The authenticity of the host '::ffff:{self.hostname}' cannot be established.
                ssh-rsa key fingerprint is {self.fingerprint}.
                Are you sure you want to continue connecting (yes/no)? yes'''
            PDF.STORE_DATA(self,SSH_AUTH,Format=False)
            PDF.STORE_DATA(self,f'''\n{user }@::ffff:{self.hostname} password: \n''',Format=False)
            self.session_1 = netopeer_connection.call_home(self,host='', port=4334, username=user , hostkey_verify=False, password=pswrd, timeout = 60,allow_agent = False , look_for_keys = False)
            print(self.session_1.session_id)
            self.session_1.close_session()
            return 'Call Home initiated!!'
            
        
            
        ###############################################################################
        ## Exception
        ###############################################################################
        except errors.AuthenticationError as e:
            print(e)
            s = f'''nc ERROR: Unable to authenticate to the remote server (all attempts via supported authentication methods failed).
            cmd_listen: Receiving SSH Call Home on port 4334 as user "{user}" failed.'''
            Configuration.append_data_and_print(self,f"Authentication fail for {user} with wrong credential || successful.")
            PDF.STORE_DATA(self,s,Format=False)
            return '{}'.format(e)
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            PDF.STORE_DATA(self,f"Error occured in line number {exc_tb.tb_lineno}",Format=False)
            PDF.STORE_DATA(self,'{}'.format(e),Format=False)
            return e



    ########################### Main Function ############################
    def Main_Function(self):
        
        Output = Configuration.Link_detction_and_check_ping(self)
        if Output[-1]!=True:
            return Output[0]
        self.hostname = Output[-2]

        
        self.username = configur.get('INFO','sudo_user')
        self.password = configur.get('INFO','sudo_pass')
        try:
            self.add_test_description_and_software_detail(Output[2],Output[0],Output[1])
            time.sleep(10)
            netopeer_connection.delete_system_log(self,host= self.hostname)   

                
            ############################### DU Side Interfaces #############################
            PDF.STORE_DATA(self,"\t Interfaces Present in DU Side",Format=True)
            ip_config = subprocess.getoutput('ifconfig')
            PDF.STORE_DATA(self,ip_config,Format='XML')

            PDF.add_page(self)
            ############################### DHCP Status #############################
            st = subprocess.getoutput('sudo /etc/init.d/isc-dhcp-server status')
            PDF.DHCP_Status(self,data=st)



            PDF.add_page(self)
            hs = {'observer':'admin1234','operator':'4647dn','installerr':'wireless1234','installer':'admin','operator1':'admin123'}
            Test_Step1 = '\tThe O-RU NETCONF Serve  establishes TCP connection and performs a Call Home procedure towards the NETCONF Client and not establishes a SSH.'
            PDF.STORE_DATA(self,'{}'.format(Test_Step1),Format='TEST_STEP')

            results = []
            for key, val in hs.items():
                try:
                    res = self.Call_Home(key,val)
                # except TransportError as e:
                #     self.session_1.close_session()
                finally:
                    try:
                        self.session_1.close_session()
                    except Exception as e:
                        print(e)
                    time.sleep(10)
                PDF.STORE_DATA(self,'{}\n'.format('-'*100),Format=False)
                if "AuthenticationException" in str(res):
                    Flag = True
                    results.append(Flag)
                else:
                    return res
            return True

                    


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
        Test_procedure = [f"{'='*100}\nTest case *Reject_SSH_Authentication_due_to_Incorrect_Credential* Started!! Status: Running\n{'='*100}",'** Test Coverage **'.center(50),
                    'Ping the DHCP IP assign to Vlan','Perform Call Home repeatedly and reject SSH Authentication','Capability exchange', 'Start Time : {}'.format(start_time)]
        notification('\n'.join(Test_procedure))
        Result = self.Main_Function()
        Configuration.Result_Declartion(self,'Reject_SSH_Authentication_due_to_Incorrect_Credential',Result, 'Transport_and_Handshake_in_IPv4_Environment_negative_case_3_1_1_2_flow_2')
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
        else:
            return True
    

if __name__ == "__main__":
    obj = Transport_and_Handshake_in_IPv4_Environment_negative_case_3_1_1_2_flow_2()
    obj.api_call()



