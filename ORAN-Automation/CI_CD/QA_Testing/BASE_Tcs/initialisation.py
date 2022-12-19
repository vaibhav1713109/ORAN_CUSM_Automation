import subprocess, ifcfg
import re
import configparser
import paramiko
import time
import sys,os
from configparser import ConfigParser

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(root_dir)
configur = ConfigParser()
configur.read('{}/inputs.ini'.format(root_dir))

class initialisation():
    def __init__(self) -> None:
        self.interfaces = list(ifcfg.interfaces().keys())
        self.high_speed_interface = None
        self.dhcp_interface = None
        self.HighSpeed_interface_Vlans = None
        self.dhcp_interface_IP = None
   
    def find_high_speed_interface(self):
        for interface in self.interfaces:
            cmd = f"cat /sys/class/net/{interface}/speed"
            result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = result.communicate()
            if error:
                print(f"Error: {error.decode().strip()}")
                continue
            speed = output.decode().strip()
            if speed in ["10000", "25000"]:
                self.high_speed_interface = interface
                return True
        print("Not able to find the high-speed interface.")
        return False
        
    def check_ping_status(self,ip_address):
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
      
    def get_interfcae_configured_with_DHCP_Server(self):
        command = """awk -F'=' '/^INTERFACES=/ { gsub(/"/, "", $2); print $2 }' /etc/default/isc-dhcp-server"""
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
        if error and "No such file or directory" not in error.decode().strip():
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
                        
    def is_DHCP_server_running(self):
        cmd = "sudo systemctl status isc-dhcp-server.service"
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if "Active: active (running)" in out.decode():
            return True
        else:
            return False
            
    def find_IP_of_DHCP_interface(self,interface):
        command = f"ip addr show {interface}"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, _ = process.communicate()
        if process.returncode == 0:
            lines = output.decode().split('\n')
            for line in lines:
                if 'inet ' in line:
                    ip = line.split('inet ')[1].split('/')[0]
                    self.dhcp_interface_IP = ip 
                    return True
        return False
        
    def assign_ip_for_dhcp_interface(self,interface, ip_address):
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
                if line.startswith('INTERFACES='):
                    interf_confgrd = line.split("=")[1]
                    name_interf = f'"{dhcp_interface}"'
                    if interf_confgrd[:-1] == name_interf:
                        return True
                    lines[i] = f'INTERFACES="{dhcp_interface}"\n'
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
    object_init.find_high_speed_interface(object_init.interfaces)
    if object_init.high_speed_interface == None:
        print("Initialisation Failed --> High Speed interface not identified... Aborting")
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
    object_init.get_interface_names()
    if object_init.dhcp_interface != object_init.high_speed_interface:
        print("Editing interface name in dhcp config to Base Interface")
        if object_init.edit_dhcp_interface_name(object_init.high_speed_interface):
            object_init.get_interfcae_configured_with_DHCP_Server()
            if object_init.dhcp_interface == object_init.high_speed_interface:
                print("Edited DHCP interface name")
            else:
                print("Initialisation Failed due to interface name change... Aborting")
                return False
    else:
        print("Interface name configured with DHCP server conf file is the High Speed interface itself")
    if not object_init.is_DHCP_server_running():
        object_init.find_IP_of_DHCP_interface(object_init.dhcp_interface)
        if object_init.dhcp_interface_IP == None:
            object_init.assign_ip_for_dhcp_interface(object_init.dhcp_interface,IP_dhcp_interf)
            if object_init.dhcp_interface_IP == None:
                print("Initialisation Failed --> IP can't assigned to DHCP interface... Aborting")
                return False
        if not object_init.restart_dhcp_server():
            print("Initialisation Failed --> Not able to re-start DHCP Service... Aborting")
            return False
    if object_init.is_DHCP_server_running():
        print("DHCP Server is Running...")
        return True
  
def RU_PowerCycle(rps_switch_ip):
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
    
def is_valid_ip_address(ip):
    pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    match = re.match(pattern, ip)    
    return match is not None
    
def is_valid_mac_address(mac):
    pattern = r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"
    match = re.match(pattern, mac)    
    return match is not None
    
def fetch_dhcp_IP_and_MAC_of_RU(interfc):
    ip_list=[]
    mac_list=[]
    ru_key = configur.get('INFO','ru_key')
    command = f"sudo systemctl status isc-dhcp-server.service | grep 'via {interfc}' | grep {ru_key} | grep 'DHCPACK on'"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        print(f"An error occurred: {error.decode()}")
        return None
    dhcp_msgs = output.decode().split("\n")
    print(dhcp_msgs)
    ip_pattern = '(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    mac_patter = '(?:[0-9a-fA-F]:?){12}'
    ip_list = list(re.findall(ip_pattern,dhcp_msgs[-2]))
    mac_list = list(re.findall(mac_patter,dhcp_msgs[-2]))
    msgs = [msg.strip() for msg in dhcp_msgs if msg.strip()]
    if len(ip_list) == len(mac_list) != 0:
        return ip_list,mac_list
    else:
        print("Fetching of IP address and mac address is not completed...")
        return None

def get_10g_25g_interfaces_of_RU(ru_ip, username, password, mac_address):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ru_ip, username=username, password=password)
        stdin, stdout, stderr = ssh.exec_command("ifconfig | grep -o '^[a-zA-Z0-9.]*'")
        interfaces = [line.strip() for line in stdout]        
        for interface in interfaces:
            stdin, stdout, stderr = ssh.exec_command(f"ifconfig {interface}")
            result = stdout.read().decode()
            for line in result.splitlines():
                if mac_address in line:
                    return interface
        return None
    except paramiko.ssh_exception.AuthenticationException:
        raise Exception("Authentication failed. Please check your credentials.")
    except paramiko.ssh_exception.SSHException as ssh_ex:
        raise Exception("SSH error occurred:", str(ssh_ex))
    finally:
        ssh.close()
        
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
        print(f'Error : {e}')
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
    IP_DHCP_interface = '192.168.4.15'
    root_user = configur.get('INFO','super_user')
    root_pass = configur.get('INFO','super_pass')
    rps_switch_ip = configur.get('INFO','rps_switch_ip')
    rps_switch_user = configur.get('INFO','rps_switch_user')
    rps_switch_pass = configur.get('INFO','rps_switch_pass')
    rps_switch_port = configur.get('INFO','rps_switch_port')
    wait_time = configur.get('INFO','wait_time')
    ru_name = configur.get('INFO','ru_name')
    tx_freq = float(configur.get('INFO','tx_center_frequency'))*1000
    rx_freq = float(configur.get('INFO','rx_center_frequency'))*1000
    init = initialisation()
    print("initialising....")
    # if init:
    if init.initialisation_for_dhcp(IP_DHCP_interface):
        init.find_high_speed_interface()
        print("initialisation Completed")
        # if not RU_PowerCycle(rps_switch_ip):
        #     print("RU PowerCycle is not completed... Aborting")
        #     sys.exit(100)
        input('{0}\nPlease do a power cycle....\n{0}'.format('-'*100))
        print("RU_PowerCycled...waiting")
        time.sleep(int(wait_time))  # wait_Time
        print(init.high_speed_interface)
        ip_list,mac_list = fetch_dhcp_IP_and_MAC_of_RU(init.high_speed_interface)
        print(ip_list,mac_list)
        if ip_list == None:
            sys.exit(101)
        if not init.check_ping_status(ip_list[0]):
            print("Ping not obtained... Please Check connection")
            sys.exit(102)
        RU_interf = get_10g_25g_interfaces_of_RU(ip_list[0],root_user,root_pass,mac_list[0])
        print(RU_interf)
        if RU_interf == None:
            print("Unable to identify RU 10G/25G interface")
            sys.exit(103)
        FREF_Offs,deltaF_Global,NREF_Offs = identify_Fref_deltF_Nref(tx_freq)
        tx_Nref = str(int(NREF_Offs + (tx_freq-FREF_Offs) / deltaF_Global))
        print(int(tx_Nref))
        FREF_Offs,deltaF_Global,NREF_Offs = identify_Fref_deltF_Nref(rx_freq)
        rx_Nref = str(int(NREF_Offs + (rx_freq-FREF_Offs) / deltaF_Global))
        print(int(rx_Nref))
        append_to_ini_file('{}/inputs.ini'.format(root_dir),'INFO',
                            {'tx_arfcn':tx_Nref,'rx_arfcn':rx_Nref,
                            'fh_interface':RU_interf,'ru_mac':mac_list[0]})
