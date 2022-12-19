import pandas as pd
import subprocess
import shutil
import xml.etree.ElementTree as ET
import time
import os
import sys
import re
import random
from tabulate import tabulate
import configparser
import paramiko

###############################################################################
# Directory Path
###############################################################################
dir_name = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(dir_name)
print(root_dir)
sys.path.append(root_dir)

from MPLANE.require.Notification import notification

def create_table_and_send_to_space(data):
    Header = ['Test Case', 'Status']
    ACT_RES = tabulate(data, Header, tablefmt='fancy_grid')
    notification(ACT_RES)

def process_arguments():
    if len(sys.argv) == 3:
        RU_name = sys.argv[1]
        Version = sys.argv[2]
        return RU_name, Version, 0
    else:
        print("Program called with incorrect format")
        return 406, 406, 406

def create_ini_file(config_param):
    INFO = ['IP_DHCP_interface', 'Static_Dynamic', 'static_ip', 'sudo_user', 'sudo_pass', 'sftp_user', 'sftp_pass', 'element_name',
            'syslog_path', 'flash_image_path', 'wait_time', 'scs_value', 'duplex_scheme', 'tx_center_frequency','rx_center_frequency',
            'bandwidth', 'tx_arfcn', 'rx_arfcn', 'corrupt_image_path','sw_path', 'ru_name', 'img_version', 'uplane_xml', 'tc_27_xml',
            'du_fh_interface','ru_key','super_user', 'super_pass']
    
    CUPlane = ['test_mac_ip', 'test_mac_username', 'test_mac_password', 'Flex_Ran_Path', 'vxt_add', 'du_mac', 'Amplitude', 'external_gain']

    PowerCycle = ['RPS_Kikusui','rps_switch_ip','rps_switch_user', 'rps_switch_pass', 'rps_switch_port','Kiku_visa_addrs']

    SPlane = ["paragon_ip", "port_num", "File_path"]

    Telnet = ['is_telnet','port_id','telnet_user','telnet_password']

    RUNNING = ["Parent_path","init_state", 'ru_mac', 'fh_interface']
    config = configparser.ConfigParser()
    config.add_section('INFO')
    config.add_section('CUPlane')
    config.add_section('PowerCycle')
    config.add_section('SPlane')
    config.add_section('RUNNING')
    config.add_section('Telnet')

    for key, value in config_param.items():
        if key in INFO:
            config.set('INFO', key, str(value))
        elif key in CUPlane:
            config.set('CUPlane', key, str(value))
        elif key in PowerCycle:
            config.set('PowerCycle', key, str(value))
        elif key in SPlane:
            config.set('SPlane', key, str(value))
        elif key in Telnet:
            config.set('Telnet', key, str(value))
        elif key in RUNNING:
            config.set('RUNNING', key, str(value))
    

    with open('{}/inputs.ini'.format(root_dir), 'w') as configfile:
        config.write(configfile)
    if os.path.exists('{}/inputs.ini'.format(root_dir)):
        print(f"Create_ini_file : {root_dir}/inputs.ini File created Successfully...")
        return True
    else:
        return "Create_ini_file Error : File is not created..."


def read_xls_for_fetching_config_and_test_cases(ru_name, version):
    ru_keyword = {"LPRUB_4T4R":"lpru","LPRUC_4T4R":"lpru","LPRUD_4T4R":"lpru","BND28_4T4R":"bn28","BND1_2T2R":"mcb1","VVDN_8T8R":"VVDN8T8R"}
    df = pd.ExcelFile('{}/test_case.xlsx'.format(dir_name))
    df1 = pd.read_excel(df, header=0, nrows=50)
    df2 = pd.read_excel(df, header=0, skiprows=51)
    config_param_dict = {}
    for i, row in df1.iterrows():
        config = row['Config_Param']
        param = row['Value']
        config_param_dict[config] = param
    if ru_name != config_param_dict['ru_name']:
        print(f'ru_name conflict --> The name Passed to Master = {ru_name},,, Connect with CICD team')
        print("Aborting...")
        return None
    if version != config_param_dict['img_version']:
        print(f'img_version conflict --> The version Passed to Master = {version},,, Connect with CICD team')
        print("Aborting...")
        return None
    config_param_dict['ru_key'] = ru_keyword[ru_name].format(ru_name)
    config_param_dict['flash_image_path'] = f'{root_dir}/RUs_Info/{ru_name}/Flash_Image'
    config_param_dict['corrupt_image_path'] = f'{root_dir}/RUs_Info/{ru_name}/Corrupt_Image'
    uplan_xml = "{0}/RUs_Info/{1}/uplane.xml".format(root_dir, ru_name)
    tc_27_xml = "{0}/RUs_Info/{1}/tc_27.xml".format(root_dir, ru_name)
    config_param_dict['uplane_xml'] = uplan_xml
    config_param_dict['tc_27_xml'] = tc_27_xml
    config_param_dict['Parent_path'] = root_dir
    config_param_dict['init_state'] = "Not_initialised"
    print(config_param_dict)
    if create_ini_file(config_param_dict):
        return df2
    else:
        return None

def Create_required_directories(ru_name, version):
    try:
        import pwd,grp
        new_owner = new_group = root_dir.split('/')[2]
        uid = pwd.getpwnam(new_owner).pw_uid
        gid = grp.getgrnam(new_group).gr_gid
        present_time = time.localtime()
        if not os.path.exists(f"{root_dir}/LOGS"):
            os.mkdir(f"{root_dir}/LOGS")
            os.chown(f"{root_dir}/LOGS",uid,gid)
        if not os.path.exists(f"{root_dir}/LOGS/{ru_name}/"):
            os.mkdir(f"{root_dir}/LOGS/{ru_name}/")
            os.chown(f"{root_dir}/LOGS/{ru_name}/",uid,gid)
        if not os.path.exists(f"{root_dir}/LOGS/{ru_name}/{version}/"):
            os.mkdir(f"{root_dir}/LOGS/{ru_name}/{version}/")
            os.chown(f"{root_dir}/LOGS/{ru_name}/{version}/",uid,gid)
        if not os.path.exists(f"{root_dir}/LOGS/{ru_name}/{version}/MPLANE/"):
            os.mkdir(f"{root_dir}/LOGS/{ru_name}/{version}/MPLANE/")
            os.chown(f"{root_dir}/LOGS/{ru_name}/{version}/MPLANE/",uid,gid)
        if not os.path.exists(f"{root_dir}/LOGS/{ru_name}/{version}/SPLANE/"):
            os.mkdir(f"{root_dir}/LOGS/{ru_name}/{version}/SPLANE/")
            os.chown(f"{root_dir}/LOGS/{ru_name}/{version}/SPLANE/",uid,gid)
        if not os.path.exists(f"{root_dir}/LOGS/{ru_name}/{version}/CUPLANE/"):
            os.mkdir(f"{root_dir}/LOGS/{ru_name}/{version}/CUPLANE/")
            os.chown(f"{root_dir}/LOGS/{ru_name}/{version}/CUPLANE/",uid,gid)
        if not os.path.exists(f"{root_dir}/LOGS/{ru_name}/{version}/CUPLANE/TestMac/"):
            os.mkdir(f"{root_dir}/LOGS/{ru_name}/{version}/CUPLANE/TestMac/")
            os.chown(f"{root_dir}/LOGS/{ru_name}/{version}/CUPLANE/TestMac/",uid,gid)
        if not os.path.exists(f"{root_dir}/Master_Script/xml_files"):
            os.mkdir(f"{root_dir}/Master_Script/xml_files")
            os.chown(f"{root_dir}/Master_Script/xml_files",uid,gid)
        
        if os.path.exists(f"{root_dir}/LOGS/{ru_name}/{version}/MPLANE/") and os.path.exists(f"{root_dir}/LOGS/{ru_name}/{version}/SPLANE/") and os.path.exists(f"{root_dir}/LOGS/{ru_name}/{version}/CUPLANE/") and os.path.exists(f"{root_dir}/LOGS/{ru_name}/{version}/CUPLANE/TestMac/"):
            print('Create_directories : All require directories are created successfully ...')
            return True
        else:
            print('Create_directories Error : All require directories are not created...')
            return False
    except Exception as e:
        error = f"Create_directories_and_copy_ini_file Error : {e}"
        print(error)
        return False

def execute_a_specific_test_case(root_dir, script_path, script_name, arguments, timeout):
    absolute_script_path = f'{root_dir}/{script_path}'
    start_time = time.time()
    if str(arguments) == 'nan':
        process = subprocess.Popen(['{0}/CI_CD/bin/python'.format(root_dir),'{0}/{1}'.format(absolute_script_path, script_name)])
    else:
        argument_list = str(arguments).split()
        script_args = ['{0}/CI_CD/bin/python'.format(root_dir),'{0}/{1}'.format(absolute_script_path, script_name)] + argument_list
        process = subprocess.Popen(script_args)
    while process.poll() is None:
        elapsed_time = time.time() - start_time
        if elapsed_time > timeout:
            print("execute_tc_xls",return_code,elapsed_time) 
            process.terminate()
            return 408,elapsed_time
    print("execute_tc_xls_outside while",return_code,elapsed_time) 
    return process.returncode,elapsed_time

def execute_tc_xls(df, ru_name, Version, Pass, Fail, Skip):
    create_xml_file()
    config = configparser.ConfigParser()
    config.read('{}/inputs.ini'.format(root_dir))
    init_Status = config.get('RUNNING','init_state')
    index = 0
    retry_flag = False
    while index < len(df):
        row = df.iloc[index] 
        execute = row['Execute']
        script_name = row['Script Name']
        script_path = row['Script Path']
        arguments = row['Arguments']
        timeout = row['Timeout']
        plane = row['Plane']
        new_filename = f'{root_dir}/Master_Script/xml_files/temp_{index}.xml'
        if index > 0:
            copy_root_branch_and_last_testcase_from_xml(f"{dir_name}/test_status.xml", f"{dir_name}/temp.xml")
            with open(new_filename,'w+'):
                print(f'{new_filename} is created.')
            shutil.copyfile(f"{dir_name}/temp.xml",new_filename)
        if execute == 'yes':
            absolute_script_path = f'{root_dir}/{script_path}'
            return_code,elapsed_time = execute_a_specific_test_case(root_dir, script_path, script_name, arguments, timeout)
            print("execute_tc_xls",return_code,elapsed_time) 
            if return_code == 0:
                append_pass_in_xml_file(script_name, plane, "pass", elapsed_time)
                executed_test_case.append([script_name, 'Pass'])
                Pass += 1
            elif return_code == 408:
                append_Timeout_failure_in_xml_file(script_name, plane, "Timeout", elapsed_time)
                executed_test_case.append([script_name, 'Timeout'])
                Fail += 1
            elif return_code == 100 and ru_name == "LPRU":
                append_fail_in_xml_file(script_name, plane, "fail", elapsed_time, return_code)
                executed_test_case.append([script_name, 'Fail'])
                Fail += 1
                process = subprocess.Popen(['{0}/CI_CD/bin/python'.format(
                    root_dir), '{0}/{1}'.format(absolute_script_path, 'RU_powercycle.py')])
            else:
                print(f"The TestCase : {script_name} is returned = {return_code}")
                append_fail_in_xml_file(script_name, plane, "fail", elapsed_time, return_code)
                executed_test_case.append([script_name, 'Fail'])
                Fail += 1
            if retry_flag:
                if return_code != 0:
                    print("Software Update is not completed, Therefore quiting further Testing")
                    return Pass, Fail, Skip

        else:
            append_skiped_in_xml_file(script_name, plane, "skipped", 0)
            executed_test_case.append([script_name, 'Skip'])
            Skip += 1
            time.sleep(5)
        if (script_name == 'sw_update.py') and (execute == 'yes'):
            if return_code != 0:
                retry_flag = True
                continue
            if init_Status == 'for_telnet':
                initialization_script_path = f'{root_dir}/BASE_Tcs/initialisation.py'
                process = subprocess.Popen(['{0}/CI_CD/bin/python'.format(root_dir), '{0}'.format(initialization_script_path)])
                while process.poll() is None:
                    pass
                ReturnCode = process.returncode
                print(ReturnCode)
                if ReturnCode == 0:
                    print("RU configured to Dynamic,   Initialisation Completed")
                else:
                    print("RU_not configured to Dynamic, initialisation is not completed")
        elif init_Status == 'for_telnet':
            append_to_ini_file('{}/inputs.ini'.format(root_dir),'RUNNING',{'init_state':'initialised'})
        index += 1
    copy_root_branch_and_last_testcase_from_xml(f"{dir_name}/test_status.xml", f"{dir_name}/temp.xml")
    new_filename = f'{root_dir}/Master_Script/xml_files/temp_{index+1}.xml'
    with open(new_filename,'w+'):
        print(f'{new_filename} is created.')
    shutil.copyfile(f"{dir_name}/temp.xml",new_filename)
    return Pass, Fail, Skip

def read_ini_file(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    connection_details = {}
    connection_details['host'] = config.get('INFO', 'static_ip')
    connection_details['username'] = config.get('INFO', 'super_user')
    connection_details['password'] = config.get('INFO', 'super_pass')
    return connection_details

def create_xml_file():
    os.remove('{}/test_status.xml'.format(dir_name)
              ) if os.path.exists('{}/test_status.xml'.format(dir_name)) else None
    root = ET.Element("testsuites")
    testsuite = ET.SubElement(root, "testsuite")
    testsuite.set("name", "cd_testings")
    testsuite.set("tests", "0")
    testsuite.set("skipped", "0")
    testsuite.set("failures", "0")
    testsuite.set("time", "0")
    tree = ET.ElementTree(root)
    tree.write('{}/test_status.xml'.format(dir_name),
               encoding="utf-8", xml_declaration=True)

def append_Timeout_failure_in_xml_file(script_name, plane, status, elapsed_time):
    tree = ET.parse('{}/test_status.xml'.format(dir_name))
    root = tree.getroot()
    testsuite = root.find('testsuite')
    testsuite.set('tests', str(int(testsuite.get('tests'))+1))
    testsuite.set('failures', str(int(testsuite.get('failures'))+1))
    testsuite.set('time', str(float(testsuite.get('time'))+elapsed_time))
    testcase = ET.SubElement(testsuite, 'testcase')
    testcase.set('name', script_name)
    testcase.set('classname', plane)
    testcase.set('time', str(elapsed_time))
    failure = ET.SubElement(testcase, 'failure')
    failure.set('type', status)
    failure.text = f"The testcase execution time reached beyond {elapsed_time}"
    tree.write('{}/test_status.xml'.format(dir_name),
               encoding='utf-8', xml_declaration=True)

def append_pass_in_xml_file(script_name, plane, status, elapsed_time):
    tree = ET.parse('{}/test_status.xml'.format(dir_name))
    root = tree.getroot()
    testsuite = root.find('testsuite')
    testsuite.set('tests', str(int(testsuite.get('tests'))+1))
    testsuite.set('time', str(float(testsuite.get('time'))+elapsed_time))
    testcase = ET.SubElement(testsuite, 'testcase')
    testcase.set('name', script_name)
    testcase.set('classname', plane)
    testcase.set('time', str(elapsed_time))
    #ET.SubElement(testcase, status)
    tree.write('{}/test_status.xml'.format(dir_name),
               encoding='utf-8', xml_declaration=True)

def append_fail_in_xml_file(script_name, plane, status, elapsed_time, return_code):
    tree = ET.parse('{}/test_status.xml'.format(dir_name))
    root = tree.getroot()
    testsuite = root.find('testsuite')
    testsuite.set('tests', str(int(testsuite.get('tests'))+1))
    testsuite.set('failures', str(int(testsuite.get('failures'))+1))
    testsuite.set('time', str(float(testsuite.get('time'))+elapsed_time))
    testcase = ET.SubElement(testsuite, 'testcase')
    testcase.set('name', script_name)
    testcase.set('classname', plane)
    testcase.set('time', str(elapsed_time))
    failure = ET.SubElement(testcase, 'failure')
    failure.set('type', status)
    failure.text = f"The expected return code was 0, But obtained : {return_code}"
    tree.write('{}/test_status.xml'.format(dir_name),
               encoding='utf-8', xml_declaration=True)

def append_skiped_in_xml_file(script_name, plane, status, elapsed_time):
    tree = ET.parse('{}/test_status.xml'.format(dir_name))
    root = tree.getroot()
    testsuite = root.find('testsuite')
    testsuite.set('tests', str(int(testsuite.get('tests'))+1))
    testsuite.set('skipped', str(int(testsuite.get('skipped'))+1))
    testsuite.set('time', str(float(testsuite.get('time'))+elapsed_time))
    testcase = ET.SubElement(testsuite, 'testcase')
    testcase.set('name', script_name)
    testcase.set('classname', plane)
    testcase.set('time', str(elapsed_time))
    skipped = ET.SubElement(testcase, status)
    tree.write('{}/test_status.xml'.format(dir_name))

def copy_root_branch_and_last_testcase_from_xml(input_xml, output_xml):
    tree = ET.parse(input_xml)
    root = tree.getroot()
    output_root = ET.Element(root.tag)
    output_tree = ET.ElementTree(output_root)
    last_testsuite = root.findall('testsuite')[-1]
    # print(last_testsuite.text,dir(last_testsuite))
    # print(last_testsuite.findall('testcase'))
    output_testsuite = ET.SubElement(output_root, 'testsuite')
    output_testsuite.attrib = last_testsuite.attrib
    test_cases = last_testsuite.findall('testcase')
    if len(test_cases) > 0:
        last_testcase = test_cases[-1]
        output_testcase = ET.SubElement(output_testsuite, 'testcase')
        output_testcase.attrib = last_testcase.attrib
        for child in last_testcase:
            output_testcase.append(child)
        output_tree.write(output_xml)
    #input('Please check xml')

####################  Below functions currently not used in this Master Script #######################################

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

def read_ini_file(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    connection_details = {}
    connection_details['host'] = config.get('INFO', 'static_ip')
    connection_details['username'] = config.get('INFO', 'super_user')
    connection_details['password'] = config.get('INFO', 'super_pass')
    return connection_details

####################   Above 2 functions are not used in this Master Script currently  ##############################


if __name__ == "__main__":
    # try:
        RU_name, Version, valid = process_arguments()
        print(RU_name, Version, valid)
        if valid != 0:
            print("Master Script called incorrectly... Use the following format")
            print(
                f'sudo {root_dir}/CI_CD/bin/python {dir_name}/read_xls_execute_scripts.py <RU_name>, <Version>')
            raise Exception("Aborting...")
        else:
            df = read_xls_for_fetching_config_and_test_cases(RU_name, Version)
            if type(df) == pd.DataFrame:
                is_complete = Create_required_directories(RU_name,Version)
                if is_complete:
                    initialization_script_path = f'{root_dir}/BASE_Tcs/re_init.py'
                    process = subprocess.Popen(
                            ['{0}/CI_CD/bin/python'.format(root_dir), '{0}'.format(initialization_script_path)])
                    while process.poll() is None:
                        pass
                    return_code = process.returncode
                    print(return_code)
                    if return_code == 0:
                        input_file_path = f"{root_dir}/inputs.ini"
                        output_file_path = f"{root_dir}/MPLANE/require/inputs.ini"
                        shutil.copyfile(input_file_path, output_file_path)
                        print("The ini file copied Successfully")
                        Pass, Fail, Skip = 0, 0, 0
                        executed_test_case = []
                        Pass, Fail, Skip = execute_tc_xls(df,RU_name, Version, Pass, Fail, Skip)
                        create_table_and_send_to_space(executed_test_case)
                        notification(f'Total Test cases : {len(executed_test_case)}\nPass Test cases : {Pass}\nFail Test cases : {Fail}\nSkip Test cases : {Skip}')
                    else:
                        print(f'RU Initialisation is not completed successfully.')
                else:
                    print('Not able to obtain the Config Params')
                    raise Exception("Aborting...")
            else:
                print('Not able to create the config --> ini file')
                raise Exception("Aborting...")
    # except Exception as e:
    #     print(f'Main Function Error : {e}')
    #     print("Execution not Completed")
    # finally:
    #     # Create the finish.txt file
    #     time.sleep(5)
    #     open('finish', 'w').close()
