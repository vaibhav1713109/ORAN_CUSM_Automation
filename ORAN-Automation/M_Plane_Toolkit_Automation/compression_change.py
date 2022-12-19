import json
import subprocess
import time
import paramiko
import glob
import os,sys
from configparser import ConfigParser

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
configur.read('{}/Requirement/inputs.ini'.format(parent))


class MPlaneConfiguration():
    def __init__(self) -> None:
        self.ru_name = configur.get('INFO','ru_name')
        self.super_user = configur.get('INFO','super_user')
        self.super_user_pass = configur.get('INFO','super_user_pass')
        self.interface_ru = configur.get('INFO','fh_interface')
        self.du_mac = configur.get('INFO','du_mac')
        self.ru_mac = configur.get('INFO','ru_mac')
        self.ru_vlan_id = configur.get('INFO','ru_vlan_id')
        self.element_name = configur.get('INFO','element_name')
        self.bandwidth = configur.get('INFO','bandwidth')
        self.tx_center_freq = configur.get('INFO','tx_center_frequency')
        self.rx_center_freq = configur.get('INFO','rx_center_frequency')
        self.tx_arfcn = configur.get('INFO','tx_arfcn')
        self.rx_arfcn = configur.get('INFO','rx_arfcn')
        self.duplex_scheme = configur.get('INFO','duplex_type')
        self.scs_val = configur.get('INFO','subcarrier_spacing')
        self.hostname = configur.get('INFO','RU_IP')
        self.dhcp_server_ip = configur.get('INFO','dhcp_server_ip')


    def write_json(self,new_data, filename='C:\\ProgramData\\Keysight\\MPlane\\Client\\duprofile\\v2\\client_config.json'):
        with open(filename,'w') as file:
            json.dump(new_data, file, indent = 4)
            
    def configure_client_config_json(self):
        print('Configuring Client.json file for making mplane connection.')
        with open ("C:\\ProgramData\\Keysight\\MPlane\\Client\\duprofile\\v2\\client_config.json") as json_file:
            data=json.load(json_file)
            temp=data["general"]
            x= {"call-flow-xml": ["compression_change.xml"], "fail_call_home": "False", "username": self.super_user, "password": self.super_user_pass, "tls-hostname": self.super_user,}
            temp.update(x)
        self.write_json(data)
        print('Configuring complete for Client.json file.')

    def configure_compression(self,comp=16):
        file1 = open('{}/Scripts/compression_change.xml'.format(parent)).read()
        file2 = open('{0}/Requirement/Yang_xml/interface.xml'.format(parent)).read()
        file3 = open('{0}/Requirement/Yang_xml/processing.xml'.format(parent)).read()
        file4 = open('{0}/RUs_Info/{1}/uplane.xml'.format(parent,self.ru_name)).read()
        file2 = file2.format(ru_mac=self.ru_mac,interface_name = self.interface_ru,vlan_id = self.ru_vlan_id)
        file3 = file3.format(ru_mac=self.ru_mac,interface_name = self.interface_ru,element_name=self.element_name,du_mac = self.du_mac,vlan_id = self.ru_vlan_id)
        file4 = file4.format(element_name=self.element_name,iq_bitwidth=comp,bandwidth = self.bandwidth,duplex_scheme = self.duplex_scheme,tx_arfcn=self.tx_arfcn,tx_center_freq = self.tx_center_freq,rx_arfcn=self.rx_arfcn,rx_center_freq = self.rx_center_freq)
        file1 = file1.format(interface = file2,processing=file3,uplane=file4)
        file5 = open('C:\\ProgramData\\Keysight\\MPlane\\Client\\duprofile\\v2\\MC_TC_026.xml', 'w')
        file5 = file5.writelines(file1)
        print('Append all related data into xml files')
        print(f"""\n
                    ru_mac = {self.ru_mac}
                    interface_name = {self.interface_ru}
                    vlan_id = {self.ru_vlan_id}
                    element_name = {self.element_name}
                    iq_bitwidth={comp}
                    bandwidth = {self.bandwidth}
                    duplex_scheme = {self.duplex_scheme}
                    tx_arfcn = {self.tx_arfcn}
                    tx_center_freq = {self.tx_center_freq}
                    rx_arfcn = {self.rx_arfcn}
                    rx_center_freq = {self.rx_center_freq}
                    """)

    def run_mplane_toolkit(self):
        time.sleep(2)

        subprocess.run(f"MPlaneClient.bat --ip {self.dhcp_server_ip} --duprofile duprofile\\v2 --ruprofile ruprofile\\v2", shell=True)

        time.sleep(2)
        pass


if __name__ == "__main__":
    obj = MPlaneConfiguration()
    obj.configure_client_config_json()
    obj.configure_compression(comp=14)
    obj.run_mplane_toolkit()
    print("\n********************EXECUTED********************\n")

    pass