import os
import paramiko, time,re, sys
from configparser import ConfigParser
from genrate_report import *


parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root_dir = os.path.dirname(parent_dir)
configur = ConfigParser()
configur.read('{}/inputs.ini'.format(root_dir))

def ul_crc_result(channel, command):
    pattern = '\s*[(]\s*\d+\s+\d+\s+\d*\s*\d+[)]\s*'
    crc_pattern = '\s*[(]\s*\d+\s+\d+\s+1[)]\s*'
    crc_pass = crc_fail = 0
    stdin, stdout, stderr = channel.exec_command(command)
    print(stderr.readlines())
    lines = stdout.readlines()
    print(*lines)
    ul_crc_data = []
    for line in lines[::-1]:
        if 'UL ' in line and 'US    ' in line:
            # ul_crc_data.append('{}\n'.format('-'*100))
            if crc_pass+crc_fail == 12:
                break
            index = lines.index(line)
            ul_crc_data.append(lines[index])
            ul_crc_data.append(lines[index+1])
            # print(lines[index+2],end='')
            ul_crc_data.append(lines[index+3])
            # print(lines[index+4],end='')
            val = re.findall(pattern,lines[index+1])
            crc = re.findall(crc_pattern,val[2])
            # print(f'CRC_Value for {lines[index].split("|")[0]} = {val}')
            if len(crc) != 0:
                crc_pass+=1
                # print(f'CRC_Value for {lines[index].split("|")[0]} = Pass')
            else:
                crc_fail+=1
                # print(f'CRC_Value for {lines[index].split("|")[0]} = Fail')
    print('='*100)
    print("Summary".center(100))
    print('='*100)
    for data in ul_crc_data:
        print('-'*100)
        print(data,end='')
    center_freq = configur.get('INFO','tx_center_frequency')
    bandwidth = configur.get('INFO','bandwidth')
    status = []
    if crc_fail > 0 or crc_pass == 0:
        status.append('Fail')
    else:
        status.append('Pass')
    status.insert(0,center_freq)
    status.insert(1,bandwidth)
    return status,crc_fail,crc_pass,ul_crc_data



if __name__ == "__main__":
    test_mac_ip, username, password='172.17.95.107','vvdn','vvdntech'
    ssh1 = paramiko.SSHClient()
    ssh1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh1.connect(test_mac_ip, username = username, password =password)
    cmd = "sudo -s cat /home/vvdn/Source_bkp/FlexRAN_v22.07_release_pacakge/bin/nr5g/gnb/l1/PhyStats-c0.txt"
    Result = ul_crc_result(ssh1,cmd)
    ## Genrating the report
    report_path = '{0}/TestMac/Results/{1}.pdf'.format(root_dir,sys.argv[0].split('.')[0])
    genrate_report_ul([Result[0]],Result[1],Result[2],report_path,Result[-1])
    if 'Pass' in Result[0]:
        print('='*100)
        print("CRC : PASS".center(100))
        print('='*100)
        sys.exit(0)
    else:
        print('='*100)
        print("CRC : Fail".center(100))
        print('='*100)
        sys.exit(5000)