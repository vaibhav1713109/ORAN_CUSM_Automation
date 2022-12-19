import os, sys, xmltodict, xml.dom.minidom, ifcfg
from ncclient import manager
import time,socket,paramiko
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

class MPlane_Configuration():
    def __init__(self,config_data) -> None:
        self.ru_name = config_data['ru_name']
        self.sudo_user = config_data['sudo_user']
        self.sudo_pass = config_data['sudo_pass']
        self.interface_ru = config_data['fh_interface']
        self.du_mac = config_data['du_mac']
        self.ru_mac = config_data['ru_mac']
        self.ru_vlan_id = config_data['ru_vlan_id']
        self.element_name = config_data['element_name']
        self.bandwidth = config_data['bandwidth'][4:-1]
        self.tx_center_freq = config_data['tx_center_frequency']
        self.rx_center_freq = config_data['rx_center_frequency']
        self.tx_arfcn = self.identify_Fref_deltF_Nref(self.tx_center_freq)
        self.rx_arfcn = self.identify_Fref_deltF_Nref(self.rx_center_freq)
        self.duplex_scheme = config_data['duplex_type']
        self.scs_val = config_data['scs_value'][2:-3]
        self.dhcp_server_ip = config_data['dhcp_server_ip']
        self.mplnane_version = config_data['mplnane_version']
        self.gain = config_data['gain']
        self.config_data = config_data
        print(self.ru_name,self.sudo_user,self.sudo_pass,self.interface_ru,self.du_mac,
            self.ru_mac,self.ru_vlan_id,self.element_name,self.bandwidth,self.tx_center_freq, self.rx_center_freq, self.tx_arfcn,
            self.rx_arfcn,self.duplex_scheme,self.scs_val,self.dhcp_server_ip)
    
    def identify_Fref_deltF_Nref(self,Fref):
        Fref = float(Fref)*1000
        if Fref < 3000:        
            FREF_Offs = 0        
            deltaF_Global = 0.005        
            NREF_Offs = 0    
        else:       
            FREF_Offs = 3000        
            deltaF_Global = 0.015        
            NREF_Offs = 600000    
        arfcn = int(NREF_Offs + (Fref-FREF_Offs) / deltaF_Global)
        return str(arfcn)

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
    

    def create_connection(self):
        try:
            session, login_info = self.session_login(USER_N=self.sudo_user,PSWRD=self.sudo_pass)
            print(self.hostname,self.sudo_user,self.sudo_pass)
            print("Connection Established..")
            return session
        except Exception as e:
            print(e)
            try:
                session.close_session()
            except Exception as e:
                print(e)
            return False

    ###############################################################################
    ## Sesssion Login
    ###############################################################################
    def session_login(self,host = '0.0.0.0',USER_N='',PSWRD=''):
        # print(self.hostname,USER_N,PSWRD)
        try:
            session = manager.call_home(host = '0.0.0.0', port=4334, hostkey_verify=False,username = USER_N, password = PSWRD,timeout = 60,allow_agent = False , look_for_keys = False)
            self.hostname, call_home_port = session._session._transport.sock.getpeername()   #['ip_address', 'TCP_Port']
            login_info = f'''> listen --ssh --login {USER_N}
                    Waiting 60s for an SSH Call Home connection on port 4334...
                    Interactive SSH Authentication done.'''.strip()
            
        except Exception as e:
            print(f"session_login Error : {e}")
            warn('Call Home is not initiated!!!!!! So it will try with connect command!!!!')
            # manager.connect(host = '192.168.4.50', port=830, hostkey_verify=False,username = 'root', password = 'vvdn',timeout = 60)
            self.hostname = self.config_data['ru_static_ip']
            session = manager.connect(host = self.hostname, port=830, hostkey_verify=False,username = USER_N, password = PSWRD,timeout = 60)
            server_key_obj = session._session._transport.get_remote_server_key()
            login_info = f'''> connect --ssh --host {self.hostname} --port 830 --login {USER_N}
                    Interactive SSH Authentication done. 
                            '''
        return session, login_info

    ###############################################################################
    ## Sync Check
    ###############################################################################
    def CheckSync(self,session):
        print('Checking Sync of RU')
        start_time = time.time() + 60
        while time.time() < start_time:
            SYNC = '''<filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
            <sync xmlns="urn:o-ran:sync:1.0">
            </sync>
            </filter>
            '''
            data  = session.get(SYNC).data_xml
            dict_Sync = xmltodict.parse(str(data))
            state = dict_Sync['data']['sync']['sync-status']['sync-state']
            x = xml.dom.minidom.parseString(data)
            xml_pretty_str = x.toprettyxml()
            if state == 'LOCKED':
                print('Sync-State "LOCKED" detected!!')
                return True
        else:
            print('Sync-State "UNLOCKED" detected!!')
            return False

    ###############################################################################
    ## add data for interface_xml, processing_xml and uplane_xml
    ###############################################################################
    def add_require_data_into_xmls(self,comptression_format=16):
        n = self.interface_ru[3]
        self.interface_xml = open('{0}/Requirement/Yang_xml/interface.xml'.format(parent)).read()
        self.processing_xml = open('{0}/Requirement/Yang_xml/processing.xml'.format(parent)).read()
        self.uplane_xml = open('{0}/RUs_Info/{1}/uplane.xml'.format(parent,self.ru_name)).read()
        self.interface_xml = self.interface_xml.format(ru_mac=self.ru_mac,interface_name = self.interface_ru,vlan_id = self.ru_vlan_id,number=n)
        self.processing_xml = self.processing_xml.format(ru_mac=self.ru_mac,interface_name = self.interface_ru,element_name=self.element_name,du_mac = self.du_mac,vlan_id = self.ru_vlan_id)
        self.uplane_xml = self.uplane_xml.format(tx_arfcn = self.tx_arfcn, rx_arfcn = self.rx_arfcn, bandwidth = int(float(self.bandwidth)*(10**6)), tx_center_freq = int(float(self.tx_center_freq)*(10**9)), 
                    rx_center_freq = int(float(self.rx_center_freq)*(10**9)), duplex_scheme = self.duplex_scheme,element_name= self.element_name, scs_val = self.scs_val,iq_bitwidth=comptression_format,
                    gain = self.gain)
        print('Append all related data into xml files')
        print(f"""\n
                    ru_mac = {self.ru_mac}
                    interface_name = {self.interface_ru}
                    vlan_id = {self.ru_vlan_id}
                    element_name = {self.element_name}
                    iq_bitwidth={comptression_format}
                    bandwidth = {self.bandwidth}
                    duplex_scheme = {self.duplex_scheme}
                    tx_arfcn = {self.tx_arfcn}
                    tx_center_freq = {self.tx_center_freq}
                    rx_arfcn = {self.rx_arfcn}
                    rx_center_freq = {self.rx_center_freq}
                    """)
        print(self.interface_xml)
        print(self.processing_xml)
        print(self.uplane_xml)

    ###############################################################################
    ## Change the Compression format
    ###############################################################################
    def ChangeCompression(self,session,comptression_format=16):
        try:
            self.add_require_data_into_xmls(comptression_format)
            ###############################################################################
            ## Configure Interface Yang
            ###############################################################################
            print("<Send RPC : Interface>")
            u1 =f'''
                    <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                    {self.interface_xml}
                    </config>'''
            Data = session.edit_config(u1, target='running',default_operation='merge')
            if 'Ok' in str(Data) or 'ok' in str(Data) or 'OK' in str(Data):
                print("<RPC Reply Interface : OK>")
            else:
                print(Data)
                return False
            ###############################################################################
            ## Configure Processing Yang
            ###############################################################################
            u2 =f'''
                    <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                    {self.processing_xml}
                    </config>'''
            
            print("<Send RPC : Processing>")
            Data = session.edit_config(u2, target='running',default_operation='merge')
            if 'Ok' in str(Data) or 'ok' in str(Data) or 'OK' in str(Data):
                print("<RPC Reply Processing : OK>")
            else:
                print(Data)
                return False
            ###############################################################################
            ## Test Procedure 1 : Configure Uplane Yang
            ###############################################################################
            
            XML_DATA = xmltodict.parse(str(self.uplane_xml))
            snippet = f"""
                        <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                        {self.uplane_xml}
                        </config>"""
            
            print("<Send RPC : Uplane>")
            data1 = session.edit_config(target="running", config=snippet, default_operation = 'replace')
            if 'Ok' in str(Data) or 'ok' in str(Data) or 'OK' in str(Data):
                print("<RPC Reply Uplane : OK>")
            else:
                print(Data)
                print("o-ran-uplane configuration didn't configure in O-RU")
                return "o-ran-uplane configuration didn't configure in O-RU"
                                    
            time.sleep(10)
            ###############################################################################
            ## Post Get Filter
            ###############################################################################      
            up ='''
                <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                <user-plane-configuration xmlns="urn:o-ran:uplane-conf:1.0">
                </user-plane-configuration>
                </filter>
                '''
            timeout = time.time() + 60
            while timeout > time.time():
                Cap = session.get(up).data_xml
                x = xml.dom.minidom.parseString(Cap)
                xml_pretty_str = x.toprettyxml()
                USER_PLANE = xmltodict.parse(str(Cap))
                ARFCN_RX1 = USER_PLANE['data']['user-plane-configuration']['rx-array-carriers']['absolute-frequency-center']
                ARFCN_TX1 = USER_PLANE['data']['user-plane-configuration']['tx-array-carriers']['absolute-frequency-center']
                RX_active = USER_PLANE['data']['user-plane-configuration']['rx-array-carriers']['active']
                TX_active = USER_PLANE['data']['user-plane-configuration']['tx-array-carriers']['active']
                RX_state = USER_PLANE['data']['user-plane-configuration']['rx-array-carriers']['state']
                TX_state = USER_PLANE['data']['user-plane-configuration']['tx-array-carriers']['state']

                # self.interface_xml.close()
                # self.processing_xml.close()
                # self.uplane_xml.close()
                # session.close_session()
                ################# Check the ARFCN #################
                if (ARFCN_RX1 == self.rx_arfcn) and (ARFCN_TX1 == self.tx_arfcn):
                    if RX_active == 'ACTIVE' and TX_active == "ACTIVE" and TX_state == "READY" and RX_state == "READY":
                        print("RX Carrier : ", RX_active,RX_state)
                        print("TX Carrier : ", TX_active,TX_state)
                        return True
            else:
                print("RX Carrier : ", RX_active,RX_state)
                print("TX Carrier : ", TX_active,TX_state)
                return False
            

        ###############################################################################
        ## Exception
        ###############################################################################
        except Exception as e:
            print('{}'.format(e),)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(
                f"Error occured in line number {exc_tb.tb_lineno}",)
            return e
    
    ###############################################################################
    ## Check the counter values
    ###############################################################################
    def capture_ru_state(self,host,username,password):
        try:
            port = 22
            command = "cd /etc/scripts/; ./stat_ru.sh"
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(host, port, username, password)
            stdin, stdout, stderr = client.exec_command(command)
            Error = stderr.read().decode()
            if Error:
                return Error, False
            else:
                ru_state = stdout.read().decode()
            return ru_state, True
        except Exception as e:
            time.sleep(5)
            error = f'Check_ru_state Error : {e}'
            print(error)
            return error, False

    ###############################################################################
    ## Verifying ru states weather packets are on time 
    ###############################################################################
    def verify_ru_stat(self):
        print(self.hostname,self.super_user,self.super_user_pass)
        ru_state, status = self.capture_ru_state(self.hostname,self.super_user,self.super_user_pass)
        if status:
            dl_TOTAL_RX_packets_max = 0
            dl_RX_ON_TIME_packets_max = 0
            dl_c_plane_TOTAL_RX_packets_max = 0
            dl_c_plane_RX_ON_TIME_packets_max = 0
            ul_cplane_TOTAL_RX_packets_max = 0
            ul_cplane_RX_ON_TIME_packets_max = 0
            ru_stat = ru_state.split('=============================================================================================')
            dl_counter = ru_stat[3]

            print('========================= RECIEVE COUNTERS DL =============================================')
            for line in dl_counter.split('\n'):
                if 'LAYER' in line:
                    print(line)
                elif 'TOTAL_RX Packets' in line:
                    # print(line)
                    dl_TOTAL_RX_packets = int(line.rsplit(" ",1)[1])
                    if dl_TOTAL_RX_packets > dl_TOTAL_RX_packets_max:
                        dl_TOTAL_RX_packets_max = dl_TOTAL_RX_packets
                    print(f'TOTAL_RX_packets : {dl_TOTAL_RX_packets}') 
                elif 'RX_ON-TIME' in line:
                    # print(line)
                    dl_RX_ON_TIME_packets = int(line.rsplit(" ",1)[1])
                    if dl_RX_ON_TIME_packets > dl_RX_ON_TIME_packets_max:
                        dl_RX_ON_TIME_packets_max = dl_RX_ON_TIME_packets
                    print(f'RX_ON-TIME_packets : {dl_RX_ON_TIME_packets}')
                else:
                    print(line)

            '=========================Receive counter DL C Plane============================================='
            dl_Cplane_counter = ru_stat[4]
            print('=========================Receive counter DL C Plane=============================================')
            for line in dl_Cplane_counter.split('\n'):
                if 'LAYER' in line:
                    print(line)
                elif 'TOTAL_RX Packets' in line:
                    print(line)
                    dl_c_plane_TOTAL_RX_packets = int(line.rsplit(" ",1)[1])
                    # print(f'TOTAL_RX_packets : {dl_c_plane_TOTAL_RX_packets}') 
                    if dl_c_plane_TOTAL_RX_packets > dl_c_plane_TOTAL_RX_packets_max:
                        dl_c_plane_TOTAL_RX_packets_max = dl_c_plane_TOTAL_RX_packets
                elif 'RX_ON-TIME' in line:
                    print(line)
                    dl_c_plane_RX_ON_TIME_packets = int(line.rsplit(" ",1)[1])
                    # print(f'RX_ON-TIME_packets : {dl_c_plane_RX_ON_TIME_packets}') 
                    if dl_c_plane_RX_ON_TIME_packets > dl_c_plane_RX_ON_TIME_packets_max:
                        dl_c_plane_RX_ON_TIME_packets_max = dl_c_plane_RX_ON_TIME_packets
                else:
                    print(line)
                    
            '=========================Receive counter UL C Plane============================================='
            ul_Cplane_counter = ru_stat[5]
            print('=========================Receive counter UL C Plane=============================================')
            for line in ul_Cplane_counter.split('\n'):
                if 'LAYER' in line:
                    print(line)
                elif 'TOTAL_RX Packets' in line:
                    print(line)
                    ul_cplane_TOTAL_RX_packets = int(line.rsplit(" ",1)[1])
                    # print(f'TOTAL_RX_packets : {ul_cplane_TOTAL_RX_packets}') 
                    if ul_cplane_TOTAL_RX_packets > ul_cplane_TOTAL_RX_packets_max:
                        ul_cplane_TOTAL_RX_packets_max = ul_cplane_TOTAL_RX_packets
                elif 'RX_ON-TIME' in line:
                    print(line)
                    ul_cplane_RX_ON_TIME_packets = int(line.rsplit(" ",1)[1])
                    # print(f'RX_ON-TIME_packets : {ul_cplane_RX_ON_TIME_packets}')
                    if ul_cplane_RX_ON_TIME_packets > ul_cplane_RX_ON_TIME_packets_max:
                        ul_cplane_RX_ON_TIME_packets_max = ul_cplane_RX_ON_TIME_packets
                else:
                    print(line)

            '=========================Check Wether on-time packets are more then 95% of total packets================================'
            if dl_RX_ON_TIME_packets_max < (dl_TOTAL_RX_packets_max*95)//100 or ((dl_RX_ON_TIME_packets_max == 0)):
                print(f'dl_RX_ON_TIME_packets {dl_RX_ON_TIME_packets_max} are less then 95% of dl_TOTAL_RX_packets {dl_TOTAL_RX_packets_max}')
            else:
                print('DL Counter packets are on time..')
            if dl_c_plane_RX_ON_TIME_packets_max < (dl_c_plane_TOTAL_RX_packets_max*95)//100 or dl_c_plane_RX_ON_TIME_packets_max == 0:
                print(f'dl_c_plane_RX_ON_TIME_packets {dl_c_plane_RX_ON_TIME_packets_max} are less then 95% of dl_c_plane_TOTAL_RX_packets {dl_c_plane_TOTAL_RX_packets_max}')
            else:
                print('DL C Plane packets are on time..')
            if ul_cplane_RX_ON_TIME_packets_max < (ul_cplane_TOTAL_RX_packets_max*95)//100 or ul_cplane_RX_ON_TIME_packets_max == 0:
                print(f'ul_cplane_RX_ON_TIME_packets {ul_cplane_RX_ON_TIME_packets_max} are less then 95% of ul_cplane_TOTAL_RX_packets {ul_cplane_TOTAL_RX_packets_max}')
                return False
            else:
                print('DL C Plane packets are on time..')
            return True
        else:
            print(ru_state)
            return False




if __name__ == "__main__":
    ########################################################################
    ## For reading data from .ini file
    ########################################################################
    configur = ConfigParser()
    configur.read('{}/Requirement/inputs.ini'.format(parent))
    information = configur['INFO']
    comp = sys.argv[1]
    obj1 = MPlane_Configuration(information)
    # obj1.add_require_data_into_xmls()
    connection = obj1.create_connection()
    if connection:
        obj1.CheckSync(connection)
        print(obj1.ChangeCompression(connection,comp))
    else:
        print('Can\'t create netopeer connection!!')
    # 'obj1.hostname,obj1.super_user,obj1.super_user_pass'
    # obj1.verify_ru_stat()