import requests
import time,os,sys,clr
from configparser import ConfigParser
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(root_dir)

def play_and_stop_recorder(test_case_name,eAxID,radioframe,config_file):
    try:
        RU_Name = config_file['ru_name']
        img_version = config_file['img_version']
        ru_serial_no = config_file['ru_serial_no']
        testing_type = config_file['testing_type']
        bandwidth = config_file['bandwidth']
        report_path = f"{root_dir}/Results/{testing_type}/{RU_Name}/{img_version}/{ru_serial_no}/{bandwidth}/EAXCID{eAxID}/{test_case_name}"
        filename = f"{report_path}\\{test_case_name}.pcap"
        print(filename)
        url = "http://localhost:9000/Modules/0/"
        payload = dict(state='on', radioframes='0')
        headers = {
        'Content-Type': 'application/json',
        }
        #start Recorder
        if "PRACH" not in test_case_name:
            data = str({"state":"on","radioframes":radioframe})
            resp = requests.put(url+"Recorder",data=data,headers = headers)
            print("Start Recorder Response:" + str(resp.content)[1:]+"\t Response Code:" + str(resp.status_code))
            time.sleep(4)
            while True:
                resp = requests.get(url+"Recorder",data=payload)
                if 'off' in resp.text:
                    print("Recorder State:" + resp.text+"\t Response Code:" + str(resp.status_code))
                    break
                else:
                    time.sleep(2)

        #getRecorder pcap
        file = open(filename[:-5] + "_captured.pcap", "wb")
        resp = requests.get(url+"Recorder/pcap")
        file.write(resp.content)
        file.close()
        print("Copied the Pcap")
        return True
    except Exception as e:
        print(f'play_and_stop_recorder Error : {e}')
        return f'play_and_stop_recorder Error : {e}'
    pass


def Pcap_Load_and_Data_play_record_(test_case_name,eAxID,config_file):
    try:
        radioframe = config_file['radioframes']
        RU_Name = config_file['ru_name']
        img_version = config_file['img_version']
        ru_serial_no = config_file['ru_serial_no']
        testing_type = config_file['testing_type']
        bandwidth = config_file['bandwidth']
        report_path = f"{root_dir}/Results/{testing_type}/{RU_Name}/{img_version}/{ru_serial_no}/{bandwidth}/EAXCID{eAxID}/{test_case_name}"
        if 'PRACH' in test_case_name:
            radioframe = '2'
        print("============================================================================================")
        print("============================PLAYER AND RECORDER FUNCTION====================================")
        print("============================================================================================")

        url = "http://localhost:9000/Modules/0/"

        #url = "http://localhost:9000/Modules/1/"

        #Player Recorder Functions
        filename = f"{report_path}\\{test_case_name}.pcap"
        # print(filename)
        time.sleep(3)
        files = {
        'data': (f"{report_path}\\{test_case_name}_1.pcap", open(filename, 'rb')),
        }
        payload = dict(state='on', radioframes='0')
        headers = {
        'Content-Type': 'application/json',
        }
        
        #load pcap
        resp = requests.post(url+"Player/pcap",files = files)
        print("Load Pcap Status:" + str(resp.content)[1:] +"\t Response Code:" + str(resp.status_code))
        
        #start Recorder
        data = str({"state":"on","radioframes":radioframe})
        resp = requests.put(url+"Recorder",data=data,headers = headers)
        print("Start Recorder Response:" + str(resp.content)[1:]+"\t Response Code:" + str(resp.status_code))
        
        #Get Recorder state
        resp = requests.get(url+"Recorder",data=payload)
        print("Recorder State:" + resp.text+"\t Response Code:" + str(resp.status_code))
        
        #start player
        data = '{"state":"on","radioframes":0}'
        resp = requests.put(url+"Player",data=data,headers = headers)
        # input()
        print("Start Player Response:" + str(resp.content)[1:]+"\t Response Code:" + str(resp.status_code))
        
        # input()
        #Getplayer state
        resp = requests.get(url+"Player",data=payload)
        print("Player State:" + resp.text+"\t Response Code:" + str(resp.status_code))

        time.sleep(3)
        while True:
            resp = requests.get(url+"Recorder",data=payload)
            if 'off' in resp.text:
                print("Recorder State:" + resp.text+"\t Response Code:" + str(resp.status_code))
                break
            else:
                time.sleep(2)

        ## start the recorder again for better results
        time.sleep(10)
        status = play_and_stop_recorder(test_case_name,eAxID,radioframe,config_file)
        if not status:
            return status
        
        print("The Packets are Transmiting ....")
        
        print("============================================================================================")
        print("============================================================================================")
        return True
    except Exception as e:
        print(f'Pcap_Load_and_Data_play_record_ Error : {e}')
        return f'Pcap_Load_and_Data_play_record_ Error : {e}'
    
if __name__ == "__main__":
    configur = ConfigParser()
    configur.read('{}/Requirement/inputs.ini'.format(root_dir))
    information = configur['INFO']
    if len(sys.argv)>2:
        test_case_name = sys.argv[1]
        Pcap_Load_and_Data_play_record_(test_case_name,sys.argv[2],information)
    else:
        print('Please run with below format\npython pcap_load_play_recorde.py {test_case_name} {eaxcid}')