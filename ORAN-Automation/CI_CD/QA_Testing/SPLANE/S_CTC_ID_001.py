import socket , os, STARTUP, json, sys, time, paramiko, xmltodict, xml.dom.minidom ,subprocess,re
from Notification import notification
from ncclient import manager
from scp import SCPException
from paramiko import SSHClient
from scp import SCPClient
from calnexRest import calnexInit
from configparser import ConfigParser

###############################################################################
## Directory Path
###############################################################################
dir_name = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(dir_name)
print(root_dir)

########################################################################
## For reading data from .ini file
########################################################################
configur = ConfigParser()
configur.read('{}/inputs.ini'.format(root_dir))
###########################################################################################################################
#                                                   Start PDF                                                             #
###########################################################################################################################
pdf = STARTUP.PDF_CAP(TC = "1")
d1 = os.path.dirname(os.path.realpath(__file__))
def kill_ssn(host, port, user, password,sid):
    with manager.connect(host=host, port=port, username=user, hostkey_verify=False, password=password) as m:
        m.kill_session(sid)

###########################################################################################################################
#                                                Main Fucntion code flow                                                  #
###########################################################################################################################
def session_login(host, port, user, password):
    try:
        ###########################################################################################################################
        #                                                   Netopeer Connection Initialization                                    #
        ###########################################################################################################################
        with manager.connect(host=host, port=port, username=user, hostkey_verify=False, password=password) as m:
       
            notification("Netopeer Connection Established || Success")
            list1.append("Netopeer Connection Established || Success")
            STARTUP.STORE_DATA('Step 1 Connect to the NETCONF Server',Format = True,PDF = pdf)
            STARTUP.STORE_DATA(f'''> connect --ssh --host {host} --port 830 --login {user}
                    Interactive SSH Authentication
                    Type your password:
                    Password: 
                    > status
                    Current NETCONF session:
                    ID          : {m.session_id}
                    Host        : {host}
                    Port        : {port}
                    Transport   : SSH
                    Capabilities:
                    ''',Format = False,PDF = pdf)
            for i in m.server_capabilities:
                STARTUP.STORE_DATA(i,Format = False,PDF = pdf)
        ###########################################################################################################################
        #                                       Subscribe to the Notifications                                                    #
        ###########################################################################################################################
            filter = """<filter type="xpath" xmlns="urn:ietf:params:xml:ns:netconf:notification:1.0" xmlns:sync="urn:o-ran:sync:1.0" select="/sync:*"/>"""
            cap = m.create_subscription(filter=filter)
            pdf.add_page()
            notification("Subscribed to sync notifications || Success")
            list1.append("Subscribed to sync notifications || Success")
            STARTUP.STORE_DATA('>subscribe',Format = True,PDF = pdf)
            if "ok" in str(cap) or "Ok" in str(cap) or "OK" in str(cap):
                STARTUP.STORE_DATA('Ok',Format = False,PDF = pdf)
            pdf.ln(5)
        ###########################################################################################################################
        #                                              Initial/FREERUN O-RU state                                                         #
        ###########################################################################################################################
            STARTUP.STORE_DATA('Step 1 PTP and syncE both are in Passive state',Format = True,PDF = pdf)
            time.sleep(2)
            pdf.ln(8)
            notification("Retrieving the Freerun state of O-RU || Success")
            list1.append("Retrieving the Freerun state of O-RU || Success")
            STARTUP.STORE_DATA('Step 2 Freerun State of O-RU in Startup Condition',Format = True,PDF = pdf)
            SYNC = '''<filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
            <sync xmlns="urn:o-ran:sync:1.0">
            </sync>
            </filter>
            '''       
            data1  = m.get(SYNC).data_xml
            x = xml.dom.minidom.parseString(data1)            
            xml_pretty_str = x.toprettyxml()
            STARTUP.STORE_DATA('Expected Result',Format = True,PDF = pdf)
            STARTUP.STORE_DATA(xml_pretty_str,Format = "XML",PDF= pdf)

    except Exception as e:
        STARTUP.STORE_DATA(f"{e}",Format = "TEST_STEP",PDF = pdf)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        STARTUP.STORE_DATA('Error Line Number:',f'{exc_tb.tb_lineno}',Format = "TEST_STEP",PDF = pdf)
        notification(f"Fail Reason: {e}")
        list1.append(f"Fail Reason: {e}")
        sys.exit(1)

###########################################################################################################################
#                                           Result decleration fuction                                                    #
###########################################################################################################################
def Result_Decleration(host, port, user, password):
    try:
        with manager.connect(host=host, port=port, username=user, hostkey_verify=False, password=password) as m:
            pdf.add_page()
            STARTUP.STORE_DATA('RESULTS',Format =True,PDF = pdf)
            SYNC = '''
                <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                <sync xmlns="urn:o-ran:sync:1.0">
                </sync>
                </filter>
                '''
       
            value_SYNC = m.get(SYNC).data_xml
 
            dict_Sync = xmltodict.parse(str(value_SYNC))
            Sync_state=dict_Sync['data']['sync']['sync-status']['sync-state']

            STARTUP.STORE_DATA(f"{'Sync_state STATUS' : <50}{'=' : ^20}{'PASS' : ^20}" if Sync_state == "FREERUN" else f"{'Sync_state STATUS' : <50}{'=' : ^20}{'FAIL' : ^20}",Format = False,PDF = pdf)
            
            Ptp_lock_state=dict_Sync['data']['sync']['ptp-status']['lock-state']
            STARTUP.STORE_DATA(f"{'Ptp_lock_state STATUS' : <50}{'=' : ^20}{'PASS' : ^20}" if Ptp_lock_state == "UNLOCKED" else f"{'Ptp_lock_state STATUS' : <50}{'=' : ^20}{'FAIL' : ^20}",Format = False,PDF = pdf)
            
            Ptp_state=dict_Sync['data']['sync']['ptp-status']['sources']['state']
            print(Ptp_state)
            STARTUP.STORE_DATA(f"{'Ptp_state STATUS' : <50}{'=' : ^20}{'PASS' : ^20}" if Ptp_state == "DISABLED" else f"{'Ptp_state STATUS' : <50}{'=' : ^20}{'FAIL' : ^20}",Format = False,PDF = pdf)
            
            SyncE_lock_state=dict_Sync['data']['sync']['synce-status']['lock-state']
            STARTUP.STORE_DATA(f"{'SyncE_lock_state STATUS' : <50}{'=' : ^20}{'PASS' : ^20}" if SyncE_lock_state == "UNLOCKED" else f"{'SyncE_lock_state STATUS' : <50}{'=' : ^20}{'FAIL' : ^20}",Format = False,PDF = pdf)

            SyncE_state=dict_Sync['data']['sync']['synce-status']['sources']['state']
            STARTUP.STORE_DATA(f"{'SyncE_State STATUS' : <50}{'=' : ^20}{'PASS' : ^20}" if SyncE_state == "DISABLED" else f"{'SyncE_state STATUS' : <50}{'=' : ^20}{'FAIL' : ^20}",Format = False,PDF = pdf)
    except Exception as e:
        STARTUP.STORE_DATA(f"{e}",Format = "TEST_STEP",PDF = pdf)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        STARTUP.STORE_DATA('Error Line Number:',f'{exc_tb.tb_lineno}',Format = False,PDF = pdf)
        notification(f"Fail Reason: {e}")
        list.append(f"Fail Reason: {e}")
        sys.exit(1)

def CREATE_LOGS(PDF,name):
    name1 = str(path) + "/" +str(name) + ".pdf"
    PDF.output(name1)

def get_ip_address(inr):
        wait_time = 60
        ru_mac = inr
        timeout = time.time()+wait_time
        Result = subprocess.getoutput(f'sudo journalctl -u isc-dhcp-server.service | grep "{ru_mac}" | grep "DHCPACK"')
        Result = Result.split('\n')
        dhcp_ip = ''
        # for line in Result:
        #     if "DHCPACK on" in line and f"via {self.INTERFACE_NAME}" in line: 
        pattern = '(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        ans = re.findall(pattern,Result[-1])
        dhcp_ip = ans[0]
        return dhcp_ip

if __name__ == '__main__':
    try:
        list1 = []
        # f = open(f'{d1}/details.json')
        # data = json.load(f)
        Paragon_IP = configur.get('SPlane','paragon_ip')
        calnexInit(Paragon_IP)
        ip_type = configur.get('INFO','static_dynamic')
        ip_type = ip_type.upper()
        username = configur.get('INFO','sudo_user')
        password = configur.get('INFO','sudo_pass')
        root_user = configur.get('INFO','super_user')
        root_pass = configur.get('INFO','super_pass')
        syslog_path = configur.get('INFO','syslog_path')
        ru_name = configur.get('INFO','ru_name')
        img_version = configur.get('INFO','img_version')
        static_ip = configur.get('INFO','static_ip')
        report_path = f"{root_dir}/LOGS/{ru_name}/{img_version}/SPLANE"
        ###########################################################################################################################
        #                                              Dynamic ip Code Flow                                                        #
        ###########################################################################################################################
        if ip_type == "DYNAMIC":
            inr = configur.get('INFO','ru_mac')
            # m = manager.call_home(host = '', port=4334, hostkey_verify=False,username =username, password =password)
            # li = m._session._transport.sock.getpeername()
            # sid = m.session_id
            # kill_ssn(li,830,username,password,sid)
            ip = get_ip_address(inr)
            res = session_login(ip,830,username,password)   
            pdf.add_page()
        ###########################################################################################################################
        #                                              Capturing system logs                                                         #
        ###########################################################################################################################
            STARTUP.STORE_DATA('SYSTEM LOGS',Format = True,PDF = pdf)
            command = f"cat {syslog_path} | grep SYNCMNGR;"
            command1 = f"rm -rf {syslog_path};"
            
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            s = ssh_client.connect(hostname=ip,username=root_user,password=root_pass)
            stdin, stdout, stderr = ssh_client.exec_command(command)
            lines = stdout.readlines()
            for i in lines:
                STARTUP.STORE_DATA(i,Format ="XML",PDF = pdf)
            
            Result_Decleration(ip,830,username,password)
            path = report_path
            Remote_path= path + "/TC1.log"
            ssh_ob = paramiko.SSHClient()
            ssh_ob.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_ob.connect(hostname=ip,username=root_user,password=root_pass)
            scp = SCPClient(ssh_ob.get_transport())
            scp.get('/var/log/synctimingptp2.log',Remote_path)
            scp.close()
            notification("Logs Created || Success")
            list1.append("Logs Created || Success")
            pdf.ln(10)
            STARTUP.STORE_DATA("SUMMARY",Format =True,PDF = pdf)
            pdf.ln(2)
            STARTUP.summary(pdf,list1)
            CREATE_LOGS(pdf,name = "S_CTC_ID_001")
            # command2 = "reboot"            
            # ssh_client = paramiko.SSHClient()
            # ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # ssh_client.connect(hostname=ip,username=root_user,password=root_pass)
            # stdin, stdout, stderr = ssh_client.exec_command(command2)
            # time.sleep(120)
            # notification("Board rebooted successfully proceed to next test case")
            
        ###########################################################################################################################
        #                                              Static ip Code Flow                                                        #
        ###########################################################################################################################
        elif ip_type == "STATIC":
            res = session_login(static_ip,830,username,password)   
            pdf.add_page()
            STARTUP.STORE_DATA('SYSTEM LOGS',Format = True,PDF = pdf)
            # command = f"cat {syslog_path} | grep SYNCMNGR"
            command = f"cat {syslog_path}"
            # command = f"cat {syslog_path}"
            command1 = f"rm -rf {syslog_path}"
        
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=static_ip,username=root_user,password=root_pass)
            
            stdin, stdout, stderr = ssh_client.exec_command(command)
            lines = stdout.readlines()
            for i in lines:
                STARTUP.STORE_DATA(i,Format ="XML",PDF = pdf)
            stdin, stdout, stderr = ssh_client.exec_command(command1)

            Result_Decleration(static_ip,830,username,password)
            list1.append("Result Status || Declared")
            path = report_path
            Remote_path= path + "/TC1.log"
            ssh_ob = paramiko.SSHClient()
            ssh_ob.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_ob.connect(hostname=static_ip,username=root_user,password=root_pass)
            scp = SCPClient(ssh_ob.get_transport())
            scp.get('/var/log/synctimingptp2.log',Remote_path)
            scp.close()
            pdf.ln(10)
            STARTUP.STORE_DATA("SUMMARY",Format =True,PDF = pdf)
            pdf.ln(2)
            STARTUP.summary(pdf,list1)
            CREATE_LOGS(pdf,name = "S_CTC_ID_001")
            # command2 = "reboot"            
            # ssh_client = paramiko.SSHClient()
            # ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # ssh_client.connect(hostname=static_ip,username=root_user,password=root_pass)
            # stdin, stdout, stderr = ssh_client.exec_command(command2)
            # time.sleep(200)
            # notification("Board rebooted successfully proceed to next test case")
        else:
            print("ip type not defined correctly in details.json")
            notification("ip type not defined correctly in details.json")
            sys.exit(1)

    except SCPException as e:
        STARTUP.STORE_DATA("File Not found in RU",Format = False,PDF = pdf)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        STARTUP.STORE_DATA(f'Error Line Number:{exc_tb.tb_lineno}',Format =False,PDF = pdf)     
        notification(f"Fail Reason: {e}")
        list1.append(f"Fail Reason: {e}")
        sys.exit(1)
    except UnicodeError as e:
        STARTUP.STORE_DATA("Please give correct Ip address",Format =False,PDF = pdf)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        STARTUP.STORE_DATA(f'Error Line Number:{exc_tb.tb_lineno}',Format = False,PDF = pdf)
        notification(f"Fail Reason: {e}")
        list1.append(f"Fail Reason: {e}")
        sys.exit(1)

    except paramiko.ssh_exception.AuthenticationException as e:
        STARTUP.STORE_DATA("Please give correct username or password",Format =False,PDF = pdf)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        STARTUP.STORE_DATA(f'Error Line Number:{exc_tb.tb_lineno}',Format = False,PDF = pdf)
        notification(f"Fail Reason: {e}")
        list1.append(f"Fail Reason: {e}")
        sys.exit(1)

    except socket.timeout as e:
        STARTUP.STORE_DATA(f'{e}',Format = False,PDF = pdf)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        STARTUP.STORE_DATA(f'Error Line Number:{exc_tb.tb_lineno}',Format = False,PDF = pdf)
        notification(f"Fail Reason: {e}")
        list1.append(f"Fail Reason: {e}")
        sys.exit(1)
    except Exception as e:
        STARTUP.STORE_DATA(f'{e}',Format = "TEST_STEP",PDF = pdf)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        STARTUP.STORE_DATA(f'Error Line Number:{exc_tb.tb_lineno}',Format = False,PDF = pdf) 
        notification(f"Fail Reason: {e}")
        list1.append(f"Fail Reason: {e}")
        sys.exit(1)