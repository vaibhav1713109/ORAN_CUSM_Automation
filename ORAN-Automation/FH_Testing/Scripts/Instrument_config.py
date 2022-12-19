import sys, re, xmltodict,shutil
import os
import time
from configparser import ConfigParser
import requests
import xml.etree.ElementTree as ET

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(root_dir)




def ORS_instrument_Configuration(config_file):
    try:
        url = "http://localhost:9000/Modules"
        print("============================================================================================")
        print("============================INSTRUMENT CONFIGURATION========================================")
        print("============================================================================================")
        #Get Module List
        payload = dict(id='0',model='S5040A',address='PXI0::2-0.0::INSTR')
        resp = requests.get(url,data=payload)
        print("Get Module List:"+ str(resp.content)[1:]+"\t Response Code:" + str(resp.status_code))
        url = "http://localhost:9000/Modules/0/"
        
        mytree = ET.parse(r'C:\Users\Administrator\Documents\Keysight\Open RAN Studio\InstrumentConfig.xml')
        myroot = mytree.getroot()
        for neighbor in myroot.iter('TimeSyncConfig'):
            neighbor.find('PtpMode').text = 'Master'
        for neighbor in myroot.iter('PortInfo'):
            NetworkPortName = neighbor.find('NetworkPortName').text
            if NetworkPortName == 'QSFP1_1':
                neighbor.find('OruAddress').text = config_file['ru_mac']

        generate_instrumentconfig = f'{root_dir}\\Scripts\\InstrumentConfig.xml'
        mytree.write(generate_instrumentconfig)
        instrumentconfig = 'C:\\Users\\Administrator\\Documents\\Keysight\\Open RAN Studio\\InstrumentConfig.xml'
        shutil.copyfile(generate_instrumentconfig,instrumentconfig)
        files = {
            'data': (instrumentconfig, open(instrumentconfig, 'rb')),
        }
        resp = requests.post(url+"Configure",files = files)
        print("Load Configuration Status:" + str(resp.content)[1:] +"\t Response Code:" + str(resp.status_code))
        print("Instrument configured successfully")
        print("End.")
        print("============================================================================================")
        return True

    except Exception as e:
        print(f'ORS_instrument_Configuration Error : {e}')
        return f'ORS_instrument_Configuration Error : {e}'
    


if __name__ == "__main__":
    configur = ConfigParser()
    configur.read('{}/Requirement/inputs.ini'.format(root_dir))
    information = configur['INFO']
    status = ORS_instrument_Configuration(information)
    if status == True:
        sys.exit(0)
    else:
        sys.exit(100)
    pass