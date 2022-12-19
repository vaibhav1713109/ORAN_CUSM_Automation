import sys,os,time
from configparser import ConfigParser
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(root_dir)

import clr
sys.path.append("C:\Windows\Microsoft.NET\Framework\\v4.0.30319")
sys.path.append(f"{root_dir}/Dependencies")
# clr.AddReference(f"{root_dir}/Dependencies/Agilent.SA.Vsa.Interfaces.dll")
#clr.AddReference(r"C:\ORAN_AUTOMATION1\Dependencies\KalApi.dll")
clr.AddReference(f"{root_dir}\\Dependencies\\Open RAN Studio API.dll")
clr.AddReference(f"{root_dir}/Dependencies/xRAN Configuration.dll")
clr.AddReference(f"{root_dir}/Dependencies/xRAN Transport.dll")
clr.AddReference(f"{root_dir}/Dependencies/Errors Logging Tracing.dll")
clr.AddReference(f"{root_dir}/Dependencies/System.Runtime.InteropServices.RuntimeInformation.dll")
clr.AddReference("System")
clr.AddReference("System.Linq")
clr.AddReference("System.Threading.Tasks")
from Keysight.OpenRanStudio import*
from ErrorsLoggingTracing.Exceptions import*
# from Agilent.SA.Vsa import*


def Generate_ORB_prach(test_case_name,eAxID,config_file):
    try:
        print("============================================================================================")
        print("============================Generate ORB from captured PCAP=================================")
        print("============================================================================================")
        
        
        #Api.ApplicationDirectory = "C:\Program Files\Keysight\Open RAN Studio"
        #Instantiation creates all resources necessary to subsequent API usage.
        RU_Name = config_file['ru_name']
        img_version = config_file['img_version']
        ru_serial_no = config_file['ru_serial_no']
        testing_type = config_file['testing_type']
        bandwidth = config_file['bandwidth']
        report_path = f"{root_dir}/Results/{testing_type}/{RU_Name}/{img_version}/{ru_serial_no}/{bandwidth}/EAXCID{eAxID}/{test_case_name}"
        myApi = Api()
        
        pcap_filename = f"{report_path}\\{test_case_name}_captured.pcap"
        # pcap_filename = f"{report_path}\\captured 2023-09-26--11-26-18.pcap"
        orstx_filename = f"{report_path}\\{test_case_name}.orstx"

        print("- Import PCAP in Explorer")
        myProject = myApi.Explorer(pcap_filename,orstx_filename)
        
        print("- Inspecting eAxID value of the packets")
        index = myProject.GetEaxcId(0)
        print("- eAxID: ", index)
        
        print("- Filter Uplink Packets")
        
        # myProject.FilterPackets(OrsConfiguration.PRACH_SCS.SCS30k, OrsConfiguration.DataDirection.UL, index, FieldTypes.MessageType.U_Plane)
        # myProject.FilterPackets(OrsConfiguration.PRACH_SCS.SCS30k, OrsConfiguration.DataDirection.UL, index, FieldTypes.MessageType.U_Plane)
        myProject.FilterPackets(OrsConfiguration.DataDirection.UL, index, FieldTypes.MessageType.U_Plane)
        save_file = f"{report_path}\\{test_case_name}_recovered_iq"
        print("- Extract Uplink U plane IQ Data")
        carrier_t = myProject.GetCarrierType(0)
        # print(carrier_t)
        myProject.RecoverIQTD(index, OrsConfiguration.DataDirection.UL, save_file,carrier_t)
        #myApi.close()
        print("ORB_Created")
        return True

    except Exception as e:
        print(f'Generate_ORB Error : {e}')
        return f'Generate_ORB Error : {e}'


def Generate_ORB(test_case_name,eAxID,config_file):
    # try:
        print("============================================================================================")
        print("============================Generate ORB from captured PCAP=================================")
        print("============================================================================================")
        
        
        #Api.ApplicationDirectory = "C:\Program Files\Keysight\Open RAN Studio"
        #Instantiation creates all resources necessary to subsequent API usage\
        RU_Name = config_file['ru_name']
        img_version = config_file['img_version']
        ru_serial_no = config_file['ru_serial_no']
        testing_type = config_file['testing_type']
        bandwidth = config_file['bandwidth']
        report_path = f"{root_dir}/Results/{testing_type}/{RU_Name}/{img_version}/{ru_serial_no}/{bandwidth}/EAXCID{eAxID}/{test_case_name}"
        myApi = Api()
        
        pcap_filename = f"{report_path}\\{test_case_name}_captured.pcap"
        orstx_filename = f"{report_path}\\{test_case_name}.orstx"
        print(pcap_filename)
        print(orstx_filename)
        
        print("- Import PCAP in Explorer")
        myProject = myApi.Explorer(pcap_filename,orstx_filename)
        
        print("- Inspecting eAxID value of the packets")
        index = myProject.GetEaxcId(0)
        print("- eAxID: ", index)
        
        print("- Filter Uplink Packets")
        # myProject.FilterPackets(OrsConfiguration.NumerologyType.Mu1, OrsConfiguration.DataDirection.UL, index, FieldTypes.MessageType.U_Plane)
        # myProject.FilterPackets(OrsConfiguration.DataDirection.UL, index, FieldTypes.MessageType.U_Plane)
        myProject.FilterPackets(OrsConfiguration.DataDirection.UL, index, FieldTypes.MessageType.U_Plane)
        
        save_file = f"{report_path}\\{test_case_name}_recovered_iq"
        print("- Extract Uplink U plane IQ Data")
        myProject.RecoverIQTD(index, OrsConfiguration.DataDirection.UL, save_file)
        #myApi.close()
        print("- ORB_Created Successfully")
        return True

    # except Exception as e:
    #     print(f'Generate_ORB Error : {e}')
    #     return f'Generate_ORB Error : {e}'


if __name__ == "__main__":
    configur = ConfigParser()
    configur.read('{}/Requirement/inputs.ini'.format(root_dir))
    information = configur['INFO']
    start_time = time.time()
    print(sys.argv)
    if len(sys.argv)>2:
        if "PRACH" not in sys.argv[1]:
            print(Generate_ORB(sys.argv[1],sys.argv[2],information))
        else:
             print(Generate_ORB_prach(sys.argv[1],sys.argv[2],information))
    else:
        print('Please run with below format\npython orb_gen.py {test_case_name} {eAxID}')

    end_time = time.time()
    print(f'\n\nTaken_Time_for_orb_gen : {end_time-start_time}')
