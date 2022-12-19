###############################################################################
##@ FILE NAME:      M_CTC_ID_035
##@ TEST SCOPE:     M PLANE O-RAN CONFORMANCE
##@ Version:        V_1.0.0
##@ Support:        @Ramiyer, @VaibhavDhiman, @PriyaSharma
###############################################################################

###############################################################################
## Package Imports 
###############################################################################

import sys, os, time, xmltodict, xml.dom.minidom, lxml.etree, ifcfg, socket
from lxml import etree
from ncclient import manager
from ncclient.operations.rpc import RPC, RPCError
from ncclient.transport import errors
from paramiko.ssh_exception import NoValidConnectionsError
from ncclient.operations.errors import TimeoutExpiredError
from ncclient.transport.errors import SessionCloseError
from ncclient.xml_ import to_ele
from configparser import ConfigParser
from scapy.all import *

###############################################################################
## Directory Path
###############################################################################
dir_name = os.path.dirname(os.path.abspath(__file__))
parent = os.path.dirname(dir_name)
# print(parent)
root_dir = parent.rsplit('/',1)[0]
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



class M_CTC_ID_035(PDF,Configuration,netopeer_connection,genrate_pdf_report):
   
    # init method or constructor 
    def __init__(self):
        PDF.__init__(self)
        netopeer_connection.__init__(self)
        Configuration.__init__(self)
        genrate_pdf_report.__init__(self)
        PDF.PDF_CAP(self)
        self.file_notification = None
        self.error = None
        self.filename = None
        self.summary = []
        self.rmt = ''
        self.sftp_pass = ''
        self.super_user = configur.get('INFO', 'super_user')
        self.super_pass = configur.get('INFO', 'super_pass')

    
    def login_with_another_session_for_file_upload(self,filter=None,cmd = ''):
        try:
            with manager.connect(host = self.hostname, port=830, hostkey_verify=False,username = self.username, password = self.password,timeout = 60,allow_agent = False , look_for_keys = False) as root_session:
                ###############################################################################
                ## Check Notification for troubleshoot
                ###############################################################################
                print(cmd)
                print(filter)
                create_subscription = root_session.create_subscription(filter=filter)
                if 'ok' in str(create_subscription) or 'Ok' in str(create_subscription) or 'OK' in str(create_subscription):
                    Configuration.append_data_and_print(self,f"create_subscription || Ok")
                t = time.time() + 30
                while time.time() < t:
                    n = root_session.take_notification(timeout = 30)
                    if n == None:
                        break
                    notify = n.notification_xml
                    print("notification : ",notify)
                    x = xml.dom.minidom.parseString(notify)
                    xml_pretty_str = x.toprettyxml()
                    if 'file-upload' in notify:
                        xml_pretty_str = x.toprettyxml()
                        PDF.STORE_DATA(self,'{}'.format(xml_pretty_str), Format='XML')
                        if 'SUCCESS' in notify:
                            Configuration.append_data_and_print(self,f'file-upload || Success')
                            self.file_notification = xml_pretty_str
                        else:
                            Configuration.append_data_and_print(self,f'file-upload || Failed')
                            self.file_notification = xml_pretty_str
                            self.error = f'file-upload Failed'
                        return
                print("xml_pretty_str : ",xml_pretty_str)
                if len(xml_pretty_str) == 0 or xml_pretty_str == None:
                    self.error = f'Notification captured for file upload || Fail'
                    return
        ###############################################################################
        ## Exceptions
        ###############################################################################
        except RPCError as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            if exc_tb:
                PDF.STORE_DATA(self,f"Error occured in line number {exc_tb.tb_lineno}", Format=False)
            rpc_error_element = etree.ElementTree(e.xml)
            rpc_error = etree.tostring(rpc_error_element).decode()
            rpc_error = xml.dom.minidom.parseString(rpc_error).toprettyxml()
            PDF.STORE_DATA(self,rpc_error,Format='XML')
            # print(rpc_error)
            self.error = rpc_error
    
        except Exception as e:
            PDF.STORE_DATA(self,'{}'.format(e), Format=True)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            PDF.STORE_DATA(self,f"Error occured in line number {exc_tb.tb_lineno}", Format=False)
            print(f"login_with_another_session_for_file_upload Error : {e}")
            self.error = f"login_with_another_session_for_file_upload Error : {e}"
        
        finally:
            try:
                root_session.close_session()
            except Exception as e:
                print(f"login_with_another_session_for_file_upload Error : {e}")


    def check_troublehoot_file(self):
        pass

    ###############################################################################
    ## Test Procedure
    ###############################################################################
    def test_execution(self,cmd,ethtool_out,ping_output):
        try:
            netopeer_connection.session_login(self,timeout=60,username=self.username,password=self.password)
            if self.session :
                Configuration.append_data_and_print(self,'Netopeer Connection || Successful')
                Test_Desc = '''This scenario is MANDATORY for both O-RU and O-DU Tests.
                                This test validates the capability of the O-RU to upload trace logs.
                                This scenario corresponds to the following chapters in [3]:
                                11.2.2 Trace'''
                Result = netopeer_connection.add_test_description(self,Test_Description=Test_Desc, Test_Case_name='M_CTC_ID_035')
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
                filter = """<filter type="xpath" xmlns="urn:ietf:params:xml:ns:netconf:notification:1.0" xmlns:trace="urn:o-ran:trace:1.0" select="/trace:*"/>"""
                cmd = '> subscribe --filter-xpath /o-ran-trace:*'
                netopeer_connection.create_subscription(self,filter=filter,cmd=cmd)
                
                ###############################################################################
                ## Configure start-trace RPC
                ###############################################################################
                trace_xml = """<start-trace-logs xmlns="urn:o-ran:trace:1.0">
                                    </start-trace-logs>
                                """
                Configuration.append_data_and_print(self,'Configure Trace RPC || In Progresss')
                Test_Step1 = '''\t\t The TER NETCONF Client sends <rpc><start-trace-logs> to the O-RU NETCONF Server. The O-RU
                        NETCONF Server responds with <rpc-reply>< trace-status-grouping >.'''
                PDF.STORE_DATA(self,'{}'.format(Test_Step1),Format='TEST_STEP')

                rpc_reply = self.send_rpc(rpc_data=trace_xml)
                if rpc_reply != True:
                    Configuration.append_data_and_print(self,'Configure Trace RPC || Fail')
                    return rpc_reply
                Configuration.append_data_and_print(self,'Configure Trace RPC || Pass')
                

                Test_Step2 = '''\t\t The O-RU NETCONF Server starts generating one or more file(s) containing trace logs. When the
                                generation of the log file(s) are completed, the O-RU NETCONF Server sends <notification><trace-log-
                                generated> and <is-notification-last> set as false with a list of one or more log file names to the TER
                                NETCONF Server.'''
                PDF.STORE_DATA(self,'{}'.format(Test_Step2),Format='TEST_STEP')
                Configuration.append_data_and_print(self,'Waiting 15 min for trace notification || In Progresss')
                time.sleep(870)

                ###############################################################################
                ## Captured trace notification after 15 min
                ###############################################################################
                notif = self.session.take_notification(block=True,timeout = 60)
                notify = notif.notification_xml
                print(notify)
                x = xml.dom.minidom.parseString(notify)
                xml_pretty_str = x.toprettyxml()
                if 'trace-log-generated' in notify and 'is-notification-last>false' in notify:
                    filename_string = xmltodict.parse(str(xml_pretty_str))
                    self.filename = filename_string['notification']['trace-log-generated']['log-file-name']
                    self.filename = "/"+self.filename.split('p4')[-1]
                    PDF.STORE_DATA(self,'{}'.format(xml_pretty_str), Format='XML')
                    Configuration.append_data_and_print(self,f'Notification captured for trace || Success')
                else:
                    PDF.STORE_DATA(self,'{}'.format(xml_pretty_str), Format='XML')
                    Configuration.append_data_and_print(self,f'Notification captured for trace || Fail')
                    return f'Notification captured for trace || Fail'
                
                pub_k = subprocess.getoutput('cat /etc/ssh/ssh_host_rsa_key.pub')
                pk = pub_k.split()
                pub_key = pk[1]
                ###############################################################################
                ## Configure file upload rpc w.r.t genrated trace file
                ###############################################################################   
                file_upload_xml = open("{}/require/Yang_xml/TC_34.xml".format(parent)).read()
                file_upload_xml = file_upload_xml.format(rmt_path=self.rmt,password=self.sftp_pass,pub_key= pub_key,t_logs = self.filename)
                Configuration.append_data_and_print(self,'Configure file-upload RPC || In Progresss')
                Test_Step3 = '''\t\t The TER NETCONF Client sends <rpc><file-upload>log-file-name</file-upload></rpc> to the O-RU
                            NETCONF Server to start uploading the log file(s). The O-RU NETCONF Server responds with <rpc-
                            reply><file-upload> with status SUCCESS.'''
                PDF.STORE_DATA(self,'{}'.format(Test_Step3),Format='TEST_STEP')


                ###### Make a thread for reading the notifications ######
                file_filter = """<filter type="xpath" xmlns="urn:ietf:params:xml:ns:netconf:notification:1.0" xmlns:file="urn:o-ran:file-management:1.0" select="/file:*"/>"""
                cmd = '> subscribe --filter-xpath /o-ran-file-management:*'
                t1 = threading.Thread(target=self.login_with_another_session_for_file_upload,kwargs={'filter':file_filter,'cmd' : cmd})
                t1.start()
                time.sleep(5)
                rpc_reply = self.send_rpc(rpc_data=file_upload_xml)
                if rpc_reply != True:
                    Configuration.append_data_and_print(self,'Configure file-upload RPC || Fail')
                    return rpc_reply
                
                Configuration.append_data_and_print(self,'Configure file-upload RPC || Success')
                t1.join(timeout=20)
                print(self.error)
                if self.error != None:
                    return self.error
                

                ###############################################################################
                ## Configure stop-trace rpc
                ###############################################################################   
                trace_xml = """<stop-trace-logs xmlns="urn:o-ran:trace:1.0">
                                    </stop-trace-logs>
                                """
                Configuration.append_data_and_print(self,'Configure stop-Trace RPC || In Progresss')
                Test_Step5 = '''\t\t The TER NETCONF Client sends <rpc><stop-trace-logs> to the O-RU NETCONF Server. The O-RU
                        NETCONF Server responds with <rpc-reply>< trace-status-grouping >.'''
                PDF.STORE_DATA(self,'{}'.format(Test_Step5),Format='TEST_STEP')

                rpc_reply = self.send_rpc(rpc_data=trace_xml)
                if rpc_reply != True:
                    Configuration.append_data_and_print(self,'Configure stop-Trace RPC || Fail')
                    return rpc_reply
                Configuration.append_data_and_print(self,'Configure stop-Trace RPC || Pass')
                

                Test_Step6 = '''\t\t The TER NETCONF Client can wit for te otification from the O-RU NETCONF Server. The O-RU
                        NETCONF Server sends <notificaton> and set<is-notification-last> to true.'''
                PDF.STORE_DATA(self,'{}'.format(Test_Step6),Format='TEST_STEP')

                ###############################################################################
                ## Captured trace notification
                ###############################################################################
                notif = self.session.take_notification(block=True,timeout = 60)
                notify = notif.notification_xml
                x = xml.dom.minidom.parseString(notify)
                xml_pretty_str = x.toprettyxml()
                if 'trace-log-generated' in notify and 'is-notification-last>true' in notify:
                    filename_string = xmltodict.parse(str(xml_pretty_str))
                    self.filename = filename_string['notification']['trace-log-generated']['log-file-name']
                    self.filename = "/"+self.filename.split('p4')[-1]
                    PDF.STORE_DATA(self,'{}'.format(xml_pretty_str), Format='XML')
                    Configuration.append_data_and_print(self,f'Notification captured for stop-trace || Success')
                else:
                    PDF.STORE_DATA(self,'{}'.format(xml_pretty_str), Format='XML')
                    Configuration.append_data_and_print(self,f'Notification captured for trace || Fail')
                    return f'Notification captured for stop-trace || Fail'
                
                ###############################################################################
                ## Configure file upload rpc w.r.t genrated trace file
                ###############################################################################   
                file_upload_xml = open("{}/require/Yang_xml/TC_34.xml".format(parent)).read()
                file_upload_xml = file_upload_xml.format(rmt_path=self.rmt,password=self.sftp_pass,pub_key= pub_key,t_logs = self.filename)
                Configuration.append_data_and_print(self,'Configure file-upload RPC || In Progresss')
                Test_Step7 = '''\t\t The TER NETCONF Client sends <rpc><file-uload>lg-file-name</file-upload></rpc> to the O-RU
                        NETCONF Server to start uploading the remainng logfile(s). The O-RU NETCONF Server responds
                        with <rpc-reply><file-upload> with status SUCESS'''
                PDF.STORE_DATA(self,'{}'.format(Test_Step7),Format='TEST_STEP')


                ###### Make a thread for reading the notifications ######
                file_filter = """<filter type="xpath" xmlns="urn:ietf:params:xml:ns:netconf:notification:1.0" xmlns:file="urn:o-ran:file-management:1.0" select="/file:*"/>"""
                cmd = '> subscribe --filter-xpath /o-ran-file-management:*'
                t1 = threading.Thread(target=self.login_with_another_session_for_file_upload,kwargs={'filter':file_filter,'cmd' : cmd})
                t1.start()
                time.sleep(5)
                rpc_reply = self.send_rpc(rpc_data=file_upload_xml)
                if rpc_reply != True:
                    Configuration.append_data_and_print(self,'Configure file-upload RPC || Fail')
                    return rpc_reply
                
                Configuration.append_data_and_print(self,'Configure file-upload RPC || Success')
                t1.join(timeout=30)
                print(self.error)
                if self.error != None:
                    return self.error
                return True

        ###############################################################################
        ## Check Access Denied
        ###############################################################################
        except RPCError as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            if exc_tb:
                PDF.STORE_DATA(self,f"Error occured in line number {exc_tb.tb_lineno}", Format=False)
            rpc_error_element = etree.ElementTree(e.xml)
            rpc_error = etree.tostring(rpc_error_element).decode()
            rpc_error = xml.dom.minidom.parseString(rpc_error).toprettyxml()
            PDF.STORE_DATA(self,rpc_error,Format='XML')
            # print(rpc_error)
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
    ## Main Function
    ###############################################################################
    def Main_Function(self):
        Output = Configuration.Link_detction_and_check_ping(self)
        if Output[-1]!=True:
            return Output[0]
        self.hostname = Output[-2]
        test_server_ip_format='.'.join(self.hostname.split('.')[:-1])+'.'
        self.sftp_server_ip = Configuration.test_server_10_interface_ip(self,ip_format=test_server_ip_format)

        ###############################################################################
        ## Read User Name and password from Config.INI of Config.py
        ###############################################################################
        self.sftp_user = configur.get('INFO','sftp_user')
        self.sftp_pass = configur.get('INFO','sftp_pass')
        self.rmt = 'sftp://{0}@{1}:22/home/{0}'.format(self.sftp_user,self.sftp_server_ip)

        try:
            time.sleep(10)
            netopeer_connection.delete_system_log(self,host= self.hostname)
            Result = self.test_execution(Output[2],Output[0],Output[1])
            return Result
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
        Test_procedure = [f"{'='*100}\nTest case *Trace Test* Started!! Status: Running\n{'='*100}",'** Test Coverage **'.center(50),'DHCP/Static IP Ping',
                'Netopeer Connection','Capability exchange','Create-subscription','Configure Start Trace RPC', 'Upload genrated log file to remote', 'Start Time : {}'.format(start_time),'='*100]
        notification('\n'.join(Test_procedure))
        Result = self.Main_Function()
        Configuration.Result_Declartion(self,'Trace Test ',Result, 'M_CTC_ID_035')
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
    obj = M_CTC_ID_035()
    obj.api_call()


