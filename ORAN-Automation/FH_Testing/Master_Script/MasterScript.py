import pandas as pd
import sys,json
import os,csv
import time, shutil
from configparser import ConfigParser
import subprocess, shutil

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(root_dir)
sys.path.append(root_dir)
from Scripts.Instrument_config import *
from Oran_GUI_Pyqt5.popup import *
from Oran_GUI_Pyqt5.sync_popup import *
from Scripts.generate_report import *


data_xls = pd.read_excel(f'{root_dir}/Requirement/CU_plane_Test_Cases.xlsx', sheet_name='Automation')
def create_ini_file_using_new_df(new_df):
    with open(f'{root_dir}/Master_Script/dummy_inputs.ini', 'w') as file:
        file.write('[INFO]\n')
        # print(new_df.columns)
        test_case_name = ''
        test_case_id = ''
        for column in new_df.columns:
            file.write(f'{column} = {new_df[column].values[0]}\n')
            if column == "Test execution" and new_df[column].values[0] == 'Yes':
                print(new_df["TEST CASE ID"].values[0],new_df["SUMMARY"].values[0],new_df['DL/UL'].values[0])
                test_case_name = new_df["SUMMARY"].values[0]
                test_case_id = new_df["TEST CASE ID"].values[0]
        return test_case_name,test_case_id



if __name__ == "__main__":
    ru_sync = False
    csv_file_data = []
    present_time = time.localtime()
    time_format = time.strftime('%d_%m_%Y_%I_%M_%S_%p',present_time)
    for index, row in data_xls.iterrows():
        new_df = pd.DataFrame(columns=data_xls.columns)
        new_df = pd.concat([new_df, row.to_frame().T], ignore_index=True)
        test_case,test_case_id = create_ini_file_using_new_df(new_df)
        # input("Print check your inputs.ini file")
        ###################################################
        ## Run Master Script
        ###################################################
        if test_case and test_case_id:
            shutil.copyfile(f'{root_dir}/Master_Script/dummy_inputs.ini',f'{root_dir}/Requirement/inputs.ini')
            configur = ConfigParser()
            configur.read('{}/Requirement/inputs.ini'.format(root_dir))
            print('{}/Requirement/inputs.ini'.format(root_dir))
            information = configur['INFO']
            eaxid = information['eaxcids']
            RU_Name = information['ru_name']
            img_version = information['img_version']
            ru_serial_no = information['ru_serial_no']
            if ru_sync == False:
                app = QtWidgets.QApplication([])
                ui = Ui_popup_sync()
                ui.check_sync('Check RU is Sync?')
                if ui.choice == QtWidgets.QMessageBox.Yes:
                    ru_sync = True
                    pass
                else:
                    process1 = subprocess.Popen(["python",'{0}/Scripts/Instrument_config.py'.format(root_dir)])
                    while process1.poll() is None:
                        timeout = True
                    return_code1 = process1.returncode
                    if return_code1!= 0:
                        print('Instrument Configuration are failed...')
                        sys.exit(1)
                    else:
                        ui.choice = QtWidgets.QMessageBox.question(ui,'Extract!',
                                                            "Enter Yes when RU is sync",
                                                            QtWidgets.QMessageBox.Yes)
                        if ui.choice == QtWidgets.QMessageBox.Yes:
                            ru_sync = True
                            pass
            print('Making Directrios for each cases....')
            process2 = subprocess.Popen(["python",'{0}/Scripts/initialisation.py'.format(root_dir),test_case,eaxid])
            while process2.poll() is None:
                timeout = True
            if process2.returncode != 0:
                sys.exit(100090)
            process3 = subprocess.Popen(["python",'{0}/Master_Script/run_all_function.py'.format(root_dir),time_format])
            while process3.poll() is None:
                timeout = True
            if process3.returncode != 0:
                continue
            json_file = f"{root_dir}/Results/{RU_Name}/{img_version}/{ru_serial_no}/EAXCID{eaxid}/Eaxcid_{eaxid}_{time_format}.json"
            csv_file_path = f"{root_dir}/Results/{RU_Name}/{img_version}/{ru_serial_no}/EAXCID{eaxid}/Eaxcid_{eaxid}_{time_format}.csv"
            report_path = f"{root_dir}/Results/{RU_Name}/{img_version}/{ru_serial_no}/EAXCID{eaxid}/Eaxcid_{eaxid}_{time_format}.pdf"
            with open(json_file, 'r') as file:
                DL_UL_Results = json.load(file)
            generate_report_dl_ul(DL_UL_Results,report_path)
            
    present_time = time.localtime()
    time_format = time.strftime('%d_%m_%Y_%I_%M_%S_%p',present_time)
    shutil.copytree(f"{root_dir}/Results/{RU_Name}/{img_version}",f"{root_dir}/Results/{RU_Name}/{img_version}_{time_format}")
    print(f'Logs are saved at location {root_dir}/Results/{RU_Name}/{img_version}_{time_format}')
