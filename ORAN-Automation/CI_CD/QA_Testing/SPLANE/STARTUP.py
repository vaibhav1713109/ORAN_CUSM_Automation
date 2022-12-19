from os import name, path
from fpdf import FPDF
import json ,os
from fpdf.enums import XPos, YPos
from configparser import ConfigParser


###############################################################################
## Directory Path
###############################################################################
dir_name = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(dir_name)


########################################################################
## For reading data from .ini file
########################################################################
configur = ConfigParser()
configur.read('{}/inputs.ini'.format(root_dir))
ru_name = configur.get('INFO','ru_name')
img_version = configur.get('INFO','img_version')
d1 = os.path.dirname(os.path.realpath(__file__))
class PDF(FPDF):
    

    def header(self):
     #    self.image('{}/require/vvdn_logo.png'.format(parent), 10, 8, 33)
        self.set_text_color(44, 112, 232)
        self.set_font('Arial', 'B', 15)
        self.set_x(-45)
        self.set_font('Times', 'B', 12)
        self.cell(0,10,'S Plane Conformance', XPos.RIGHT, new_y= YPos.NEXT, align='R')
        self.set_text_color(0,0,0)
        self.ln(20)


    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(0,0,0)
        self.cell(0, 10, 'Page %s' % self.page_no(), XPos.RIGHT, new_y= YPos.NEXT, align='C')
        self.set_text_color(44, 112, 232)
        self.set_font('Arial', 'B', 8)
        self.cell(0, -10, 'Copyright (c) 2016 - 2022 VVDN Technologies Pvt Ltd', XPos.RIGHT, new_y= YPos.NEXT, align='R')
        self.cell(0,10)
        self.set_text_color(0,0,0)

f = open(f'{d1}/details.json')
data = json.load(f)
str3 = f"{data['ru_name']}"
def STORE_DATA(*datas,Format,PDF):
     for data in datas:
        # OUTPUT_LIST.append(*data)
        # print(''.join([*data])
          if Format == True:
               print('='*100)
               print(data)
               print('='*100)
               HEADING(PDF,data)

          elif Format == 'XML':
               print(data)
               XML_FORMAT(PDF,data)

          elif Format == 'CONF':
               print('='*100)
               print(data)
               print('='*100)
               CONFDENTIAL(PDF,data)
          
          elif Format == 'DESC':
               print('='*100)
               print(data)
               print('='*100)
               Test_desc(PDF,data)
          
          elif Format == 'TEST_STEP':
               print('='*100)
               print(data)
               print('='*100)
               Test_Step(PDF,data)
          
          # elif Format == False:
          #      # print('='*100)
          #      print(data)
          #      # print('='*100)
          #      Test_Step(PDF,data)

          else:
               print(data)
               PDF.write(h=5,txt=data)
               PDF.ln()

def CREATE_LOGS(PDF,name):
    # STORE_DATA(OUTPUT_LIST,OUTPUT_LIST)
    PDF.output(f"{path}.pdf")
    PDF.output(f"{path+name}.pdf")
def Test_desc(PDF,data):
     PDF.set_font("Times",style = 'B', size=13)
     PDF.set_text_color(17, 64, 37)
     PDF.write(5, '\n{}\n'.format('='*71))
     PDF.multi_cell(w =180,h = 10,txt='Test Description : {}'.format(data),border=1,align='L')
     PDF.write(5, '\n{}\n'.format('='*71))
     PDF.set_font("Times",style = '',size = 9)
     PDF.set_text_color(0, 0, 0)
     # PDF.ln(80)
     pass
def PDF_CAP(TC):
    d1 = os.path.dirname(os.path.realpath(__file__))
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Times", size=9)
    pdf.image(name=f'{d1}/Front_Page.png', x = None, y = None, w = 180, h = 70, type = '', link = '')
    pdf.ln(30)
    line_height = (pdf.font_size) * 3.5
    col_width = pdf.epw / 2 
    data1 = (
    (f"Test Case","S_CTC_ID_00{0}".format(TC)),
    ("Brief", f"{ru_name} ORAN CONFORMANCE TEST LOGS FOR S PLANE "),
    ("Author","Vikas Saxena, (vikas.saxena@vvdntech.in)"),
    (f"Software Release for {ru_name} ",f"Beta Release:{img_version}")
)
    for row in data1:
     for datum in row:
          pdf.multi_cell(col_width, line_height, datum, border=1,
                    new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size)
     pdf.ln(line_height)
    pdf.add_page()
    return pdf
def HEADING(PDF,data,*args):
    PDF.set_font("Times",style = 'B', size=9)
    PDF.write(5, '\n{}\n'.format('='*75))
    PDF.write(5,data)
    PDF.write(5, '\n{}\n'.format('='*75))
    PDF.set_font("Times",style = '',size = 9)

def XML_FORMAT(PDF,data):
    PDF.set_text_color(0,0,0)
    PDF.write(4,data)
    PDF.set_text_color(0, 0, 0)

def CONFDENTIAL(PDF,data):
     PDF.set_font("Times",style = 'B', size=15)
     PDF.set_text_color(10, 32, 71)
     PDF.write(5, '\n{}\n'.format('='*62))
     PDF.multi_cell(w =180,txt=data,border=1,align='L',h = 5)
     PDF.write(5, '\n{}\n'.format('='*62))
     PDF.set_font("Times",style = '',size = 9)
     PDF.set_text_color(0, 0, 0)
     PDF.ln(30)
     pass

def Test_Step(PDF,data):
    PDF.set_font("Times",style = 'B', size=11)
    PDF.set_text_color(125, 93, 65)
    PDF.write(5, '\n{}\n'.format('='*80))
    PDF.write(5,data)
    PDF.write(5, '\n{}\n'.format('='*80))
    PDF.set_font("Times",style = '',size = 9)
    PDF.set_text_color(0,0,0)
def summary(PDF,data1): 
    data = []
    for d in data1:
        print(d)
        data.append(d.split('||'))    
    PDF.set_font("Times", size=10)
    line_height = PDF.font_size * 3.5
    col_width = PDF.epw / 3
    lh_list = [] #list with proper line_height for each row
    use_default_height = 0 #flag
    #create lh_list of line_heights which size is equal to num rows of data
    for row in data:
        for datum in row:
            word_list = datum.split()
            number_of_words = len(word_list) #how many words
            if number_of_words>2: #names and cities formed by 2 words like Los Angeles are ok)
                use_default_height = 1
                new_line_height = PDF.font_size * (number_of_words/2) #new height change according to data 
        if not use_default_height:
            lh_list.append(line_height)
        else:
            lh_list.append(new_line_height)
            use_default_height = 0

    #create your fpdf table ..passing also max_line_height!
    for j,row in enumerate(data):
        for datum in row:
            line_height = lh_list[j] #choose right height for current row
            PDF.multi_cell(col_width, line_height, datum, border=1,align='L',new_x=XPos.RIGHT, new_y=YPos.TOP, 
            max_line_height=PDF.font_size)
            # print(datum)
            
        PDF.ln(line_height)
# pdf = PDF_CAP()
# CONF = ADD_CONFIDENTIAL('10',SW_R='4.0.9')
# STORE_DATA(CONF,Heading='CONF',PDF=pdf)
# Test_Desc = 'This scenario validates that the O-RU NETCONF Server properly executes a get command with a filter applied.'
# STORE_DATA(Test_Desc,Heading='DESC',PswSlot2:VALID:false:false:STL O-RU:VN:90f0b6c:Beta Release:5.0.2:BOOT0002                                                                    
#                </user>
#           </users>
#           </filter>
#                 '''
# STORE_DATA(u_name,Heading='XML',PDF=pdf)
# STORE_DATA('\t\t***********step 1 and 2 Retrival of ru information with filter **********',Heading=True,PDF=pdf)
# CREATE_LOGS(pdf)




    




















