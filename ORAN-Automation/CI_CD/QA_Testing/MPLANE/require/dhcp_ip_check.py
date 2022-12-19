
import sys, os, time, paramiko, subprocess,re
from ncclient import manager
from ncclient.operations import errors
from ncclient.operations.rpc import RPCError
from ncclient.transport import errors
from paramiko.ssh_exception import NoValidConnectionsError
from ncclient.operations.errors import TimeoutExpiredError
from ncclient.transport.errors import SessionCloseError
from configparser import ConfigParser
from ncclient.xml_ import to_ele

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
configur.read('{}/inputs.ini'.format(dir_name))
file = open('{}/output.txt'.format(dir_name),'a')

###############################################################################
## Related Imports
###############################################################################

import STARTUP
from Vlan_Creation import *

###############################################################################
## Initiate PDF
###############################################################################
pdf = STARTUP.PDF_CAP()
summary = []

class DHCP_IP(vlan_Creation):
    def __init__(self):
        super().__init__()
        self.interface_name = ''
        self.hostname, self.call_home_port = '',''
        self.USER_N = ''
        self.PSWRD = ''
        self.P_NEO_IP = ''
        self.P_NEO_PORT = ''
        self.session = ''
       

	

    def Ru_Reset(host):
        for _ in range(5):
            try:
                host = host
                username = 'root'
                password = 'vvdn'
                command = "ruReset"
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(host, 830, username, password)

                stdin, stdout, stderr = ssh.exec_command(command)
                lines = stdout.readlines()
                return True
            except Exception as e:
                print(e)
                pass
        else:
            print('Can\'t connect to the RU.., Logs are not deleted.')

    ###############################################################################
    ## Check DHCP Status
    ###############################################################################
    def check_dhcp_status(self):
        Result = subprocess.getoutput('sudo /etc/init.d/isc-dhcp-server status')
        Result = Result.split('DHCPACK')
        pattern = '(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        ans = re.findall(pattern,Result[-1])
        return ans[0]


    def test_Main(self):
        file.write("Test Case DHCP  is under process...")
        Check1 = self.sfp_Linked()
        
        
        ###############################################################################
        ## Read User Name and password from Config.INI of Config.py
        ###############################################################################
        self.USER_N = configur.get('INFO','sudo_user')
        self.PSWRD = configur.get('INFO','sudo_pass')
        if (Check1 == False or Check1 == None):
            return False

        pkt = sniff(iface = self.interface, stop_filter = self.check_tcp_ip,timeout = 100)
        if self.hostname:
            pass
        else:
            self.hostname = self.check_dhcp_status()

        timeout = time.time()+60
        print(f'{"-"*100}\nCheck the status of Static ip ping\n{"-"*100}')
        file.write(f'{"-"*100}\nCheck the status of Static ip ping\n{"-"*100}')
        while time.time()<timeout:
            if STARTUP.ping_status(self.hostname):
                summary.append('DHCP IP Ping Successful')
                ping_out = subprocess.getoutput("ping -c 5 {}".format(self.hostname))
                file.write(ping_out)
                return True
        else:
            file.write(f'DHCP IP {self.hostname} not Pinging')
            return False
        
def Iter_dhcp(nums = 2):
    Pass = 0
    for i in range(nums):
        file.write(f'{"-"*100}\nIteration {i+1}\n{"-"*100}')
        obj = DHCP_IP()
        Result = obj.test_Main()
        if Result:
            Pass+=1
            file.write('\n')
        else:
            pass
    print(f'Total Execution: {nums} \n Pass : {Pass}, Fail : {nums-Pass}')



if __name__ == "__main__":
    Iter_dhcp(500)

