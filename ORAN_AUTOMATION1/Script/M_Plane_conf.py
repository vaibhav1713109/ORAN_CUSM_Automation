import os, sys, xmltodict, xml.dom.minidom, ifcfg
from ncclient import manager
import time,socket
import logging
from warnings import warn
from configparser import ConfigParser
logger = logging.getLogger('ncclient.manager')

###############################################################################
## Directory Path
###############################################################################
dir_name = os.path.dirname(os.path.abspath(__file__))
parent = os.path.dirname(dir_name)
print(parent)
sys.path.append(parent)

########################################################################
## For reading data from .ini file
########################################################################
configur = ConfigParser()
configur.read('{}/inputs.ini'.format(parent))

class MPlaneConfiguration:
    def __init__(self) -> None:
        try:
            self.super_user = configur.get('INFO','super_user')
            self.super_user_pass = configur.get('INFO','super_user_pass')
            self.interface_ru = configur.get('INFO','fh_interface')
            self.interface_du = configur.get('INFO','du_interface')
            self.element_name = configur.get('INFO','element_name')
            self.tx_arfcn = configur.get('INFO','tx_arfcn')
            self.rx_arfcn = configur.get('INFO','rx_arfcn')
            self.bandwidth = configur.get('INFO','bandwidths')
            self.tx_center_freq = configur.get('INFO','downlink_frequency')
            self.rx_center_freq = configur.get('INFO','uplink_frequency')
            self.duplex_scheme = configur.get('INFO','duplex_type')
            self.scs_val = configur.get('INFO','subcarrier_spacing')
            self.ru_mac = ''
            self.du_mac = ifcfg.interfaces()[self.interface]['ether']
            self.session, self.login_info = self.session_login(self.super_user,self.super_user_pass)
        except Exception as e:
            print(e)


    def CheckSync(self):
        start_time = time.time() + 1200
        while time.time() < start_time:
            SYNC = '''<filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
            <sync xmlns="urn:o-ran:sync:1.0">
            </sync>
            </filter>
            '''
            data  = self.session.get(SYNC).data_xml
            dict_Sync = xmltodict.parse(str(data))
            state = dict_Sync['data']['sync']['sync-status']['sync-state']
            x = xml.dom.minidom.parseString(data)
            xml_pretty_str = x.toprettyxml()
            if state == 'LOCKED':
                print('Sync-State "LOCKED" detected!!')
                return True
        else:
            print(xml_pretty_str)
            return False


    def call_home(*args, **kwds):
        host = kwds["host"]
        port = kwds.get("port",4334)
        timeout = kwds["timeout"]
        srv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv_socket.bind((host, port))
        srv_socket.settimeout(timeout)
        srv_socket.listen()

        sock, remote_host = srv_socket.accept()
        logger.info('Callhome connection initiated from remote host {0}'.format(remote_host))
        kwds['sock'] = sock
        srv_socket.close()
        return manager.connect_ssh(*args, **kwds)
    
    ###############################################################################
    ## Sesssion Login
    ###############################################################################
    def session_login(self,host = '0.0.0.0',USER_N = '',PSWRD = ''):
        try:
            session = self.call_home(host = '0.0.0.0', port=4334, hostkey_verify=False,username = USER_N, password = PSWRD,timeout = 60,allow_agent = False , look_for_keys = False)
            hostname, call_home_port = session._session._transport.sock.getpeername()   #['ip_address', 'TCP_Port']
            login_info = f'''> listen --ssh --login {USER_N}
                    Waiting 60s for an SSH Call Home connection on port 4334...
                    Interactive SSH Authentication done.'''.strip()
            
        except Exception as e:
            warn('Call Home is not initiated!!!!!! So it will try with connect command!!!!')
            session = manager.connect(host = host, port=830, hostkey_verify=False,username = USER_N, password = PSWRD,timeout = 60,allow_agent = False , look_for_keys = False)
            server_key_obj = session._session._transport.get_remote_server_key()
            login_info = f'''> connect --ssh --host {host} --port 830 --login {USER_N}
                    Interactive SSH Authentication done. 
                            '''
        return session, login_info

    ###############################################################################
    ## Change the Compression format
    ###############################################################################
    def ChangeCompression(self,comptression_format=16):
        try:
            ###############################################################################
            ## Fetch Mac address of RU fronhaul Interface
            ###############################################################################
            v_name1 = '''
                    <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                    </interfaces>
                    </filter>
            '''
            interface_name = self.session.get_config('running', v_name1).data_xml
            dict_interface = xmltodict.parse(str(interface_name))
            Interfaces = dict_interface['data']['interfaces']['interface']
            d = {}
            ma = {}

            
            for i in Interfaces:
                if i['name'] == self.interface_ru:
                    self.ru_mac = i['mac-address']['#text']
                    break
            
            else:
                return 'Give correct name of RU fronthaul interface!!'

            ###############################################################################
            ## Configure Interface Yang
            ###############################################################################
            n = self.interface_ru[3]
            xml_data = open('{}/Requirement/Yang_xml/interface.xml'.format(parent)).read()
            xml_data = xml_data.format(interface_name= self.interface_ru,mac = self.ru_mac, number= n)
            u1 =f'''
                    <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                    {xml_data}
                    </config>'''
            Data = self.session.edit_config(u1, target='running')
            
            ###############################################################################
            ## Configure Processing Yang
            ###############################################################################
            xml_data1 = open('{}/Requirement/Yang_xml/processing.xml'.format(parent)).read()
            xml_data1 = xml_data1.format(int_name= self.interface_ru,ru_mac = self.ru_mac, du_mac = self.du_mac, element_name= self.element_name)
            u2 =f'''
                    <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                    {xml_data1}
                    </config>'''
            Data = self.session.edit_config(u2, target='running')

            ###############################################################################
            ## Test Procedure 1 : Configure Uplane Yang
            ###############################################################################        
            Test_Step1 = "STEP 1 The TER NETCONF Client assigns unique eAxC_IDs to low-level-rx-endpoints. The same set of eAxC_IDs is also assigned to low-level-tx-endpoints. The TER NETCONF Client uses <rpc><editconfig>."
            print('{}'.format(Test_Step1))
            
            print('> edit-config  --target running --config --defop replace')
            print('******* Replace with below xml ********')
            
            
            xml_1 = open('{}/Requirement/Yang_xml/uplane.xml'.format(parent)).read()
            xml_1 = xml_1.format(tx_arfcn = self.tx_arfcn, rx_arfcn = self.rx_arfcn, bandwidth = int(float(self.bandwidth)*(10**6)), tx_center_freq = int(float(self.tx_center_freq)*(10**9)), 
                    rx_center_freq = int(float(self.rx_center_freq)*(10**9)), duplex_scheme = self.duplex_scheme,element_name= self.element_name, scs_val = self.scs_val)
            XML_DATA = xmltodict.parse(str(xml_1))
            snippet = f"""
                        <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                        {xml_1}
                        </config>"""
                        
            print(snippet)
            data1 = self.session.edit_config(target="running", config=snippet, default_operation = 'replace')
            print("Configuring o-ran-user-plane yang!!")
                                    

            ###############################################################################
            ## Post Get Filter
            ###############################################################################   
            print('################# Post get filter #################')
            print('> get --filter-xpath /o-ran-uplane-conf:user-plane-configuration')
                
            up ='''
                <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                <user-plane-configuration xmlns="urn:o-ran:uplane-conf:1.0">
                </user-plane-configuration>
                </filter>
                '''
            Cap = self.session.get(up).data_xml
            x = xml.dom.minidom.parseString(Cap)
            xml_pretty_str = x.toprettyxml()
            USER_PLANE = xmltodict.parse(str(Cap))
            ARFCN_RX1 = USER_PLANE['data']['user-plane-configuration']['rx-array-carriers']['absolute-frequency-center']
            ARFCN_TX1 = USER_PLANE['data']['user-plane-configuration']['tx-array-carriers']['absolute-frequency-center']

            # self.session.close_session()
            ################# Check the ARFCN #################
            if (ARFCN_RX1 == self.rx_arfcn) and (ARFCN_TX1 == self.tx_arfcn):
                print("o-ran-user-plane yang configured successfully!!")
                return True
            else:
                return "o-ran-uplane configuration didn't configure in O-RU"
            

        ###############################################################################
        ## Exception
        ###############################################################################
        except Exception as e:
            print('{}'.format(e),)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(
                f"Error occured in line number {exc_tb.tb_lineno}",)
            return e
    