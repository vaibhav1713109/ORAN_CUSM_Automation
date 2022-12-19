
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


class DHCP_IP():
    def __init__(self):
        super().__init__()
        self.interface_name = ''
        self.hostname, self.call_home_port = '',''
        self.USER_N = ''
        self.PSWRD = ''
        self.session = ''
    
    ###############################################################################
    ## Check Ping
    ###############################################################################
    def check_ping_status(self, ip_address):
        response = subprocess.Popen(f"ping -c 5 {ip_address}", shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = response.communicate()
        Response = stdout.decode()
        pattern = '[1-5] received'
        ans  = re.search(pattern,Response)
        if ans:
            return True
        else:
            return False
        
    ###############################################################################
    ## Identify the 10/25G Interface
    ###############################################################################
    def identify_10G_interface(self):
        du_fh_interface = configur.get('INFO','du_fh_interface')
        cmd = f"sudo ethtool {du_fh_interface} | grep 'Speed:\|Link detected'"
        # print(cmd)
        p = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        if 'sudo: /etc/sudoers.d/README is world writable' not in stderr.decode() and stderr:
            print(f"identify_10G_interface Error :", stderr)
            return False
        else:
            output = stdout.decode().split('\n')
            if '10000' in  output[0] or '25000' in  output[0]:
                return du_fh_interface
	
    ###############################################################################
    ## Get IP its return either DHCP or Static
    ###############################################################################
    def get_ip_address(self,file):
        timeout = time.time()+2
        static_ip = configur.get('INFO','static_ip')
        Result = subprocess.getoutput('sudo /etc/init.d/isc-dhcp-server status')
        Result = Result.split('DHCPACK')
        pattern = '(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        dhcp_ip = re.findall(pattern,Result[-1])[-1]
        print(f"DHCP IP: {dhcp_ip}")
        print(f'{"-"*100}\nCheck the status of DHCP ip {dhcp_ip} ping\n{"-"*100}')
        ping_out = ''
        while time.time()<timeout:
            if self.check_ping_status(dhcp_ip):
                print(f"DHCP IP {dhcp_ip} ping || successful.")
                ping_out = subprocess.getoutput("ping -c 5 {}".format(dhcp_ip))
                file.writelines(ping_out)
                print(ping_out)
                self.hostname = dhcp_ip
                return True
            time.sleep(5)
        else:
            print(f"DHCP IP {dhcp_ip} ping || fail.")
            file.write(f"\nDHCP IP {dhcp_ip} ping || fail.\n")
            print(ping_out)
            print(f'{"-"*100}\nCheck the status of Static ip {static_ip} ping\n{"-"*100}')
            for _ in range(5):
                if self.check_ping_status(static_ip):
                    file.write(f'\nStatic IP {static_ip} Ping || Successful\n\n')
                    ping_out = subprocess.getoutput("ping -c 5 {}".format(static_ip))
                    file.writelines(ping_out)
                    print(ping_out)
                    self.hostname = static_ip
                    return True
                time.sleep(5)
            else:
                print(f'Static IP {static_ip} Ping || Fail')
                file.write(f'\nStatic IP {static_ip} Ping || Fail\n')
                print(ping_out)
                return False

    def Ru_Reset(self,host,file):
        for _ in range(5):
            try:
                host = host
                username = 'root'
                password = 'vvdn'
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                print(host, 22, username, password)
                ssh.connect(host, 22, username, password)
                chan = ssh.invoke_shell()
                chan.send('ifconfig' + "\n")
                time.sleep(10)
                output = chan.recv(1024).decode("utf-8")
                file.writelines(output)
                print(output)
                chan.send('ruReset' + "\n")
                # stdin, stdout, stderr = ssh.exec_command(command)
                # lines = stdout.readlines()
                time.sleep(5)
                output = chan.recv(1024).decode("utf-8")
                file.writelines(output)
                file.write("\n\n")
                file.write("-"*100)
                print(output)
                return True
            except Exception as e:
                print("Ru_Reset error :",e)
            finally:
                try:
                    chan.close()
                    ssh.close()
                except Exception as e:
                    print("Ru_Reset error :",e)
        else:
            print('Can\'t connect to the RU.., Logs are not deleted.')

    def test_Main(self,file):
        file.write("\nTest Case DHCP  is under process...\n")
        Check1 = self.identify_10G_interface()
        
        
        ###############################################################################
        ## Read User Name and password from Config.INI of Config.py
        ###############################################################################
        self.USER_N = configur.get('INFO','sudo_user')
        self.PSWRD = configur.get('INFO','sudo_pass')
        if (Check1 == False or Check1 == None):
            return False
        status = self.get_ip_address(file)
        return status
        
def Iter_dhcp(nums = 2):
    file = open('{}/output.txt'.format(dir_name),'w')
    Pass = Fail = 0
    obj = DHCP_IP()
    Result = obj.test_Main(file)
    file.close()
    if Result:
        for i in range(nums):
            file = open('{}/output.txt'.format(dir_name),'a')
            file.write(f'\n{"#"*100}\nIteration {i+1}\n{"#"*100}')
            file.write('\n')
            reset_st = obj.Ru_Reset(obj.hostname,file)
            if reset_st == True:
                time.sleep(150)
            else:
                print(reset_st)
                file.close()
                continue
            Result = obj.test_Main(file)
            file.close()
            if Result:
                Pass+=1
            else:
                Fail+=1
    else:
        print('Neither dynamic ip ping nor static ip.')
    file = open('{}/output.txt'.format(dir_name),'a')
    file.write(f'\n\nTotal Execution: {nums} \n Pass : {Pass},Fail : {Fail}, Skip : {nums-Pass-Fail}\n')
    print(f'Total Execution: {nums} \n Pass : {Pass},Fail : {Fail}, Skip : {nums-Pass-Fail}')



if __name__ == "__main__":
    iteration = sys.argv[1]
    Iter_dhcp(int(iteration))

