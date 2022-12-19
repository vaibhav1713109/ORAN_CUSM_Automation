from ncclient import manager,operations
from ncclient.operations import RPCError
from ncclient.operations import rpc
from ncclient.xml_ import to_ele
from ncclient.operations.errors import TimeoutExpiredError
from ncclient.operations.rpc import RPCError
from ncclient.transport.errors import SessionCloseError
from ncclient.transport import errors
import subprocess, ifcfg,pyvisa
import re
import configparser
import paramiko
import time
import sys,os
import ipaddress
import pexpect
import xml.etree.ElementTree as ET
import xml.dom.minidom
import xmltodict
from configparser import ConfigParser

#root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

############################################### Geting Params #########################################
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(root_dir, "re_init.py")
configur = ConfigParser()
configur.read('{}/inputs.ini'.format(root_dir))

###$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$  Get_interfcae  $$$$$$$$$$$$$$$$$$$$$$$$$$$#
dhcp_interface = configur.get('INFO','du_fh_interface')
# dhcp_interface = "enp3s0"
###**************************************************************************#

###$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$  Get_mplane_specific  $$$$$$$$$$$$$$$$$$$$$#
oran_usr = configur.get('INFO','sudo_user')
oran_pass = configur.get('INFO','sudo_pass')
static_dynamic = configur.get('INFO','static_dynamic')

var1 = '''<filter xmlns = "urn:ietf:params:xml:ns:netconf:base:1.0">
<interfaces xmlns = "urn:ietf:params:xml:ns:yang:ietf-interfaces">
</interfaces>
</filter>'''
###***************************************************************************#
###$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$  Get_RU_specific  $$$$$$$$$$$$$$$$$$$$$$$$$#
IP_DHCP_interface = '192.168.4.15'
ru_name = configur.get('INFO','ru_name')
ru_key = configur.get('INFO','ru_key')
tx_freq = float(configur.get('INFO','tx_center_frequency'))*1000
rx_freq = float(configur.get('INFO','rx_center_frequency'))*1000
waiting_time = configur.get('INFO','wait_time')
wait_time = int(waiting_time)
###****************************************************************************#
###$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$  Get_Running_config $$$$$$$$$$$$$$$$$$$$$$$#
init_status = configur.get('RUNNING','init_state')
###*****************************************************************************#
###$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$  Get_Telnet_config $$$$$$$$$$$$$$$$$$$$$$$#
Telnet_ip = configur.get('INFO', 'static_ip')
Telnet_portid = configur.get('Telnet', 'port_id')
Telnet_username = configur.get('Telnet', 'telnet_user')
Telnet_password = configur.get('Telnet', 'telnet_password')
###******************************************************************************#
###$$$$$$$$$$$$$$$$$$$$$$$$$$  Get_PowerSupply_config $$$$$$$$$$$$$$$$$$$$$$$#
is_RPS_Or_Kiku = configur.get('PowerCycle','rps_kikusui')
if "RPS" in is_RPS_Or_Kiku:
    rps_switch_ip = configur.get('PowerCycle','rps_switch_ip')
    rps_switch_user = configur.get('PowerCycle','rps_switch_user')
    rps_switch_pass = configur.get('PowerCycle','rps_switch_pass')
    rps_switch_port = configur.get('PowerCycle','rps_switch_port')
else:
    Kiku_visa_addrs = configur.get('PowerCycle','Kiku_visa_addrs')
###******************************************************************************#
############################################### Geting Params #########################################
tx_freq = float(configur.get('INFO','tx_center_frequency'))*1000
rx_freq = float(configur.get('INFO','rx_center_frequency'))*1000


############################## Telnet Codes for LPRU ########################################################

def send_and_receive_telnet_commands(child, command):
    child.sendline(command)
    child.expect('CLI:/>')
    output = child.before.decode().strip()
    return output

def Telnet_connection(host_ip, port_id, username, password):
    child = pexpect.spawn(f'telnet {host_ip} {port_id}')
    child.expect('Username :')
    child.sendline(username)
    child.expect('Password :')
    child.sendline(password)
    child.expect('CLI:/>')
    return child

def read_output_for_matching_string(output, match_string):
    lines = output.split('\n')
    for line in lines:
        if match_string in line:
            return True
    return False

def configure_via_telenet(Dynamic_or_static,host_ip, port_id, username, password):
    try:
        child = Telnet_connection(host_ip, port_id, username, password)
        iface_status = send_and_receive_telnet_commands(child, 'get-IfaceStatus')
        match_string = 'dhcp'
        if read_output_for_matching_string(iface_status, match_string):
            if "Dynamic" in Dynamic_or_static:
                child.sendline('exit')
                return True
            else:
                child.sendline('set-Ipv4Static 192.168.4.50 255.255.255.0 192.168.4.1')
                print("RU_Configured in Static")
                return True
        else:
            if "Dynamic" in Dynamic_or_static:
                child.sendline('set-IfaceDhcp')
                print("RU is configured Dynamic.... Need to wait some time")
                return True
            else:
                child.sendline('exit')
                return True
    except Exception as e:
        print(f'Error : {e}')
        return False

################################# Telnet Codes for LPRU ########################################################

################################# Check for DHCP configs   #####################################################

class initialisation():
    def __init__(self) -> None:
        self.high_speed_interface = None
        self.dhcp_interface = None
        self.HighSpeed_interface_Vlans = None
        self.dhcp_interface_IP = None
   
    def find_high_speed_interface(self):
        self.high_speed_interface = dhcp_interface
        cmd = f"cat /sys/class/net/{self.high_speed_interface}/speed"
        result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = result.communicate()
        if error:
            print(f"Error: {error.decode().strip()}")
        speed = output.decode().strip()
        if speed in ["10000", "25000"]:
            return True
        else:
            print(f"{self.high_speed_interface} : {speed}")
            return False
        
    def check_ping_status(self,ip_address):
        response = subprocess.Popen(f"ping -c 5 {ip_address}", shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = response.communicate()
        Response = stdout.decode()
        pattern = '[1-5] received'
        ans  = re.search(pattern,Response)
        if ans:
            print(f'check_ping_status Error : Ping Obtained to {ip_address}')
            return True
        else:
            print(f'check_ping_status Error : Ping is not Obtained to {ip_address}')
            return False
      
    def get_interfcae_configured_with_DHCP_Server(self):
        command = """awk -F'=' '/^INTERFACESv4=/ { gsub(/"/, "", $2); print $2 }' /etc/default/isc-dhcp-server"""
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        if process.returncode == 0:
            interface_name = output.decode().strip()
            self.dhcp_interface = interface_name
            return True
        else:
            error_message = error.decode().strip()
            print("Not able to get the interace name configured with DHCP Server")
            return False

    def delete_Vlan_interfaces(self,vlans):
        for interface in vlans:
            cmd = f"sudo ip link delete dev {interface}"
            result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            _, error = result.communicate()
            if error:
                print(f"Error deleting VLAN interface {interface}: {error.decode().strip()}")
                return False
            else:
                print(f"Deleted VLAN interface: {interface}")
        self.find_all_vlan_interfaces_in_CICD_server(self.high_speed_interface)
        return True
              
    def find_all_vlan_interfaces_in_CICD_server(self,hs_interf):
        cmd = f"ls /proc/net/vlan/ | grep '{hs_interf}'"
        result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = result.communicate()
        if "No such file or directory" not in error.decode().strip():
            print(f"Error: {error.decode().strip()}")
            self.HighSpeed_interface_Vlans = None
            return False
        vlan_interfaces = output.decode().strip().split('\n')
        if (len(vlan_interfaces) == 1) and (vlan_interfaces[0] == ''):
            self.HighSpeed_interface_Vlans = None
            return True
        else:
            self.HighSpeed_interface_Vlans = vlan_interfaces
            print("The vlans created with Base Interfaces are : ",self.HighSpeed_interface_Vlans)
            self.delete_Vlan_interfaces(self.HighSpeed_interface_Vlans)
            return True  
                        
    def is_DHCP_server_RUNNING(self):
        cmd = "sudo systemctl status isc-dhcp-server.service"
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if "Active: active (running)" in out.decode():
            return True
        else:
            return False
            
    def find_IP_of_DHCP_interface(self,interface):
        self.dhcp_interface_IP = ifcfg.interfaces()[interface]['inet4']
        
    def assign_ip_for_dhcp_interface(self,interface, ip_address):
        if ifcfg.interfaces()[interface]['inet4'][0] == ip_address:
            print(f"IP address {ip_address} to interface {interface} already assigned")
        else:
            command = f"ip addr add {ip_address} dev {interface}"
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            _, error = process.communicate()
            if process.returncode == 0:
                print(f"Assigned IP address {ip_address} to interface {interface}")
                self.dhcp_interface_IP = ip_address
                return True
            else:
                print(f"Failed to assign IP address {ip_address} to interface {interface}. Error: {error.decode().strip()}")
                return False
            
    def restart_dhcp_server(self):
        cmd = "sudo systemctl restart isc-dhcp-server.service"
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        if stderr:
            print(f"Failed to restart DHCP server: {stderr.decode()}")
            return False
        print(f"Restart the dhcp server.")
        return True

    def edit_dhcp_interface_name(self,dhcp_interface):
        try:
            file_path = '/etc/default/isc-dhcp-server'
            with open(file_path, 'r') as dhcp_file:
                lines = dhcp_file.readlines()
            for i, line in enumerate(lines):
                if line.startswith('INTERFACESv4='):
                    if dhcp_interface in line and f"{dhcp_interface}." not in line:
                        return True
                    else:
                        new_line = line.replace(line,line.strip()[:-1]+f' enp3s0f0"')
                        lines[i] = new_line
                        break
            with open(file_path, 'w') as dhcp_file:
                dhcp_file.writelines(lines)
            return True
        except:
            print("Failed to edit DHCP interface in DHCP server Config file")
            return False
       
    def edit_dhcpd_conf(self):
        try:
            ip_address = ifcfg.interfaces()[self.high_speed_interface]['inet']
            print(ip_address)
            file = open(f'{root_dir}/MPLANE/DATA/DHCPD_CONF.txt', 'r')
            lines = file.readlines()
            hex_ip = '{:02X}:{:02X}:{:02X}:{:02X}'.format(*map(int,ip_address.split('.'))) 
            subnet = '{}.0'.format(ip_address.rsplit('.',1)[0])
            ############################################ Chnage ip address for vlan scanning ############################################
            for i, line in enumerate(lines):
                # print(i)
                if 'domain-name-servers' in line:
                    new_domain = 'option domain-name-servers {}.{}.{}.{};\n'.format(*map(str,ip_address.split('.')))
                    lines[i] = new_domain
                if 'vendor-encapsulated-options 81:' in line:
                    new_vendor_option = f'\toption vendor-encapsulated-options 81:04:{hex_ip};\n'
                    lines[i] = new_vendor_option
                if 'subnet' in line:
                    if subnet  in line:
                        flag = True
                        break
                    else: 
                        flag = False
            ############################################ ADD Subnet for reterive ip details ############################################
            if flag == False:
                new_subnet = '''[subnet {0}.0 netmask 255.255.255.0 {{
                pool {{
                        allow members of "o-ran-ru";
                        allow members of "o-ran-ru2";
                        range {0}.57 {0}.97 ;

                }}
                pool {{
                        deny members of "o-ran-ru";
                        deny members of "o-ran-ru2";
                        range {0}.6 {0}.56 ;
                }}
                option routers {1};
                option broadcast-address {0}.255;
                option subnet-mask 255.255.255.0;
                option interface-mtu 1500;
                }}]'''
                new_sub = new_subnet.format(ip_address.rsplit('.',1)[0],ip_address)
                lines.append(new_sub)
            file.close()
            file1 = open('/etc/dhcp/dhcpd.conf', 'w+')
            file1.writelines(lines)
            file1.close()
            print(f"Editing interface name in dhcpd conf file complete.")
            return True
        except Exception as e:
            print(f'edit_dhcpd_conf Error : {e}')
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(f"Error occured in line number {exc_tb.tb_lineno}")
            print("Failed to edit DHCP ip and subnet in DHCP Config file")
            return False

    def run_dhcp_for_base_interface(self):
        if not self.get_interfcae_configured_with_DHCP_Server():
            return False
        if self.dhcp_interface != self.high_speed_interface:
            if not self.edit_dhcp_interface_name(self.high_speed_interface):
                return False
        if not self.edit_dhcpd_conf():
            return False
        if not self.restart_dhcp_server():
            return False
        return True

    def initialisation_for_dhcp(self,ip_address):
        link_detection = self.find_high_speed_interface()
        if not link_detection:
            return False
        print("The 10G/25G interface present in the server = ",self.high_speed_interface)
        if ifcfg.interfaces()[self.high_speed_interface]['inet'] == None:
            if not self.assign_ip_for_dhcp_interface(self.high_speed_interface,ip_address):
                return False
        vlan_status = self.find_all_vlan_interfaces_in_CICD_server(self.high_speed_interface)
        if not vlan_status:
            return False
        print(f"Editing interface name in isc-dhcp serevr and dhcp config to Base Interface : {self.high_speed_interface}")
        if not self.run_dhcp_for_base_interface():
            return False
        return True


def check_interfaces(object_init,IP_dhcp_interf):
    interface_status = object_init.find_high_speed_interface()
    if interface_status != True:
        print(f"Initialisation Failed --> Interface {object_init.high_speed_interface} not have 10g/25g speed... Aborting")
        return False
    print("The 10G/25G interface present in the server = ",object_init.high_speed_interface)
    object_init.get_interfcae_configured_with_DHCP_Server()
    if object_init.dhcp_interface == None:
        print("Initialisation Failed --> DHCP Server Interface not identified... Aborting")
        return False
    print("The interface configured with DHCP server conf file = ",object_init.dhcp_interface)
    object_init.find_all_vlan_interfaces_in_CICD_server(object_init.high_speed_interface)
    if object_init.HighSpeed_interface_Vlans != None:
        print("The vlans created with Base Interfaces are : ",object_init.HighSpeed_interface_Vlans)
        if not object_init.delete_Vlan_interfaces(object_init.HighSpeed_interface_Vlans):      
            print("not able to delete vlan interfaces")
        print("The vlan interfaces associated with Base Interfaces are deleted")
    # object_init.get_interface_names()
    if object_init.high_speed_interface not in object_init.dhcp_interface:
        print("Editing interface name in dhcp config to Base Interface")
        if object_init.edit_dhcp_interface_name(object_init.high_speed_interface):
            object_init.get_interfcae_configured_with_DHCP_Server()
            if object_init.high_speed_interface in object_init.dhcp_interface:
                print("Edited DHCP interface name")
            else:
                print("Initialisation Failed due to interface name change... Aborting")
                return False
    else:
        print("Interface name configured with DHCP server conf file is the High Speed interface itself")
    dhcp_status = object_init.is_DHCP_server_RUNNING()
    if not dhcp_status:
        object_init.find_IP_of_DHCP_interface(object_init.high_speed_interface)
        print(object_init.dhcp_interface_IP)
        if object_init.dhcp_interface_IP == None:
            object_init.assign_ip_for_dhcp_interface(object_init.high_speed_interface,IP_dhcp_interf)
            if object_init.dhcp_interface_IP == None:
                print("Initialisation Failed --> IP can't assigned to DHCP interface... Aborting")
                return False
        if not object_init.restart_dhcp_server():
            print("Initialisation Failed --> Not able to re-start DHCP Service... Aborting")
            return False
        return True
    if object_init.is_DHCP_server_RUNNING():
        print("DHCP Server is RUNNING...")
        return True
 
def RU_PowerCycle_via_RPS():
    # Turn off O-RU
    command_off = ["curl", "-u", f"{rps_switch_user}:{rps_switch_pass}", f"http://{rps_switch_ip}/rps?SetPower={rps_switch_port}+0"]
    process_off = subprocess.Popen(command_off, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output_off, error_off = process_off.communicate()    
    if f"SetPower = {rps_switch_port} 0 : SUCCESS" in output_off.decode():
        print("RU Powered Off")
    else:
        return False
    time.sleep(7)
    # Turn on O-RU
    command_on = ["curl", "-u", f"{rps_switch_user}:{rps_switch_pass}", f"http://{rps_switch_ip}/rps?SetPower={rps_switch_port}+1"]
    process_on = subprocess.Popen(command_on, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output_on, error_on = process_on.communicate()    
    if f"SetPower = {rps_switch_port} 1 : SUCCESS" in output_on.decode():
        print("RU Powered On")
    else:
        return False
    return True
    
def RU_PowerCycle_via_Kiku():
    # resource_manager = pyvisa.ResourceManager()

    # # Replace 'TCPIP0::192.168.1.100::inst0::INSTR' with your power supply's VISA resource string
    # power_supply = resource_manager.open_resource(Kiku_visa_addrs)

    # try:
    #     # Send power off command
    #     power_supply.write('OUTP OFF')
    #     time.sleep(15)

    #     # Send power on command
    #     a = power_supply.write('OUTP ON')
    #     print(a)
    #     time.sleep(2)  # Wait for a moment before turning off


    #     print("Power supply turned OFF and ON successfully.")

    # except Exception as e:
    #     print("An error occurred:", str(e))

    # finally:
    #     power_supply.close()
    #     resource_manager.close()
    return True

def is_valid_ip_address(ip):
    pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    match = re.match(pattern, ip)    
    return match is not None
    
def is_valid_mac_address(mac):
    pattern = r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"
    match = re.match(pattern, mac)    
    return match is not None
    
def fetch_dhcp_IP_and_MAC_of_RU(interfc,ru_key):
    ip_list=[]
    mac_list=[]
    command = f"sudo systemctl status isc-dhcp-server.service | grep 'via {interfc}' | grep '{ru_key}' | grep 'DHCPACK on'"
    # print(command)
    time.sleep(10)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        print(f"An error occurred: {error.decode()}")
        return None
    dhcp_msgs = output.decode().split('\n')
    print(len(dhcp_msgs[:-1]))
    if len(dhcp_msgs[:-1]) == 0:
        return "fetch_dhcp_IP_and_MAC_of_RU Error : Fetching of IP address and mac address is not completed...", False
    print(dhcp_msgs[:-1])
    ip_pattern = '(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    mac_patter = '(?:[0-9a-fA-F]:?){12}'
    ip_list = list(re.findall(ip_pattern,dhcp_msgs[-2]))
    mac_list = list(re.findall(mac_patter,dhcp_msgs[-2]))
    msgs = [msg.strip() for msg in dhcp_msgs if msg.strip()]
    if len(ip_list) == len(mac_list) != 0:
        return ip_list,mac_list
    else:
        return "fetch_dhcp_IP_and_MAC_of_RU Error : Fetching of IP address and mac address is not completed...", False

def NP_Connection(host):
    try:
        device = manager.connect(host=host, port=830, username=oran_usr, password=oran_pass, hostkey_verify=False)
        print("Connection Established")
        return device

    except Exception as e:
        print(f"Failed to establish connection: {e}")
        return None

def get_filter_command(connection, filter_str):
    try:
        result = connection.get(filter_str)
        xml_data = result.data_xml
        return xml_data
    except Exception as e:
        print(f"Failed to execute 'get' command: {e}")
        return None

def read_xml_for_a_leaf(xml_object, complex_element_name, leaf_name):
    root = ET.fromstring(xml_object)
    content_list = []
    for complex_element in root.iter():
        if len(list(complex_element)) > 0 and complex_element.tag.endswith(complex_element_name):
            for element in complex_element:
                if element.tag.endswith(leaf_name):
                    content_list.append(element.text)
    return content_list

def close_connection(connection):
    try:
        connection.close_session()
        print("Connection closed successfully.")
    except Exception as e:
        print(f"Failed to close connection: {e}")

def get_interface_informations_from_RU(ru_ip):
    try:
        is_ping = init.check_ping_status(ru_ip)
        if is_ping:
            print("connecting to the netopeer")
            NPC = NP_Connection(ru_ip)
            if NPC:
                get_res=get_filter_command(NPC, var1)
                if(get_res):
                    dom = xml.dom.minidom.parseString(get_res)
                    xml_object = dom.toprettyxml(indent="  ")
                    print(xml_object)
                    result_interf = read_xml_for_a_leaf(xml_object,'interface','name')
                    print(result_interf)
                    result_mac= read_xml_for_a_leaf(xml_object,'interface','phys-address')
                    print(result_mac)
                    result_ip=read_xml_for_a_leaf(xml_object,'address', 'ip')
                    print(result_ip)
                    zip_list = list(zip(result_interf,result_mac,result_ip))
                    print(zip_list)
                    for ip_set in zip_list:  
                        if ru_ip in ip_set:
                            print(ip_set)
                            append_to_ini_file('{}/inputs.ini'.format(root_dir),'RUNNING',{'possible_ip':ru_ip})
                            append_to_ini_file('{}/inputs.ini'.format(root_dir),'INFO',{'fh_interface':ip_set[0],'ru_mac':ip_set[1]})
                            return True
                    else:
                        error = f"get_interface_informations_from_RU Error : Failed to get fronthaul interface and mac"
                        return error
                else:
                    error = f"get_interface_informations_from_RU Error : Failed to execute 'get' command"
                    return error

            else:
                error = "get_interface_informations_from_RU Error : Connection to NETCONF server failed."
                return error
        else:
            error =  f"Ping is not obtained --> with Possible Ru IP {ru_ip}....restarting RU to fetch Possible IP"
            return error
    except Exception as e:
        error = f"get_interface_informations_from_RU Error : Failed to execute 'get' command: {e}"
        return error

def check_ping_to_static_IP(ip_address):
    response = subprocess.Popen(f"ping -c 5 {ip_address}", shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = response.communicate()
    Response = stdout.decode()
    pattern = '[1-5] received'
    ans  = re.search(pattern,Response)
    if ans:
        print(f'Ping Obtained to {ip_address}')
        return True
    else:
        print(f'Ping is not Obtained to {ip_address}')
        return False   

def append_to_ini_file(filename, section, data):
    config = configparser.ConfigParser()    
    if not os.path.isfile(filename):
        print(f"INI file '{filename}' does not exist.")
        return 404    
    config.read(filename)
    if not config.has_section(section):
        print(f"Section '{section}' is not present in the config file.")
        return 407
    try:
        for key, value in data.items():
            if config.has_option(section, key):
                config.remove_option(section, key)
            config.set(section, key, value)
        with open(filename, "w") as config_file:
            config.write(config_file)
        print("Data appended to INI file successfully.")
        return 0
    except Exception as e:
        print(f'append_to_ini_file Error : {e}')
        return 507
        
def identify_Fref_deltF_Nref(Fref):
    if Fref < 3000:
        FREF_Offs = 0
        deltaF_Global = 0.005
        NREF_Offs = 0
    else:
        FREF_Offs = 3000
        deltaF_Global = 0.015
        NREF_Offs = 600000
    return FREF_Offs,deltaF_Global,NREF_Offs

if __name__ == "__main__":
    if "Not_initialised" in init_status:
        TelnetRus = ["LPRU","BND28"]
        if any(item in ru_name for item in TelnetRus) and static_dynamic== 'Static': #No need of Restart use Static_IP to fetch
            FREF_Offs,deltaF_Global,NREF_Offs = identify_Fref_deltF_Nref(tx_freq)
            tx_Nref = str(int(NREF_Offs + (tx_freq-FREF_Offs) / deltaF_Global))
            FREF_Offs,deltaF_Global,NREF_Offs = identify_Fref_deltF_Nref(rx_freq)
            rx_Nref = str(int(NREF_Offs + (rx_freq-FREF_Offs) / deltaF_Global))
            init = initialisation()
            status = get_interface_informations_from_RU(Telnet_ip)
            if status != True:
                sys.exit(1000)
            append_to_ini_file('{}/inputs.ini'.format(root_dir),'INFO',{'tx_arfcn':tx_Nref,'rx_arfcn':rx_Nref})
            append_to_ini_file('{}/inputs.ini'.format(root_dir),'RUNNING',{'init_state':'for_telnet'})
        else: 
            #Restart is required
            print("restarting RU")
            if "RPS" in is_RPS_Or_Kiku:
                RU_PowerCycle_via_RPS()
            else:
                RU_PowerCycle_via_Kiku()
            # time.sleep(int(wait_time)//4)
            
            init = initialisation()
            print("initialising....")
            is_dhcp_config = check_interfaces(init,IP_DHCP_interface)
            print(is_dhcp_config)
            if is_dhcp_config != True:
                sys.exit(1000)
            # time.sleep(3*int(wait_time)//4)
            ip_list,mac_list = fetch_dhcp_IP_and_MAC_of_RU(init.high_speed_interface,ru_key) 
            if mac_list == False:
                print(ip_list)
                ip_list = ['192.168.4.50']
            print(ip_list[0],mac_list)
            if not init.check_ping_status(ip_list[0]):
                print("Ping not obtained...in Dynamic IP, Please Check connection")
                if not init.check_ping_status('192.168.4.50'):
                    print("Ping not obtained...in Static IP 192.168.4.50, Please Check connection")
                    sys.exit(102)
            append_to_ini_file('{}/inputs.ini'.format(root_dir),'RUNNING',{'possible_IP': f'{ip_list[0]}'})
            RU_interf = get_interface_informations_from_RU(ip_list[0])
            FREF_Offs,deltaF_Global,NREF_Offs = identify_Fref_deltF_Nref(tx_freq)
            tx_Nref = str(int(NREF_Offs + (tx_freq-FREF_Offs) / deltaF_Global))
            print(int(tx_Nref))
            FREF_Offs,deltaF_Global,NREF_Offs = identify_Fref_deltF_Nref(rx_freq)
            rx_Nref = str(int(NREF_Offs + (rx_freq-FREF_Offs) / deltaF_Global))
            print(int(rx_Nref))
            append_to_ini_file('{}/inputs.ini'.format(root_dir),'INFO',
                            {'tx_arfcn':tx_Nref,'rx_arfcn':rx_Nref})
            
            append_to_ini_file('{}/inputs.ini'.format(root_dir),'RUNNING',{'init_state':'initialised'})
            sys.exit(0)            
    elif "for_telnet" in init_status:
        print("Checking ping to Static IP")
        is_pingStatic = check_ping_to_static_IP(Telnet_ip)
        if not is_pingStatic:
            print("Aborting")
            sys.exit(1000)
        init = initialisation()
        print("Changing to DHCP via Telnet")
        status_dynamic = configure_via_telenet("Dynamic",Telnet_ip,Telnet_portid,Telnet_username,Telnet_password)
        if not status_dynamic:
            print("Telnet configuration to DHCP Failed... Aborting")
            sys.exit(2000)
        # time.sleep(25)
        
        is_dhcp_config = check_interfaces(init,IP_DHCP_interface)
        ip_list,mac_list = fetch_dhcp_IP_and_MAC_of_RU(init.high_speed_interface,ru_key) 
        print(ip_list,mac_list)
        if ip_list == None:
            print("Dynamic IP not able to fetch from DHCP Server")
            sys.exit(201)
        if not init.check_ping_status(ip_list[0]):
            print("Ping not obtained...in Dynamic IP, Please Check connection")
            sys.exit(202)
        append_to_ini_file('{}/inputs.ini'.format(root_dir),'RUNNING',{'possible_IP': f'{ip_list[0]}',
                                                                    'init_state':'initialised'})
        sys.exit(0)    
    else:
        possible_ru_IP = configur.get('RUNNING','possible_IP')
        if possible_ru_IP:
            init = initialisation()
            is_ping = init.check_ping_status(possible_ru_IP)
            if is_ping:
                sys.exit(0)
            else:
                print("Ping is not obtained --> with Possible IP....restarting RU to fetch Possible IP")
                if "RPS" in is_RPS_Or_Kiku:
                    RU_PowerCycle_via_RPS()
                else:
                    RU_PowerCycle_via_Kiku()
                init = initialisation()
                print("Re-initialising....")
                time.sleep(int(wait_time)//4)
                is_dhcp_config = check_interfaces(init,IP_DHCP_interface)
                time.sleep(3*int(wait_time)//4)
                ip_list,mac_list = fetch_dhcp_IP_and_MAC_of_RU(init.high_speed_interface,ru_key)
                print(ip_list,mac_list)
                if ip_list == None:
                    print("Dynamic IP not able to fetch from DHCP Server")
                    sys.exit(301)
                if not init.check_ping_status(ip_list[0]):
                    print("Ping not obtained...in Dynamic IP, Please Check connection")
                    sys.exit(302)
                append_to_ini_file('{}/inputs.ini'.format(root_dir),'RUNNING',{'possible_IP':f'{ip_list[0]}'})
                sys.exit(0)
