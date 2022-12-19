import os
from functools import reduce
from configparser import ConfigParser
from tabulate import tabulate
from fpdf.enums import XPos, YPos
from fpdf import FPDF

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dir_name = os.path.dirname(os.path.abspath(__file__))
print(dir_name)


class PDF(FPDF):
    def header(self):
        # Logo
        self.image('{}/vvdn_logo.png'.format(dir_name), 10, 8, 33)
        self.set_text_color(44, 112, 232)
        self.set_font('Times', 'B', 15)
        # self.set_x(-45)
        # self.set_font('Times', 'B', 12)
        # self.cell(10,10, 'ACLR & POWER', 0, 0, 'C')
        self.set_text_color(0, 0, 0)
        self.ln(20)

    # Page footer
    def footer(self):
        self.set_y(-15)
        self.set_font('Times', 'I', 8)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, 'Page %s' % self.page_no(),
                  XPos.RIGHT, new_y=YPos.NEXT, align='L')
        self.set_text_color(44, 112, 232)
        self.set_font('Times', 'B', 10)
        self.cell(0, -10, 'Copyright (c) 2016 - 2022 VVDN Technologies Pvt Ltd',
                  XPos.RIGHT, new_y=YPos.NEXT, align='R')
        self.cell(0, 10)
        self.set_text_color(0, 0, 0)

################# Table Heading ################
def HEADING(PDF, data):
    print('='*100)
    print(data)
    print('='*100)
    PDF.set_font("Times", style='BU', size=20)
    PDF.ln(5)
    PDF.set_text_color(0, 102, 204)
    PDF.multi_cell(w=PDF.epw, txt=data, border=0, align='C')
    PDF.set_text_color(0, 0, 0)
    PDF.ln(5)
    PDF.set_font("Times", style='', size=12)
    pass

################# Add Front Page ################
def PDF_CAP():
    pdf = PDF()
    pdf.add_page(format=(350, 250))
    pdf.set_font("Times", size=9)
    y = int(pdf.epw)
    pdf.image(name='{}/Front_Page.png'.format(dir_name),
              x=None, y=None, w=y, h=0, type='', link='')
    pdf.set_font("Times", style='', size=9)
    # pdf.add_page(format=(350, 250))
    pdf.set_font("Times", size=12)
    pdf.set_font_size(float(10))
    return pdf

def Test_HEADING(PDF, data, *args):
    li = data.split('\n')
    print('-'*100)
    print(data)
    print('-'*100)
    PDF.set_font("Times", style='B', size=11)
    PDF.write(5, li[0])
    PDF.ln(6)
    PDF.set_font("Times", style='', size=11)
    PDF.write(5, li[1])
    PDF.ln(10)

def render_header(PDF, TABLE_Header, line_height, col_width):
    PDF.set_font("Times", style="B")  # enabling bold text
    for col_name in TABLE_Header:
        m_l_h = PDF.font_size
        PDF.multi_cell(w=col_width, h=line_height, txt=col_name, border=1,
                       new_x="RIGHT", new_y="TOP", max_line_height=PDF.font_size, align='C')
    PDF.ln(line_height)
    PDF.set_font("Times", style='', size=11)

def render_table_data(PDF, TABLE_DATA, line_height, col_width, TABLE_Header):  # repeat data rows
    for row in TABLE_DATA:
        if PDF.will_page_break(line_height):
            PDF.set_font("Times", style="B", size=15)
            render_header(PDF, TABLE_Header, line_height, col_width)
            PDF.set_font("Times", style="", size=11)
        for datum in row:
            if datum == 'Pass':
                PDF.set_fill_color(105, 224, 113)
            elif datum == 'Fail':
                PDF.set_fill_color(235, 52, 52)
            else:
                PDF.set_fill_color(255, 255, 255)
            PDF.multi_cell(w=col_width, h=line_height, txt=datum, border=1,
                           new_x="RIGHT", new_y="TOP", max_line_height=PDF.font_size, align='C', fill=True)
        PDF.ln(line_height)

def add_ul_image(PDF, Images):
    y = int(PDF.epw)
    i = 0
    PDF.add_page(format=(350, 250))
    for key, val in Images.items():
        i += 1
        PDF.set_y(30)
        PDF.set_font("Times", style='B', size=15)
        PDF.multi_cell(w=PDF.epw, txt='Channel {}'.format(
            key), border=0, align='C')
        for img in val:
            PDF.image(img, 20, 40, 300)
            PDF.add_page(format=(350, 250))
        PDF.set_font("Times", style='', size=11)
        pass
    PDF.set_font("Times", style='', size=9)
    pass

def add_image(PDF, Images:dict):
    i = 0
    for key,image in Images.items():
        if os.path.exists(image):
            i+=1
            PDF.set_y(30)
            PDF.set_font("Times", style='B', size=15)
            PDF.multi_cell(w=PDF.epw, txt=f'SS CH{key}', border=0, align='C')
            PDF.ln(10)
            PDF.image(image, 20, 40, 300)
            if i < len(Images):
                PDF.add_page(format=(350, 250))
            PDF.set_font("Times", style='', size=11)
        else:
            print(f"ScreenShot not append for {image}")
            PDF.write(h=5, txt=f"\nScreenShot not append for {image}")

def check_crc_pass_fail(PDF, ResultData, line_height):
    line_height = 5
    crc_pass = crc_fail = 0
    Header = ['Channel', 'Slot', 'CRC Passed', 'Bit Length']
    for lines in ResultData[-1]:
        if lines[2] == 'True':
            crc_pass += 1
        elif lines[2] == 'False':
            crc_fail += 1
    PDF.set_y(30)
    PDF.set_font("Times", style='B', size=15)
    PDF.multi_cell(w=PDF.epw, txt=f'{ResultData[0]} CH{ResultData[1]} CRC Table', border=0, align='C')
    PDF.ln(10)
    render_header(PDF, Header, line_height, PDF.epw / len(Header))
    PDF.set_font("Times", style='', size=11)
    render_table_data(
        PDF, ResultData[-1], line_height, PDF.epw / len(Header), Header)
    PDF.ln(10)
    PDF.set_font("Times", style='B', size=15)
    PDF.multi_cell(w=PDF.epw, txt='CRC PASS : {0} || CRC FAIL : {1}'.format(
        crc_pass, crc_fail), border=0, align='C')
    PDF.set_font("Times", style='', size=11)
    pass

def check_ul_crc_pass_fail(PDF, ResultData):
    crc_pass = crc_fail = 0
    PDF.set_y(30)
    PDF.set_font("Times", style='B', size=15)
    PDF.multi_cell(w=PDF.epw, txt=f'{ResultData[0]} CH{ResultData[1]} CRC Table', border=0, align='C')
    PDF.ln(10)
    PDF.set_font("Times", style='', size=11)
    for val in ResultData[-1]:
        PDF.write(h=5, txt=val)
        PDF.ln(5)
        if 'CRC=Fail' in val:
            crc_fail += 1
        elif 'CRC=Pass' in val:
            crc_pass += 1
    PDF.ln(10)
    PDF.set_font("Times", style='B', size=15)
    PDF.multi_cell(w=PDF.epw, txt='CRC PASS : {0} || CRC FAIL : {1}'.format(
        crc_pass, crc_fail), border=0, align='C')
    PDF.set_font("Times", style='', size=11)

def test_report_dl(PDF,table_data_dl,line_height,crc_data_dl,screen_shot_dl):
    ##################################################################################################################
    #                                     Add DL Data into the report                                                #
    ##################################################################################################################
    HEADING(PDF, f'\n Test Report DL \n')
    DL_Header = ["Test Case",'Channel No', 'Channel Frequency [GHz]', 'BS Channel Bandwidth [MHz]',
            'Measured EVM (RMS) [%]', 'EVM Limit [%]', 'Output Power [dBm]', 'Limit Low [dBm]', 'High Low [dBm]', 'Verdict']
    Test_HEADING(PDF, f'''Test purpose : \nThe test purpose is to verify the DL test.''')
    Test_HEADING(PDF, 'Test environment : \nNormal test conditions.')
    PDF.set_font("Times",style = '',size = 11)
    render_header(PDF, DL_Header, line_height, PDF.epw / len(DL_Header))
    render_table_data(PDF, table_data_dl, line_height, PDF.epw / len(DL_Header), DL_Header)
    PDF.add_page(format=(350, 250))
    print(crc_data_dl)
    for data in crc_data_dl:
        check_crc_pass_fail(PDF,data,line_height-3)
        PDF.add_page(format=(350, 250))
    for images in screen_shot_dl:
        if os.path.exists(images[-1]):
            PDF.set_y(30)
            PDF.set_font("Times", style='B', size=15)
            PDF.multi_cell(w=PDF.epw, txt=f'SS {images[0]} CH{images[1]}', border=0, align='C')
            PDF.ln(10)
            PDF.image(images[-1], 20, 40, 300)
            PDF.add_page(format=(350, 250))
            PDF.set_font("Times", style='', size=11)
        else:
            print(f"ScreenShot not append for {images[-1]}")
            PDF.write(h=5, txt=f"\nScreenShot not append for {images[-1]}")
        
def test_report_ul(PDF,table_data_ul,line_height,crc_data_ul,screen_shot_ul):
    HEADING(PDF, f'\n Test Report UL \n')
    UL_Header = ["Test Case",'Channel No', 'Channel Frequency [GHz]', 'BS Channel Bandwidth [MHz]',
                        'Measured EVM (RMS) [%]', 'EVM Limit [%]','Verdict']
    Test_HEADING(PDF, f'''Test purpose : \nThe test purpose is to verify the UL test.''')
    Test_HEADING(PDF, 'Test environment : \nNormal test conditions.')
    PDF.set_font("Times",style = '',size = 11)
    render_header(PDF, UL_Header, line_height, PDF.epw / len(UL_Header))
    render_table_data(PDF, table_data_ul, line_height, PDF.epw / len(UL_Header), UL_Header)
    PDF.add_page(format=(350, 250))
    for data in crc_data_ul:
        check_ul_crc_pass_fail(PDF,data)
        PDF.add_page(format=(350, 250))
    for images in screen_shot_ul:
        for image in images[-2:]:
            if os.path.exists(image):
                PDF.set_y(30)
                PDF.set_font("Times", style='B', size=15)
                PDF.multi_cell(w=PDF.epw, txt=f'SS {images[0]} CH{images[1]}', border=0, align='C')
                PDF.ln(10)
                PDF.image(image, 20, 40, 300)
                PDF.add_page(format=(350, 250))
                PDF.set_font("Times", style='', size=11)
            else:
                print(f"ScreenShot not append for {image}")
                PDF.write(h=5, txt=f"\nScreenShot not append for {image}")

def generate_report_dl_ul(Result, report_path,info_file):
    PDF = PDF_CAP()
    Header_H = PDF.font_size * 2.5
    line_height = PDF.font_size * 3.5
    PDF.ln(10)
    HEADING(PDF, '\n CU Plane Test report \n')
    PDF.ln(10)
    hw_serial_no = info_file['ru_serial_no']
    Product_Name = info_file['ru_name']
    ru_mac = info_file['ru_mac']
    sw_ver = info_file['img_version']
    ru_table_header = ['Hw S. No.', "Product Name", "RU Mac", 'SW Version']
    ru_table_data = [[hw_serial_no, Product_Name, ru_mac, sw_ver]]
    render_header(PDF, ru_table_header, line_height,
                  PDF.epw / len(ru_table_header))
    render_table_data(PDF, ru_table_data, line_height,
                      PDF.epw / len(ru_table_header), ru_table_header)
    PDF.add_page(format=(350, 250))
    # table_header = ['S. No.', "Test Case", "Verdict"]
    table_data_dl = []
    screen_shot_dl = []
    crc_data_dl = []
    table_data_ul = []
    crc_data_ul = []
    screen_shot_ul = []
    all_verdict_table = []
    i = 1
    dl_pass_flag = ul_pass_flag = pass_flag = False
    for key, vals in Result.items():
        if 'DL' in key and 'UL' in key:
            for val in vals[0]:
                val.insert(0,key)
                table_data_dl.append(val[:-2])
                crc_data_dl.append([key,val[1],val[-1]])
                screen_shot_dl.append([key,val[1],val[-2]])
                if 'Pass' in val[:-2]:
                    dl_pass_flag = True
                else:
                    dl_pass_flag = False
            for val in vals[1]:
                val.insert(0,key)
                table_data_ul.append(val[:-2])
                crc_data_ul.append([key,val[1],val[-1]])
                image_name_1 = f'{val[-2]}/VSA_Screenshot_1.gif'
                image_name_2 = f'{val[-2]}/VSA_Screenshot_2.gif'
                screen_shot_ul.append([key,val[1],image_name_1,image_name_2])
                if 'Pass' in val[:-2]:
                    ul_pass_flag = True
                else:
                    ul_pass_flag = False
            all_verdict_table.append([key,'Pass' if dl_pass_flag and ul_pass_flag else 'Fail'])
        elif "DL" in key:
            for val in vals[0]:
                val.insert(0,key)
                table_data_dl.append(val[:-2])
                crc_data_dl.append([key,val[1],val[-1]])
                screen_shot_dl.append([key,val[1],val[-2]])
                if 'Pass' in val[:-2]:
                    pass_flag = True
                else:
                    pass_flag = False
            all_verdict_table.append([key,'Pass' if pass_flag else 'Fail'])
        elif 'UL' in key:
            for val in vals[0]:
                val.insert(0,key)
                table_data_ul.append(val[:-2])
                crc_data_ul.append([key,val[1],val[-1]])
                image_name_1 = f'{val[-2]}/VSA_Screenshot_1.gif'
                image_name_2 = f'{val[-2]}/VSA_Screenshot_2.gif'
                screen_shot_ul.append([key,val[1],image_name_1,image_name_2])
                if 'Pass' in val[:-2]:
                    pass_flag = True
                else:
                    pass_flag = False
            all_verdict_table.append([key,'Pass' if pass_flag else 'Fail'])
    
    HEADING(PDF, f'\n Test Report \n')
    header = ['Test Case','Verdict']
    render_header(PDF, header, line_height, PDF.epw / len(header))
    render_table_data(PDF, all_verdict_table, line_height, PDF.epw / len(header), header)
    PDF.add_page(format=(350, 250))
    if 'DL' in key and 'UL' in key:
        test_report_dl(PDF,table_data_dl,line_height,crc_data_dl,screen_shot_dl)
        PDF.add_page(format=(350, 250))
        test_report_ul(PDF,table_data_ul,line_height,crc_data_ul,screen_shot_ul)
    elif "DL" in key:
        test_report_dl(PDF,table_data_dl,line_height,crc_data_dl,screen_shot_dl)
    elif 'UL' in key:
        test_report_ul(PDF,table_data_ul,line_height,crc_data_ul,screen_shot_ul)
    print(f"Report save at {report_path}")
    PDF.output(f"{report_path}")

def genrate_report_evm(Result:list,report_path:str):
    PDF = PDF_CAP()
    Header_H = PDF.font_size * 2.5
    line_height = PDF.font_size * 3.5
    images = {}
    for data in Result:
        file_status = os.path.exists(data[-1])
        if file_status:
            images[f"{data[0]}_{data[1]}_{data[2]}"] = data[-1]
        data.pop()
    print('\n\n\n')
    PDF.add_page(format=(350, 250))
    HEADING(PDF, f'\n Test Report EVM & Power \n')
    DL_Header = ['Channel No', 'Channel Frequency [GHz]', 'BS Channel Bandwidth [MHz]',
                        'Measured EVM (RMS) [%]', 'EVM Limit [%]','Channel Power (dBm)', 'Lower Limit (dBm)','Upper Limit (dBm)','Verdict']
    Test_HEADING(PDF, f'''Test purpose : \nThe test purpose is to verify the EVM and Power.''')
    Test_HEADING(PDF, 'Test environment : \nNormal test conditions.')
    PDF.set_font("Times",style = '',size = 11)
    render_header(PDF, DL_Header, line_height, PDF.epw / len(DL_Header))
    render_table_data(PDF, Result, line_height, PDF.epw / len(DL_Header), DL_Header)
    PDF.add_page(format=(350, 250))
    print(images)
    add_image(PDF,images)
    PDF.output(f"{report_path}")
    pass

def genrate_report_aclr(Result:list,report_path:str):
    PDF = PDF_CAP()
    Header_H = PDF.font_size * 2.5
    line_height = PDF.font_size * 3.5
    images = {}
    for data in Result:
        file_status = os.path.exists(data[-1])
        if file_status:
            images[f"{data[0]}_{data[1]}_{data[2]}"] = data[-1]
        data.pop()
    print('\n\n\n')
    PDF.add_page(format=(350, 250))
    HEADING(PDF, '\n Downlink Report - Adjacent Channel leakage power ratio: \n')
    Header = ["Channel No.",'Channel Frequency [GHz]', 'BS Channel Bandwidth BW [MHz]',
                'ACLR Lower', 'ACLR Upper', 'ACLR Limit', 'Verdict']
    Test_HEADING(PDF, '''Test purpose : \nThe test purpose is to verify the DL Test''')
    Test_HEADING(PDF, 'Test environment : \nNormal test conditions.')
    # print(tabulate(Result[2], headers=Header, stralign='left',maxcolwidths=[10, 10, 10, 10, 10, 10, 10], tablefmt='fancy_grid'))
    PDF.set_font("Times",style = '',size = 11)
    render_header(PDF, Header, line_height, PDF.epw / len(Header))
    print(Result)
    render_table_data(PDF, Result, line_height, PDF.epw / len(Header), Header)
    PDF.add_page(format=(350, 250))
    print(images)
    add_image(PDF,images)
    PDF.output(f"{report_path}")
    pass

def genrate_report_ccdf(Result:list,report_path:str):
    PDF = PDF_CAP()
    Header_H = PDF.font_size * 2.5
    line_height = PDF.font_size * 3.5
    images = {}
    for data in Result:
        file_status = os.path.exists(data[-1])
        if file_status:
            images[f"{data[0]}_{data[1]}_{data[2]}"] = data[-1]
        data.pop()
    print('\n\n\n')
    PDF.add_page(format=(350, 250))
    HEADING(PDF, '\n Downlink Report - Adjacent Channel leakage power ratio: \n')
    Header = ["Channel No.",'Channel Frequency [GHz]', 'BS Channel Bandwidth BW [MHz]',
                'CCDF [%]', 'CCDF Limit', 'Verdict']
    Test_HEADING(PDF, '''Test purpose : \nThe test purpose is to verify the DL Test''')
    Test_HEADING(PDF, 'Test environment : \nNormal test conditions.')
    # print(tabulate(Result[2], headers=Header, stralign='left',maxcolwidths=[10, 10, 10, 10, 10, 10, 10], tablefmt='fancy_grid'))
    PDF.set_font("Times",style = '',size = 11)
    render_header(PDF, Header, line_height, PDF.epw / len(Header))
    print(Result)
    render_table_data(PDF, Result, line_height, PDF.epw / len(Header), Header)
    PDF.add_page(format=(350, 250))
    print(images)
    add_image(PDF,images)
    PDF.output(f"{report_path}")
    pass

def genrate_report_freq_error(Result:list,report_path:str):
    PDF = PDF_CAP()
    Header_H = PDF.font_size * 2.5
    line_height = PDF.font_size * 3.5
    images = {}
    for data in Result:
        file_status = os.path.exists(data[-1])
        if file_status:
            images[data[0]] = data[-1]
        data.pop()
    print('\n\n\n')
    HEADING(PDF, '\n Downlink Report - Frequency Error: \n')
    Header = ['Channel Frequency [GHz]', 'BS Channel Bandwidth BW [MHz]',
                'Frequency Error [RMS] Hz', 'Frequency Error Limit[Hz]', 'Verdict']
    Test_HEADING(PDF, '''Test purpose : \nThe test purpose is to verify the DL Test''')
    Test_HEADING(PDF, 'Test environment : \nNormal test conditions.')
    # print(tabulate(Result[2], headers=Header, stralign='left',maxcolwidths=[10, 10, 10, 10, 10, 10, 10], tablefmt='fancy_grid'))
    PDF.set_font("Times",style = '',size = 11)
    render_header(PDF, Header, line_height, PDF.epw / len(Header))
    print(Result)
    render_table_data(PDF, Result, line_height, PDF.epw / len(Header), Header)
    # PDF.add_page(format=(350, 250))
    print(images)
    add_image(PDF,images)
    PDF.output(f"{report_path}")

def genrate_report_bs_power(Result:list,report_path:str):
    PDF = PDF_CAP()
    Header_H = PDF.font_size * 2.5
    line_height = PDF.font_size * 3.5
    images = {}
    for data in Result:
        file_status = os.path.exists(data[-1])
        if file_status:
            images[f"{data[0]}_{data[1]}_{data[2]}"] = data[-1]
        data.pop()
    print('\n\n\n')
    HEADING(PDF, '\n Downlink Report - Base Station Output Power: \n')
    Header = ['Channel','Channel Frequency [GHz]', 'SB Channel Bandwidth BW [MHz]',
                'BS Power', 'Power Limit', 'Power Limit', 'Verdict']
    Test_HEADING(PDF, '''Test purpose : \nThe test purpose is to verify the DL Test''')
    Test_HEADING(PDF, 'Test environment : \nNormal test conditions.')
    # print(tabulate(Result[2], headers=Header, stralign='left',maxcolwidths=[10, 10, 10, 10, 10, 10, 10], tablefmt='fancy_grid'))
    PDF.set_font("Times",style = '',size = 11)
    render_header(PDF, Header, line_height, PDF.epw / len(Header))
    print(Result)
    render_table_data(PDF, Result, line_height, PDF.epw / len(Header), Header)
    # PDF.add_page(format=(350, 250))
    print(images)
    add_image(PDF,images)
    PDF.output(f"{report_path}")
    pass

def genrate_report_ocuupied_bandwidth(Result:list,report_path:str):
    PDF = PDF_CAP()
    Header_H = PDF.font_size * 2.5
    line_height = PDF.font_size * 3.5
    images = {}
    for data in Result:
        file_status = os.path.exists(data[-1])
        if file_status:
            images[f"{data[0]}_{data[1]}_{data[2]}"] = data[-1]
        data.pop()
    print('\n\n\n')
    HEADING(PDF, '\n Downlink Report -  Occupied Bandwidth: \n')
    Header = ['Channel','Channel Frequency [GHz]', 'BS Channel Bandwidth BW [mHz]',
                'Measured Occupied Bandwidth [mHz]','Verdict']
    Test_HEADING(PDF, '''Test purpose : \nThe test purpose is to verify the RCT Occupied Bandwidth Test''')
    Test_HEADING(PDF, 'Test environment : \nNormal test conditions.')
    # print(tabulate(Result[2], headers=Header, stralign='left',maxcolwidths=[10, 10, 10, 10, 10, 10, 10], tablefmt='fancy_grid'))
    PDF.set_font("Times",style = '',size = 11)
    render_header(PDF, Header, line_height, PDF.epw / len(Header))
    print(Result)
    render_table_data(PDF, Result, line_height, PDF.epw / len(Header), Header)
    # PDF.add_page(format=(350, 250))
    print(images)
    add_image(PDF,images)
    PDF.output(f"{report_path}")

def genrate_report_OBUE(Result:list,report_path:str):
    PDF = PDF_CAP()
    Header_H = PDF.font_size * 2.5
    line_height = PDF.font_size * 3.5
    images = {}
    for data in Result:
        file_status = os.path.exists(data[-1])
        if file_status:
            images[data[0]] = data[-1]
        data.pop()
    print('\n\n\n')
    HEADING(PDF, '\n Downlink Report -  Occupied Bandwidth Unwanted Emmision: \n')
    Header = ['Channel Frequency [GHz]', 'BS Channel Bandwidth BW [mHz]',
              '50khz-5.050mhz','5.050mhz-10.05mhz','10.05mhz-40.00mhz',
              '40.00mhz-100.00mhz','100mhz-500mhz','Verdict']
    Test_HEADING(PDF, '''Test purpose : \nThe test purpose is to verify the RCT Occupied Bandwidth Unwanted Emmision Test''')
    Test_HEADING(PDF, 'Test environment : \nNormal test conditions.')
    # print(tabulate(Result[2], headers=Header, stralign='left',maxcolwidths=[10, 10, 10, 10, 10, 10, 10], tablefmt='fancy_grid'))
    PDF.set_font("Times",style = '',size = 11)
    render_header(PDF, Header, line_height, PDF.epw / len(Header))
    print(Result)
    render_table_data(PDF, Result, line_height, PDF.epw / len(Header), Header)
    # PDF.add_page(format=(350, 250))
    print(images)
    add_image(PDF,images)
    PDF.output(f"{report_path}")
      
def genrate_report_t_on_off_p(Result:list,report_path:str):
    PDF = PDF_CAP()
    Header_H = PDF.font_size * 2.5
    line_height = PDF.font_size * 3.5
    images = {}
    for data in Result:
        file_status = os.path.exists(data[-1])
        if file_status:
            images[data[0]] = data[-1]
        data.pop()
    print('\n\n\n')
    HEADING(PDF, '\n Downlink Report -  : \n')
    Header = ['Channel Frequency [GHz]', 'BS Channel Bandwidth BW [mHz]',
                'Measured Occupied Bandwidth [mHz]','Verdict']
    Test_HEADING(PDF, '''Test purpose : \nThe test purpose is to verify the RCT Occupied Bandwidth Unwanted Emmision Test''')
    Test_HEADING(PDF, 'Test environment : \nNormal test conditions.')
    # print(tabulate(Result[2], headers=Header, stralign='left',maxcolwidths=[10, 10, 10, 10, 10, 10, 10], tablefmt='fancy_grid'))
    PDF.set_font("Times",style = '',size = 11)
    render_header(PDF, Header, line_height, PDF.epw / len(Header))
    print(Result)
    render_table_data(PDF, Result, line_height, PDF.epw / len(Header), Header)
    # PDF.add_page(format=(350, 250))
    print(images)
    add_image(PDF,images)
    PDF.output(f"{report_path}")



if __name__ == "__main__":
    configur = ConfigParser()
    configur.read('{}/Requirement/inputs.ini'.format(root_dir))
    information = configur['INFO']
    # report_path = r'C:\Automation\radi_bn28\ORAN-Automation\CUPLANE\Scripts\DL_report.pdf'
    report_path = r"C:\Automation\FH_Testing\Results\CUPLANE\LPRU_v2\1.0.19\22082142000036\FR1_100M\EAXCID1\test.pdf"
    Result = {
        "Base_DL_UL": [
            [
                [
                    "2",
                    "3.700005",
                    "100",
                    "2.62",
                    "3.5",
                    "24.33",
                    "23.0",
                    "24.7",
                    "Pass",
                    "C:\\Automation\\radi_bn28\\ORAN-Automation\\CUPLANE\\Results\\LPRUD_4T4R\\2.0.7\\EAXCID2\\Base_DL_UL\\VXT_capture.png",
                    [
                        [
                            "#6317395Channel",
                            "Slot",
                            "CRC Passed",
                            "Bit Length"
                        ],
                        [
                            "PDSCH 1",
                            "0",
                            "True",
                            "84240"
                        ],
                        [
                            "PDSCH 1",
                            "1",
                            "True",
                            "84240"
                        ],
                        [
                            "PDSCH 1",
                            "2",
                            "True",
                            "84240"
                        ],
                        [
                            "PDSCH 1",
                            "3",
                            "True",
                            "84240"
                        ],
                        [
                            "PDSCH 1",
                            "4",
                            "True",
                            "84240"
                        ],
                        [
                            "PDSCH 1",
                            "5",
                            "True",
                            "84240"
                        ],
                        [
                            "PDSCH 1",
                            "6",
                            "True",
                            "84240"
                        ],
                        [
                            "PDSCH 1",
                            "10",
                            "True",
                            "84240"
                        ],
                        [
                            "PDSCH 1",
                            "11",
                            "True",
                            "84240"
                        ],
                        [
                            "PDSCH 1",
                            "12",
                            "True",
                            "84240"
                        ],
                        [
                            "PDSCH 1",
                            "13",
                            "True",
                            "84240"
                        ],
                        [
                            "PDSCH 1",
                            "14",
                            "True",
                            "84240"
                        ],
                        [
                            "PDSCH 1",
                            "15",
                            "True",
                            "84240"
                        ],
                        [
                            "PDSCH 1",
                            "16",
                            "True",
                            "84240"
                        ],
                        [
                            "PDSCH 2",
                            "0",
                            "True",
                            "792"
                        ],
                        [
                            "PDSCH 2",
                            "1",
                            "True",
                            "792"
                        ],
                        [
                            "PDSCH 2",
                            "2",
                            "True",
                            "792"
                        ],
                        [
                            "PDSCH 2",
                            "3",
                            "True",
                            "792"
                        ],
                        [
                            "PDSCH 2",
                            "4",
                            "True",
                            "792"
                        ],
                        [
                            "PDSCH 2",
                            "5",
                            "True",
                            "792"
                        ],
                        [
                            "PDSCH 2",
                            "6",
                            "True",
                            "792"
                        ],
                        [
                            "PDSCH 2",
                            "10",
                            "True",
                            "792"
                        ],
                        [
                            "PDSCH 2",
                            "11",
                            "True",
                            "792"
                        ],
                        [
                            "PDSCH 2",
                            "12",
                            "True",
                            "792"
                        ],
                        [
                            "PDSCH 2",
                            "13",
                            "True",
                            "792"
                        ],
                        [
                            "PDSCH 2",
                            "14",
                            "True",
                            "792"
                        ],
                        [
                            "PDSCH 2",
                            "15",
                            "True",
                            "792"
                        ],
                        [
                            "PDSCH 2",
                            "16",
                            "True",
                            "792"
                        ],
                        [
                            "PDSCH 3",
                            "7",
                            "True",
                            "35640"
                        ],
                        [
                            "PDSCH 3",
                            "17",
                            "True",
                            "35640"
                        ],
                        [
                            "PDSCH 4",
                            "7",
                            "True",
                            "252"
                        ],
                        [
                            "PDSCH 4",
                            "17",
                            "True",
                            "252"
                        ],
                        [
                            "PDCCH 1",
                            "0",
                            "True",
                            "108"
                        ],
                        [
                            "PDCCH 1",
                            "1",
                            "True",
                            "108"
                        ],
                        [
                            "PDCCH 1",
                            "2",
                            "True",
                            "108"
                        ],
                        [
                            "PDCCH 1",
                            "3",
                            "True",
                            "108"
                        ],
                        [
                            "PDCCH 1",
                            "4",
                            "True",
                            "108"
                        ],
                        [
                            "PDCCH 1",
                            "5",
                            "True",
                            "108"
                        ],
                        [
                            "PDCCH 1",
                            "6",
                            "True",
                            "108"
                        ],
                        [
                            "PDCCH 1",
                            "7",
                            "True",
                            "108"
                        ],
                        [
                            "PDCCH 1",
                            "10",
                            "True",
                            "108"
                        ],
                        [
                            "PDCCH 1",
                            "11",
                            "True",
                            "108"
                        ],
                        [
                            "PDCCH 1",
                            "12",
                            "True",
                            "108"
                        ],
                        [
                            "PDCCH 1",
                            "13",
                            "True",
                            "108"
                        ],
                        [
                            "PDCCH 1",
                            "14",
                            "True",
                            "108"
                        ],
                        [
                            "PDCCH 1",
                            "15",
                            "True",
                            "108"
                        ],
                        [
                            "PDCCH 1",
                            "16",
                            "True",
                            "108"
                        ],
                        [
                            "PDCCH 1",
                            "17",
                            "True",
                            "108"
                        ]
                    ]
                ]
            ],
            [
                [
                    "2",
                    "3.700005",
                    "100",
                    "1.744832992553711",
                    "3.5",
                    "Fail",
                    "C:\\Automation\\radi_bn28\\ORAN-Automation\\CUPLANE\\Results\\LPRUD_4T4R\\2.0.7\\EAXCID2\\Base_DL_UL",
                    [
                        "PUCCH Decoder : Off",
                        "PUSCH Decoder : On",
                        "PUSCH_0_IE : PUSCH Index=0, CarrierIndex=0, BWPIndex=0",
                        "PUSCH_F0_IE : Codeword=0, SlotIndex=08, RV Index=0, EffectiveCodeRate=0.6616, CRC=Pass , Number Of Code Blocks: 2",
                        "PUSCH_F1_IE : Codeword=0, SlotIndex=09, RV Index=0, EffectiveCodeRate=0.6616, CRC=Pass , Number Of Code Blocks: 2",
                        "PUSCH_F2_IE : Codeword=0, SlotIndex=18, RV Index=0, EffectiveCodeRate=0.6616, CRC=Pass , Number Of Code Blocks: 2",
                        "PUSCH_F3_IE : Codeword=0, SlotIndex=19, RV Index=0, EffectiveCodeRate=0.6616, CRC=Pass , Number Of Code Blocks: 2",
                        "PUSCH_1_IE : PUSCH Index=1, CarrierIndex=0, BWPIndex=0",
                        "PUSCH_F4_IE : Codeword=0, SlotIndex=07, RV Index=0, EffectiveCodeRate=0.6776, CRC=Pass , Number Of Code Blocks: 1",
                        "PUSCH_F5_IE : Codeword=0, SlotIndex=17, RV Index=0, EffectiveCodeRate=0.6776, CRC=Pass , Number Of Code Blocks: 1"
                    ]
                ]
            ]
        ],
        "Extended_DL_UL": [
            [
                [
                    "2",
                    "3.700005",
                    "100",
                    "2.41",
                    "3.5",
                    "24.35",
                    "23.0",
                    "24.7",
                    "Pass",
                    "C:\\Automation\\radi_bn28\\ORAN-Automation\\CUPLANE\\Results\\LPRUD_4T4R\\2.0.7\\EAXCID2\\Extended_DL_UL\\VXT_capture.png",
                    [
                        [
                            "#6317395Channel",
                            "Slot",
                            "CRC Passed",
                            "Bit Length"
                        ],
                        [
                            "PDSCH 1",
                            "0",
                            "True",
                            "84240"
                        ],
                        [
                            "PDSCH 1",
                            "1",
                            "True",
                            "84240"
                        ],
                        [
                            "PDSCH 1",
                            "2",
                            "True",
                            "84240"
                        ],
                        [
                            "PDSCH 1",
                            "3",
                            "True",
                            "84240"
                        ],
                        [
                            "PDSCH 1",
                            "4",
                            "True",
                            "84240"
                        ],
                        [
                            "PDSCH 1",
                            "5",
                            "True",
                            "84240"
                        ],
                        [
                            "PDSCH 1",
                            "6",
                            "True",
                            "84240"
                        ],
                        [
                            "PDSCH 1",
                            "10",
                            "True",
                            "84240"
                        ],
                        [
                            "PDSCH 1",
                            "11",
                            "True",
                            "84240"
                        ],
                        [
                            "PDSCH 1",
                            "12",
                            "True",
                            "84240"
                        ],
                        [
                            "PDSCH 1",
                            "13",
                            "True",
                            "84240"
                        ],
                        [
                            "PDSCH 1",
                            "14",
                            "True",
                            "84240"
                        ],
                        [
                            "PDSCH 1",
                            "15",
                            "True",
                            "84240"
                        ],
                        [
                            "PDSCH 1",
                            "16",
                            "True",
                            "84240"
                        ],
                        [
                            "PDSCH 2",
                            "0",
                            "True",
                            "792"
                        ],
                        [
                            "PDSCH 2",
                            "1",
                            "True",
                            "792"
                        ],
                        [
                            "PDSCH 2",
                            "2",
                            "True",
                            "792"
                        ],
                        [
                            "PDSCH 2",
                            "3",
                            "True",
                            "792"
                        ],
                        [
                            "PDSCH 2",
                            "4",
                            "True",
                            "792"
                        ],
                        [
                            "PDSCH 2",
                            "5",
                            "True",
                            "792"
                        ],
                        [
                            "PDSCH 2",
                            "6",
                            "True",
                            "792"
                        ],
                        [
                            "PDSCH 2",
                            "10",
                            "True",
                            "792"
                        ],
                        [
                            "PDSCH 2",
                            "11",
                            "True",
                            "792"
                        ],
                        [
                            "PDSCH 2",
                            "12",
                            "True",
                            "792"
                        ],
                        [
                            "PDSCH 2",
                            "13",
                            "True",
                            "792"
                        ],
                        [
                            "PDSCH 2",
                            "14",
                            "True",
                            "792"
                        ],
                        [
                            "PDSCH 2",
                            "15",
                            "True",
                            "792"
                        ],
                        [
                            "PDSCH 2",
                            "16",
                            "True",
                            "792"
                        ],
                        [
                            "PDSCH 3",
                            "7",
                            "True",
                            "35640"
                        ],
                        [
                            "PDSCH 3",
                            "17",
                            "True",
                            "35640"
                        ],
                        [
                            "PDSCH 4",
                            "7",
                            "True",
                            "252"
                        ],
                        [
                            "PDSCH 4",
                            "17",
                            "True",
                            "252"
                        ],
                        [
                            "PDCCH 1",
                            "0",
                            "True",
                            "108"
                        ],
                        [
                            "PDCCH 1",
                            "1",
                            "True",
                            "108"
                        ],
                        [
                            "PDCCH 1",
                            "2",
                            "True",
                            "108"
                        ],
                        [
                            "PDCCH 1",
                            "3",
                            "True",
                            "108"
                        ],
                        [
                            "PDCCH 1",
                            "4",
                            "True",
                            "108"
                        ],
                        [
                            "PDCCH 1",
                            "5",
                            "True",
                            "108"
                        ],
                        [
                            "PDCCH 1",
                            "6",
                            "True",
                            "108"
                        ],
                        [
                            "PDCCH 1",
                            "7",
                            "True",
                            "108"
                        ],
                        [
                            "PDCCH 1",
                            "10",
                            "True",
                            "108"
                        ],
                        [
                            "PDCCH 1",
                            "11",
                            "True",
                            "108"
                        ],
                        [
                            "PDCCH 1",
                            "12",
                            "True",
                            "108"
                        ],
                        [
                            "PDCCH 1",
                            "13",
                            "True",
                            "108"
                        ],
                        [
                            "PDCCH 1",
                            "14",
                            "True",
                            "108"
                        ],
                        [
                            "PDCCH 1",
                            "15",
                            "True",
                            "108"
                        ],
                        [
                            "PDCCH 1",
                            "16",
                            "True",
                            "108"
                        ],
                        [
                            "PDCCH 1",
                            "17",
                            "True",
                            "108"
                        ]
                    ]
                ]
            ],
            [
                [
                    "2",
                    "3.700005",
                    "100",
                    "1.7345576286315918",
                    "3.5",
                    "Pass",
                    "C:\\Automation\\radi_bn28\\ORAN-Automation\\CUPLANE\\Results\\LPRUD_4T4R\\2.0.7\\EAXCID2\\Extended_DL_UL",
                    [
                        "PUCCH Decoder : Off",
                        "PUSCH Decoder : On",
                        "PUSCH_0_IE : PUSCH Index=0, CarrierIndex=0, BWPIndex=0",
                        "PUSCH_F0_IE : Codeword=0, SlotIndex=08, RV Index=0, EffectiveCodeRate=0.6616, CRC=Pass , Number Of Code Blocks: 2",
                        "PUSCH_F1_IE : Codeword=0, SlotIndex=09, RV Index=0, EffectiveCodeRate=0.6616, CRC=Pass , Number Of Code Blocks: 2",
                        "PUSCH_F2_IE : Codeword=0, SlotIndex=18, RV Index=0, EffectiveCodeRate=0.6616, CRC=Pass , Number Of Code Blocks: 2",
                        "PUSCH_F3_IE : Codeword=0, SlotIndex=19, RV Index=0, EffectiveCodeRate=0.6616, CRC=Pass , Number Of Code Blocks: 2",
                        "PUSCH_1_IE : PUSCH Index=1, CarrierIndex=0, BWPIndex=0",
                        "PUSCH_F4_IE : Codeword=0, SlotIndex=07, RV Index=0, EffectiveCodeRate=0.6776, CRC=Pass , Number Of Code Blocks: 1",
                        "PUSCH_F5_IE : Codeword=0, SlotIndex=17, RV Index=0, EffectiveCodeRate=0.6776, CRC=Pass , Number Of Code Blocks: 1"
                    ]
                ]
            ]
        ],
        "16_QAM_Comp_14_bit_DL_UL": [
        [
            [
                "3",
                "3.54234",
                "FR1_100M",
                "3.45",
                "5.0",
                "24.29",
                "23",
                "24.99",
                "Pass",
                "C:\\Automation\\FH_Testing/Results/CUPLANE/LPRU_v2/1.0.19/22082142000036/FR1_100M/EAXCID3/16_QAM_Comp_14_bit_DL_UL/capture.png",
                [
                    [
                        "#6335013Channel",
                        "Slot",
                        "CRC Passed",
                        "Bit Length"
                    ],
                    [
                        "PDSCH 1",
                        "0",
                        "True",
                        "89856"
                    ],
                    [
                        "PDSCH 1",
                        "1",
                        "True",
                        "89856"
                    ],
                    [
                        "PDSCH 1",
                        "2",
                        "True",
                        "89856"
                    ],
                    [
                        "PDSCH 1",
                        "3",
                        "True",
                        "89856"
                    ],
                    [
                        "PDSCH 1",
                        "4",
                        "True",
                        "89856"
                    ],
                    [
                        "PDSCH 1",
                        "5",
                        "True",
                        "89856"
                    ],
                    [
                        "PDSCH 1",
                        "6",
                        "True",
                        "89856"
                    ],
                    [
                        "PDSCH 1",
                        "10",
                        "True",
                        "89856"
                    ],
                    [
                        "PDSCH 1",
                        "11",
                        "True",
                        "89856"
                    ],
                    [
                        "PDSCH 1",
                        "12",
                        "True",
                        "89856"
                    ],
                    [
                        "PDSCH 1",
                        "13",
                        "True",
                        "89856"
                    ],
                    [
                        "PDSCH 1",
                        "14",
                        "True",
                        "89856"
                    ],
                    [
                        "PDSCH 1",
                        "15",
                        "True",
                        "89856"
                    ],
                    [
                        "PDSCH 1",
                        "16",
                        "True",
                        "89856"
                    ],
                    [
                        "PDSCH 4",
                        "7",
                        "True",
                        "38016"
                    ],
                    [
                        "PDSCH 4",
                        "17",
                        "True",
                        "38016"
                    ],
                    [
                        "PDCCH 1",
                        "0",
                        "True",
                        "108"
                    ],
                    [
                        "PDCCH 1",
                        "1",
                        "True",
                        "108"
                    ],
                    [
                        "PDCCH 1",
                        "2",
                        "True",
                        "108"
                    ],
                    [
                        "PDCCH 1",
                        "3",
                        "True",
                        "108"
                    ],
                    [
                        "PDCCH 1",
                        "4",
                        "True",
                        "108"
                    ],
                    [
                        "PDCCH 1",
                        "5",
                        "True",
                        "108"
                    ],
                    [
                        "PDCCH 1",
                        "6",
                        "True",
                        "108"
                    ],
                    [
                        "PDCCH 1",
                        "7",
                        "True",
                        "108"
                    ],
                    [
                        "PDCCH 1",
                        "10",
                        "True",
                        "108"
                    ],
                    [
                        "PDCCH 1",
                        "11",
                        "True",
                        "108"
                    ],
                    [
                        "PDCCH 1",
                        "12",
                        "True",
                        "108"
                    ],
                    [
                        "PDCCH 1",
                        "13",
                        "True",
                        "108"
                    ],
                    [
                        "PDCCH 1",
                        "14",
                        "True",
                        "108"
                    ],
                    [
                        "PDCCH 1",
                        "15",
                        "True",
                        "108"
                    ],
                    [
                        "PDCCH 1",
                        "16",
                        "True",
                        "108"
                    ],
                    [
                        "PDCCH 1",
                        "17",
                        "True",
                        "108"
                    ]
                ]
            ]
        ],
        [
            [
                "3",
                "3.54234",
                "FR1_100M",
                "1.632390022277832",
                "3",
                "Pass",
                "C:\\Automation\\FH_Testing/Results/CUPLANE/LPRU_v2/1.0.19/22082142000036/FR1_100M/EAXCID3/16_QAM_Comp_14_bit_DL_UL",
                [
                    "PUCCH Decoder : Off",
                    "PUSCH Decoder : On",
                    "PUSCH_0_IE : PUSCH Index=0, CarrierIndex=0, BWPIndex=0",
                    "PUSCH_F0_IE : Codeword=0, SlotIndex=08, RV Index=0, EffectiveCodeRate=0.6448, CRC=Pass , Number Of Code Blocks: 3",
                    "PUSCH_F1_IE : Codeword=0, SlotIndex=09, RV Index=0, EffectiveCodeRate=0.6448, CRC=Pass , Number Of Code Blocks: 3",
                    "PUSCH_F2_IE : Codeword=0, SlotIndex=18, RV Index=0, EffectiveCodeRate=0.6448, CRC=Pass , Number Of Code Blocks: 3",
                    "PUSCH_F3_IE : Codeword=0, SlotIndex=19, RV Index=0, EffectiveCodeRate=0.6448, CRC=Pass , Number Of Code Blocks: 3",
                    "PUSCH_1_IE : PUSCH Index=1, CarrierIndex=0, BWPIndex=0",
                    "PUSCH_F4_IE : Codeword=0, SlotIndex=07, RV Index=0, EffectiveCodeRate=0.6481, CRC=Pass , Number Of Code Blocks: 1",
                    "PUSCH_F5_IE : Codeword=0, SlotIndex=17, RV Index=0, EffectiveCodeRate=0.6481, CRC=Pass , Number Of Code Blocks: 1"
                ]
            ]
        ]
    ],
        "256_QAM_DL_64_QAM_UL_Comp_12_bit": [
        [
            [
                "3",
                "3.54234",
                "FR1_100M",
                "verify_result_and_capture_screenshot Error : VI_ERROR_CONN_LOST (-1073807194): The connection for the given",
                "3",
                "session",
                "23",
                "24.99",
                "has",
                "been"
            ]
        ],
        [
            [
                "3",
                "3.54234",
                "FR1_100M",
                "1.6181265115737915",
                "3",
                "Pass",
                "C:\\Automation\\FH_Testing/Results/CUPLANE/LPRU_v2/1.0.19/22082142000036/FR1_100M/EAXCID3/256_QAM_DL_64_QAM_UL_Comp_12_bit",
                [
                    "PUCCH Decoder : Off",
                    "PUSCH Decoder : On",
                    "PUSCH_0_IE : PUSCH Index=0, CarrierIndex=0, BWPIndex=0",
                    "PUSCH_F0_IE : Codeword=0, SlotIndex=08, RV Index=0, EffectiveCodeRate=0.9231, CRC=Pass , Number Of Code Blocks: 6",
                    "PUSCH_F1_IE : Codeword=0, SlotIndex=09, RV Index=0, EffectiveCodeRate=0.9231, CRC=Pass , Number Of Code Blocks: 6",
                    "PUSCH_F2_IE : Codeword=0, SlotIndex=18, RV Index=0, EffectiveCodeRate=0.9231, CRC=Pass , Number Of Code Blocks: 6",
                    "PUSCH_F3_IE : Codeword=0, SlotIndex=19, RV Index=0, EffectiveCodeRate=0.9231, CRC=Pass , Number Of Code Blocks: 6",
                    "PUSCH_1_IE : PUSCH Index=1, CarrierIndex=0, BWPIndex=0",
                    "PUSCH_F4_IE : Codeword=0, SlotIndex=07, RV Index=0, EffectiveCodeRate=0.9325, CRC=Pass , Number Of Code Blocks: 2",
                    "PUSCH_F5_IE : Codeword=0, SlotIndex=17, RV Index=0, EffectiveCodeRate=0.9325, CRC=Pass , Number Of Code Blocks: 2"
                ]
            ]
        ]
    ]
    }

    # Test_Description = """
    #                     Objective: CU -Plane O-RU Scenario Class Base 3GPP DL/UL.
    #                     Description: The purpose of this test is to ensure the radio can transmit and receive a basic 3GPP TDD test frame by configuring the necessary parameters. This test is applicable for Category A and Category B radios.
    #                     """
    # # print(len(Result))
    generate_report_dl_ul(Result, report_path,information)
    # import json
    # with open("/home/vvdn/Desktop/CUPlane_Automation/radi_bn28/ORAN-Automation/CUPLANE/Master_Script/test.json","w") as json_file:
    #     json.dump(Result, json_file, indent=4)

