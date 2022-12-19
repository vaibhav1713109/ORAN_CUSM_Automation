import sys,os,time
from configparser import ConfigParser

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(root_dir)

import clr

sys.path.append("C:\Windows\Microsoft.NET\Framework\\v4.0.30319")
sys.path.append(r"C:\ORAN_AUTOMATION\CUPLANE\Dependencies")

clr.AddReference(f"{root_dir}/Dependencies/Open RAN Studio API.dll")
clr.AddReference(f"{root_dir}/Dependencies/xRAN Configuration.dll")
clr.AddReference(f"{root_dir}/Dependencies/xRAN Transport.dll")
clr.AddReference(f"{root_dir}/Dependencies/Errors Logging Tracing.dll")
# clr.AddReference(f"{root_dir}/Dependencies/Agilent.SA.Vsa.Interfaces.dll")
# clr.AddReference(f"{root_dir}/Dependencies/KalApi.dll")
clr.AddReference(f"{root_dir}/Dependencies/System.Runtime.InteropServices.RuntimeInformation.dll")
clr.AddReference("System")
clr.AddReference("System.Linq")
clr.AddReference("System.Threading.Tasks")
from Keysight.OpenRanStudio import*
from ErrorsLoggingTracing.Exceptions import*
# from Agilent.SA.Vsa import*


def ors_pcap_genration_prach(test_case_name,eAxID,info_section):
	try:
		bandwidth = info_section['bandwidth']
		ru_vlan_id = int(info_section['ru_vlan_id'])
		mtu_size = int(info_section['mtu_size'])
		RU_Name = info_section['ru_name']
		img_version = info_section['img_version']
		muFR1 = int(info_section['numerology(fr1)'][0])
		muFR2 = int(info_section['numerology(fr2)'][0])
		ru_serial_no = info_section['ru_serial_no']
		testing_type = info_section['testing_type']
		report_path = f"{root_dir}/Results/{testing_type}/{RU_Name}/{img_version}/{ru_serial_no}/{bandwidth}/EAXCID{eAxID}/{test_case_name}"
		print(muFR1, muFR2)
		myApi = Api()
		print("- Import Waveform Project (.scp)")
		#The method opens a project file (Signal Studio uses file extension ".scp") previously saved from Keysight Signal Studio. 
		file_name = f"{report_path}\\{test_case_name}.scp"
		myProject = myApi.ImportWaveformProject(file_name)

		print("- Set ORS Configuration")
		myConfig = OrsConfiguration(myProject)

		#Set the flow/eAxC index table size -- Flow_TableSize(DataDirection  dir, int  size )
		# myConfig.Flow_TableSize(OrsConfiguration.DataDirection.DL, 1)  
		myConfig.Flow_TableSize(OrsConfiguration.DataDirection.UL, 1)
		eAxID = int(eAxID, 16)
		print("- eAxID :",eAxID)
		myConfig.Flow_TableEntry(OrsConfiguration.DataDirection.UL, 1, eAxID, 4, 4, 4, 4, OrsConfiguration.UPlaneCmpType.STATIC, OrsConfiguration.UPlaneCmpMethod.NONE, 16)
		# Set slot ID numbering scheme
		myConfig.Numerology_SlotIdNumberingScheme(2, muFR1 = muFR1, muFR2 = muFR2) 

		# Set bandwidth for IQ recovery
		command = f"myConfig.Numerology_RecoverIqFlowBandwidth(OrsConfiguration.Bandwidth.{bandwidth}) "
		exec(f'{command}')

		# Set numerology for IQ recovery
		exec(f"myConfig.Numerology_RecoverIqFlowMu(OrsConfiguration.NumerologyType.Mu{muFR1})")

		myConfig.Numerology_PrachIqOption(True)
		if ('A3' in test_case_name):
			print('- FormatA3 is selected.')
			myConfig.Numerology_PrachPreambleFormat(OrsConfiguration.PRACH_Format.FormatA3)
			myConfig.Numerology_PrachScs(OrsConfiguration.PRACH_SCS.SCS30k)
		elif ('B4' in test_case_name):
			print('- FormatB4 is selected.')
			myConfig.Numerology_PrachPreambleFormat(OrsConfiguration.PRACH_Format.FormatB4)
			myConfig.Numerology_PrachScs(OrsConfiguration.PRACH_SCS.SCS30k)
		elif ('C2' in test_case_name):
			print('- FormatC2 is selected.')
			myConfig.Numerology_PrachPreambleFormat(OrsConfiguration.PRACH_Format.FormatC2)
			myConfig.Numerology_PrachScs(OrsConfiguration.PRACH_SCS.SCS30k)

		# Set the MTU, which impacts how stimulus packets are fragmented (on O-RAN application layer).
		myConfig.Networking_Mtu(mtu_size)  

		# Sets VLAN ID
		myConfig.Options_VlanId(ru_vlan_id) 

		# Sets Beam Forming Method
		myConfig.Beam_Method(OrsConfiguration.BfMethod.DISABLED)

		#Force the full-scale scaler to perform digital power scaling relative to 256QAM disregarding carrier modulation
		myConfig.Options_UseDpsFsFixedHighestQamScaler(True) 

		#myConfig.FlowIdxMap_AddCarrierMapEntry(0, 1) #Add mapping from a carrier (index) to a flow/eAxC ID. This variant is for simple waveforms (no MIMO). --AddCarrierMapEntry  ( int  carrierIdx,  int  flowId,  RAT_T  rat = RAT_T.NR)  
		myConfig.FlowIdxMap_AddCarrierMapEntry(0, eAxID)

		print("- Export Configuration file")
		myApi.ExportStimulus(myConfig)
		#myApi.GenerateBlerXmlFile()
		file_exists = os.path.exists(f"{report_path}\\{test_case_name}.pcap")
		# time.sleep(5)
		if file_exists:
			print("The pcap file exist")
		else:
			Error = "ORS_pcap_genration Error : The pcap file not exists"
			print(Error)
			return Error

		print('The pcap file is successfully generated')
		return True

	except Exception as e:
		print(f'ORS_pcap_genration Error : {e}')
		return f'ORS_pcap_genration Error : {e}'
	
def ors_pcap_genration(test_case_name,eAxID,info_section):
	try:
		bandwidth = info_section['bandwidth']
		dl_cplane_timing = int(info_section['dl_c-plane_timing'])
		dl_uplane_timing = int(info_section['dl_u-plane_timing'])
		ul_c_plane_time = int(info_section['ul_c-plane_time(t1a_cp_ul)'])
		ul_u_plane_time = int(info_section['ul_u-plane_time(ta3_up_ul)'])
		ru_vlan_id = int(info_section['ru_vlan_id'])
		mtu_size = int(info_section['mtu_size'])
		RU_Name = info_section['ru_name']
		img_version = info_section['img_version']
		muFR1 = int(info_section['numerology(fr1)'][0])
		muFR2 = int(info_section['numerology(fr2)'][0])
		comp_type = info_section['compression_type']
		comp_method = info_section['compression method']
		ru_serial_no = info_section['ru_serial_no']
		testing_type = info_section['testing_type']
		report_path = f"{root_dir}/Results/{testing_type}/{RU_Name}/{img_version}/{ru_serial_no}/{bandwidth}/EAXCID{eAxID}/{test_case_name}"
		myApi = Api()
		print("- Import Waveform Project (.scp)")
		#The method opens a project file (Signal Studio uses file extension ".scp") previously saved from Keysight Signal Studio. 
		file_name = f"{report_path}\\{test_case_name}.scp"
		myProject = myApi.ImportWaveformProject(file_name)

		print("- Set ORS Configuration")
		myConfig = OrsConfiguration(myProject)

		#Set the flow/eAxC index table size -- Flow_TableSize(DataDirection  dir, int  size )
		if 'No_Beam' in test_case_name and 'DL' in test_case_name:
			myConfig.Flow_TableSize(OrsConfiguration.DataDirection.DL, 1)
		elif 'No_Beam' in test_case_name and 'UL' in test_case_name:
			myConfig.Flow_TableSize(OrsConfiguration.DataDirection.UL, 1)
		else:
			myConfig.Flow_TableSize(OrsConfiguration.DataDirection.DL, 1)  
			myConfig.Flow_TableSize(OrsConfiguration.DataDirection.UL, 1)

		eAxID = int(eAxID, 16)
		print('- eAxID = ',eAxID)
		#( DataDirection  dir, int  flowIdx, int  eaxcId,  int  duIdBitAlloc,  int  bsIdBitAlloc,  int  ccIdBitAlloc,  int  ruIdBitAlloc,  UPlaneCmpType  cmpType,  UPlaneCmpMethod  cmpMethod,  int  cmpBitwidth,  CUPlaneCoupMethod  coupMethod = CUPlaneCoupMethod.NORMAL )
		if '9' in test_case_name:
			print('- 9 bit compression applied')
			print(f'- compression type = {comp_type}')
			exec(f"myConfig.Flow_TableEntry(OrsConfiguration.DataDirection.DL, 1, eAxID, 4, 4, 4, 4, OrsConfiguration.UPlaneCmpType.{comp_type}, OrsConfiguration.UPlaneCmpMethod.{comp_method}, 9)") # Add an entry to the flow/eAxC index table
			exec(f"myConfig.Flow_TableEntry(OrsConfiguration.DataDirection.UL, 1, eAxID, 4, 4, 4, 4, OrsConfiguration.UPlaneCmpType.{comp_type}, OrsConfiguration.UPlaneCmpMethod.{comp_method}, 9)")
		elif '12' in test_case_name:
			print('- 12 bit compression applied')
			print(f'- compression type = {comp_type}')
			exec(f"myConfig.Flow_TableEntry(OrsConfiguration.DataDirection.DL, 1, eAxID, 4, 4, 4, 4, OrsConfiguration.UPlaneCmpType.{comp_type}, OrsConfiguration.UPlaneCmpMethod.{comp_method}, 12)") 
			exec(f"myConfig.Flow_TableEntry(OrsConfiguration.DataDirection.UL, 1, eAxID, 4, 4, 4, 4, OrsConfiguration.UPlaneCmpType.{comp_type}, OrsConfiguration.UPlaneCmpMethod.{comp_method}, 12)")

		elif '14' in test_case_name:
			print('- 14 bit compression applied')
			print(f'- compression type = {comp_type}')
			exec(f"myConfig.Flow_TableEntry(OrsConfiguration.DataDirection.DL, 1, eAxID, 4, 4, 4, 4, OrsConfiguration.UPlaneCmpType.{comp_type}, OrsConfiguration.UPlaneCmpMethod.{comp_method}, 14)") # Add an entry to the flow/eAxC index table
			exec(f"myConfig.Flow_TableEntry(OrsConfiguration.DataDirection.UL, 1, eAxID, 4, 4, 4, 4, OrsConfiguration.UPlaneCmpType.{comp_type}, OrsConfiguration.UPlaneCmpMethod.{comp_method}, 14)")
		elif 'No_Beam' in test_case_name and 'DL' in test_case_name:
			comp_method = "NONE"
			print('- No compression applied')
			print(f'- compression type = {comp_type}')
			exec(f"myConfig.Flow_TableEntry(OrsConfiguration.DataDirection.DL, 1, eAxID, 4, 4, 4, 4, OrsConfiguration.UPlaneCmpType.{comp_type}, OrsConfiguration.UPlaneCmpMethod.{comp_method}, 16)")
		elif 'No_Beam' in test_case_name and 'UL' in test_case_name:
			comp_method = "NONE"
			print('- No compression applied')
			print(f'- compression type = {comp_type}')
			exec(f"myConfig.Flow_TableEntry(OrsConfiguration.DataDirection.UL, 1, eAxID, 4, 4, 4, 4, OrsConfiguration.UPlaneCmpType.{comp_type}, OrsConfiguration.UPlaneCmpMethod.{comp_method}, 16)")
		else:
			comp_method = "NONE"
			print('- No compression applied')
			print(f'- compression type = {comp_type}')
			exec(f"myConfig.Flow_TableEntry(OrsConfiguration.DataDirection.DL, 1, eAxID, 4, 4, 4, 4, OrsConfiguration.UPlaneCmpType.{comp_type}, OrsConfiguration.UPlaneCmpMethod.{comp_method}, 16)")
			exec(f"myConfig.Flow_TableEntry(OrsConfiguration.DataDirection.UL, 1, eAxID, 4, 4, 4, 4, OrsConfiguration.UPlaneCmpType.{comp_type}, OrsConfiguration.UPlaneCmpMethod.{comp_method}, 16)")

		# Set slot ID numbering scheme
		myConfig.Numerology_SlotIdNumberingScheme(2, muFR1 = muFR1, muFR2 = muFR2) 

		# Set bandwidth for IQ recovery
		command = f"myConfig.Numerology_RecoverIqFlowBandwidth(OrsConfiguration.Bandwidth.{bandwidth}) "
		exec(f'{command}')

		# Set numerology for IQ recovery
		exec(f"myConfig.Numerology_RecoverIqFlowMu(OrsConfiguration.NumerologyType.Mu{muFR1})")

		# Set the MTU, which impacts how stimulus packets are fragmented (on O-RAN application layer).
		myConfig.Networking_Mtu(mtu_size)  

		# Sets VLAN ID
		myConfig.Options_VlanId(ru_vlan_id) 

		# Sets Beam Forming Method
		myConfig.Beam_Method(OrsConfiguration.BfMethod.DISABLED)

		#myconfig.Timing_TcpAdvDl(425000)
		myConfig.Timing_TCpDl(dl_cplane_timing)
		myConfig.Timing_TUpDl(dl_uplane_timing)
		myConfig.Timing_TCpUl(ul_c_plane_time)
		myConfig.Timing_TUpUl(ul_u_plane_time)

		if 'No_Beam' in test_case_name:
			print('- Apply No beam')
			myConfig.Options_IdleGuardFilling(2)

		#Force the full-scale scaler to perform digital power scaling relative to 256QAM disregarding carrier modulation
		myConfig.Options_UseDpsFsFixedHighestQamScaler(True) 

		#myConfig.FlowIdxMap_AddCarrierMapEntry(0, 1) #Add mapping from a carrier (index) to a flow/eAxC ID. This variant is for simple waveforms (no MIMO). --AddCarrierMapEntry  ( int  carrierIdx,  int  flowId,  RAT_T  rat = RAT_T.NR)  
		if 'DL' in test_case_name and 'UL' in test_case_name:
			myConfig.FlowIdxMap_AddCarrierMapEntry(0, eAxID)
			myConfig.FlowIdxMap_AddCarrierMapEntry(1, eAxID)
		else:
			myConfig.FlowIdxMap_AddCarrierMapEntry(0, eAxID)

		print("- Export Configuration file")
		myApi.ExportStimulus(myConfig)
		#myApi.GenerateBlerXmlFile()

		file_exists = os.path.exists(f"{report_path}\\{test_case_name}.pcap")

		# time.sleep(5)
		if file_exists:
			print("- The pcap file exist")
		else:
			Error = "- ORS_pcap_genration Error : The pcap file not exists"
			print(Error)
			return Error

		print('- The pcap file is successfully generated')
		return True

	except Exception as e:
		print(f'ORS_pcap_genration Error : {e}')
		return f'ORS_pcap_genration Error : {e}'
	


if __name__ == "__main__":
	configur = ConfigParser()
	configur.read('{}/Requirement/inputs.ini'.format(root_dir))
	information = configur['INFO']
	start_time = time.time()
	if len(sys.argv)>2:
		if "PRACH" not in sys.argv[1]:
			print(ors_pcap_genration(sys.argv[1],sys.argv[2],information))
		else:
			print(ors_pcap_genration_prach(sys.argv[1],sys.argv[2],information))
	else:
		print('Please run with below format\npython pcap_gen.py {test_case_name} {eAxID}')

	end_time = time.time()
	print(f'\n\nTaken_Time_for_pcap_gen : {end_time-start_time}')
