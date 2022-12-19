import configparser, threading
from ncclient import manager, operations
from ncclient.operations import RPCError
from ncclient.operations import rpc
from ncclient.xml_ import to_ele
from ncclient.operations.errors import TimeoutExpiredError
from ncclient.operations.rpc import RPCError
from ncclient.transport.errors import SessionCloseError
from ncclient.transport import errors
import xml.etree.ElementTree as ET
from lxml import etree
import xml.dom.minidom
import xmltodict
import time
import sys
import os
import subprocess

# Directory Path
cwd = os.path.dirname(os.path.abspath(__file__))

config_file = configparser.ConfigParser()
config_file.read('{}/../inputs.ini'.format(cwd))
print('{}/../inputs.ini'.format(cwd))


class ru_control:
    def __init__(self) -> None:
        self.get_interface = '''<filter xmlns = "urn:ietf:params:xml:ns:netconf:base:1.0">
        <interfaces xmlns = "urn:ietf:params:xml:ns:yang:ietf-interfaces">
        </interfaces>
        </filter>'''

        self.get_processing = '''<filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <processing-elements xmlns="urn:o-ran:processing-element:1.0">
        </processing-elements>
        </filter>'''

        self.get_uplane = '''<filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <user-plane-configuration xmlns="urn:o-ran:user-plane-configuration:1.0">
        </user-plane-configuration>
        </filter>'''

        self.get_sync = '''<filter xmlns = "urn:ietf:params:xml:ns:netconf:base:1.0">
        <sync xmlns = "urn:o-ran:sync:1.0">
        </sync>
        </filter>'''

        self.get_hardware = '''<filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <hardware xmlns="urn:ietf:params:xml:ns:yang:ietf-hardware">
        </hardware>
        </filter>'''

        self.subscribe_pm = '''<filter type="xpath" xmlns="urn:ietf:params:xml:ns:netconf:notification:1.0" xmlns:pm="urn:o-ran:performance-management:1.0" select="/pm:*"/>'''
        self.host = config_file.get('RUNNING', 'possible_ip')
        self.username = config_file.get('INFO', 'sudo_user')
        self.password = config_file.get('INFO', 'sudo_pass')
        self.interface = config_file.get('INFO', 'fh_interface')
        self.vlan = '100'
        self.RU_MAC = config_file.get('INFO', 'ru_mac')
        self.DU_MAC = config_file.get('CUPlane', 'du_mac')
        self.ARFCN_DL = config_file.get('INFO', 'tx_arfcn')
        self.ARFCN_UL = config_file.get('INFO', 'rx_arfcn')
        self.dl_freq = int(float(config_file.get('INFO', 'tx_center_frequency'))*10**9)
        self.ul_freq = int(float(config_file.get('INFO', 'tx_center_frequency'))*10**9)
        self.dl_bw = int(float(config_file.get('INFO', 'bandwidth'))*10**6)
        self.ul_bw = int(float(config_file.get('INFO', 'bandwidth'))*10**6)
        self.SCS = config_file.get('INFO', 'scs_value')
        self.num_prb = "273"
        self.element_name = config_file.get('INFO', 'element_name')
        self.ip_dhcp_interface = config_file.get('INFO', 'ip_dhcp_interface')
        self.remote_file_path = 'sftp://{0}@{1}:22/home/{0}/'.format(self.username,self.ip_dhcp_interface)
        self.sftp_pass = config_file.get('INFO', 'sftp_pass')
        pub_k = subprocess.getoutput('cat /etc/ssh/ssh_host_rsa_key.pub')
        pk = pub_k.split()
        self.public_key = pk[1]

    def NP_Connection(self):
        try:
            connection = manager.connect(
                host=self.host, port=830, username=self.username, password=self.password, hostkey_verify=False)
            print("NP_Connection Status : Connection Established")
            return connection, True

        except Exception as e:
            print(f"NP_Connection Error : Failed to establish connection: {e}")
            return "NP_Connection Error : Failed to establish connection: {e}" ,False

    def get_filter_command(self, connection, filter_str):
        try:
            result = connection.get(filter_str)
            xml_data = result.data_xml
            dom = xml.dom.minidom.parseString(xml_data)
            xml_object = dom.toprettyxml(indent="  ")
            return xml_object
        except Exception as e:
            print(f"get_filter_command Error : Failed to execute 'get' command: {e}")
            return False

    def edit_config_command(self, connection, xml_data, operation):
        try:
            print("Netopeer Connection Established : ", connection.connected)
            result = connection.edit_config(target='running', config=xml_data, default_operation=operation)
            print(result)
            print(f"edit_config_command Status : Configuration {operation} successfully.")
            return True
        except RPCError as e:
            rpc_error_element = etree.ElementTree(e.xml)
            rpc_error = etree.tostring(rpc_error_element).decode()
            rpc_error = xml.dom.minidom.parseString(rpc_error).toprettyxml()
            print(f"edit_config_command RPC Error : {rpc_error}")
            return rpc_error
        except Exception as e:
            print(f"edit_config_command Error : Failed to {operation} configuration: {e}")
            return False

    def read_xml_for_a_leaf(self, xml_object, complex_element_name, leaf_name):
        root = ET.fromstring(xml_object)
        content_list = []
        for complex_element in root.iter():
            if len(list(complex_element)) > 0 and complex_element.tag.endswith(complex_element_name):
                for element in complex_element.iter():
                    if element.tag.endswith(leaf_name):
                        content_list.append(element.text)
            # if complex_element.tag.endswith(leaf_name):
            #         content_list.append(complex_element.text)
        return content_list
    
    def read_counter_values(self,xml_object):
        root = ET.fromstring(xml_object)
        content_list = {}
        dict_data  = xmltodict.parse(xml_object)
        measurement_stats = dict_data['notification']['measurement-result-stats']['rx-window-stats']
        if type(measurement_stats) == list:
            for stat in measurement_stats:
                measurement_object = stat['measurement-object']
                eaxc_measured_result = stat['eaxc-measured-result']
                for eaxcid in eaxc_measured_result:
                    count = eaxcid['count']
                    eaxc_id = eaxcid['eaxc-id']
                    if not content_list.get(eaxc_id):
                        content_list[eaxc_id] = measurement_object.ljust(40) +  f": {count}"
                    else:
                        content_list[eaxc_id] = content_list[eaxc_id] + '\n' + measurement_object.ljust(40) +  f": {count}"
        else:
            measurement_object = measurement_stats['measurement-object']
            eaxc_measured_result = measurement_stats['eaxc-measured-result']
            for eaxcid in eaxc_measured_result:
                count = eaxcid['count']
                eaxc_id = eaxcid['eaxc-id']
                if not content_list.get(eaxc_id):
                    content_list[eaxc_id] = measurement_object.ljust(40) +  f": {count}"
                else:
                    content_list[eaxc_id] = content_list[eaxc_id] + '\n' + measurement_object.ljust(40) +  f": {count}"
        return content_list

    def ru_configuration(self, connection):
        try:
            saperator = '='*60
            print(f"{saperator}\nReading xml file for interface")
            interface_xml = open(f'{cwd}/interface.xml').read()
            interface_xml = interface_xml.format(interface=self.interface, vlan=self.vlan,
                                                 RU_MAC=self.RU_MAC)
            print(f"After replacing interface xml\n{saperator}", interface_xml)
            print("{}\nReading xml file for process element".format(saperator))
            pro_element = open(f'{cwd}/processing.xml').read()
            process_element_xml = pro_element.format(interface=self.interface, vlan=self.vlan,
                                                     RU_MAC=self.RU_MAC, DU_MAC=self.DU_MAC)
            print(f"After replacing processing element xml\n{saperator}", process_element_xml)
            print("{}\nReading xml file for uplane-configuration".format(saperator))
            uplane_xml = open(f'{cwd}/uplane.xml').read()
            uplan_xml = uplane_xml.format(ARFCN_DL=self.ARFCN_DL, ARFCN_UL=self.ARFCN_UL,
                                          dl_freq=self.dl_freq, dl_bw=self.dl_bw, ul_freq=self.ul_freq,
                                          ul_bw=self.ul_bw, SCS=self.SCS, num_prb=self.num_prb, element_name=self.element_name)
            print(f"after replacing uplane-configuration xml\n{saperator}", uplan_xml)
            print(f"{saperator}\nConfiguring Interface.yang || In progress\n{saperator}")
            print("Netopeer Connection Established : ", connection.connected)
            interface_status = self.edit_config_command(connection, interface_xml, 'merge')
            # result=self.get_filter_command(connection, self.get_interface)
            if (interface_status == True):
                print(saperator)
                print("Configuring Interface.yang || Complete")
                print("Configuring processing.yang || In progress")
                print(saperator)
                processing_status = self.edit_config_command(connection, process_element_xml, 'replace')
                if processing_status == True:
                    print("Configuring processing.yang || Complete")
                    print("Configuring uplane.yang || In progress")
                    print(saperator)
                    uplane_status = self.edit_config_command(connection, uplan_xml, 'replace')
                    get_res = self.get_filter_command(connection, self.get_uplane)
                    print(get_res)
                    if uplane_status == True:
                        print(saperator)
                        print("Configuring Uplane.yang || Complete")
                        print(saperator)
                        return True

                    else:
                        print("INFO Error : Not able to execute the UPLANE xml")
                        return "INFO Error : Not able to execute the UPLANE xml"
                else:
                    print("INFO Error : Not able to execute the processing elsement xml")
                    return "INFO Error : Not able to execute the processing elsement xml"
            else:
                print("INFO Error : Not able to execute the interface xml")
                return "INFO Error : Not able to execute the interface xml"

        except Exception as e:
            print(
                f"INFO Error : Failed to execute 'RU_configutaion' command: {e}")
            return f"INFO Error : Failed to execute 'RU_configutaion' command: {e}"

    def check_counters(self,connection):
        timeout = time.time()+90
        while time.time() < timeout:
            n = connection.take_notification(timeout=90)
            notify = n.notification_xml
            x = xml.dom.minidom.parseString(notify)
            xml_pretty_str = x.toprettyxml()
            measurement_object = self.read_counter_values(xml_pretty_str)
            for key,val in measurement_object.items():
                print(f"Eaxc-id : {key}".center(100,'-'))
                print(val)

    def read_counters(self, connection):
        subscribe_pm = '''<filter type="xpath" xmlns="urn:ietf:params:xml:ns:netconf:notification:1.0" xmlns:pm="urn:o-ran:performance-management:1.0" select="/pm:*"/>'''
        subs = connection.create_subscription(filter=subscribe_pm)
        print('='*50)
        print('RU is subscribed for performance counter')
        print('='*50)
        performance_xml_act = open(f'{cwd}/performance_act.xml').read()
        performance_xml_act = performance_xml_act.format(
            remote_file_path=self.remote_file_path, pd=self.sftp_pass, public_key=self.public_key)
        print("after replacing performance xml\n", performance_xml_act)
        performance_res = self.edit_config_command(
            connection, performance_xml_act, 'replace')
        if(performance_res == True):
            print('='*50)
            self.check_counters(connection)
            print('='*50)
            performance_xml_deact = open(f'{cwd}/performance_deact.xml').read()
            performance_xml_deact = performance_xml_deact.format(
                remote_file_path=self.remote_file_path, pd=self.sftp_pass, public_key=self.public_key)
            print("after replacing performance xml\n", performance_xml_act)
            performance_deact_res = self.edit_config_command(connection, performance_xml_deact, 'replace')
            if performance_deact_res != True:
                Error = f"read_counters error : Failed to edit the xml\n {performance_deact_res}"
                return Error
            print("success")
        else:
            Error = f"read_counters error : Failed to edit the xml\n {performance_res}"
            return Error

    def ru_sync_and_oper_state(self, connection):
        sync = self.get_filter_command(connection, self.get_sync)
        state = self.get_filter_command(connection, self.get_hardware)
        timeout = time.time()+180
        if sync and state:
            sync_state = 'UNLOCKED'
            hw_oper_state = 'disabled'
            while time.time() < timeout:
                sync_state = self.read_xml_for_a_leaf(sync, 'sync-status', 'sync-state')
                # print('sync-state :',sync_state)
                ptp_lock_state = self.read_xml_for_a_leaf(sync, 'ptp-status', 'lock-state')
                # print('ptp-lock-state :',ptp_lock_state)
                synce_lock_state = self.read_xml_for_a_leaf(sync, 'synce-status', 'lock-state')
                print('synce-lock-state :', synce_lock_state)
                hw_oper_state = self.read_xml_for_a_leaf(state, 'state', 'oper-state')
                # print('hw-oper-state :',hw_oper_state)
                if 'LOCKED' in sync_state and 'enabled' in hw_oper_state:
                    print('='*60)
                    print(f"sync-state : {sync_state} \nhw-oper-state : {hw_oper_state}")
                    print('='*60)
                    return True
            else:
                print('='*60)
                print(
                    f"sync-state : {sync_state} \nhw-oper-state : {hw_oper_state}")
                print('='*60)
                return False
        else:
            print("sync state is not locked and oper-state is not enabled")
            print(f"ru_sync_and_oper_state error : \n{sync} \n\n{state}")
            return False

    def close_connection(connection):
        try:
            connection.close_session()
            print("Connection closed successfully.")
        except Exception as e:
            print(f"Failed to close connection: {e}")


if __name__ == "__main__":
    ru_obj = ru_control()
    connection = ru_obj.NP_Connection()
    if connection[-1] == True:
        sync_status = ru_obj.ru_sync_and_oper_state(connection[0])
        if sync_status!=True:
            print(sync_status)
            sys.exit(1000)
        # print(connection[0].connected)
        conf_status = ru_obj.ru_configuration(connection[0])
        if conf_status!=True:
            print(conf_status)
            sys.exit(10000)
        #ru_obj.read_counters(connection)
