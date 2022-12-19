import pyvisa, time

class vxt_connection():
    def __init__(self,visa_address:str) -> None:
        self.visa_add = visa_address

    def visa_connection(self):
        try:
            self.device = pyvisa.ResourceManager().open_resource(self.visa_add)
            self.device.timeout = 25000
            return self.device
        except Exception as e:
            print(f"Visa_connection Error | {type(e).__name__} : {e}")
            return False
        
    def scpi_write(self,scpi):
        Error = ''
        self.device.write(scpi)
        try:
            status = self.device.query("*OPC?")
            print(f"{scpi} : {status[0]}")
            if status[0] == '1': # Check for any error during the execution of SCPI command
                return 1
        except Exception as e:
            Error = f'scpi_write Error {scpi} : {e}'
            print(Error)

    def add_vxt_address(self,vxt_add:str):
        self.scpi_write(vxt_add)
    
    def select_nr5G(self):
        self.scpi_write(':RAD:SEL NR5G')

    def import_scp_file(self,FilePath = ''):
        self.scpi_write(f'RAD:NR5G:WAV:FILE:IMPort "{FilePath}"')

    def basic_conf(self,freq = '4.000005',amplitude = '-60',vxt_add = 'TCPIP::172.17.144.2::inst0::INSTR'):
        freq = float(freq)*10**9
        # self.scpi_write('RAD:NR5G:PLAY:VXT:UPD:TO')
        # self.scpi_write('RAD:NR5G:PLAY:VXT:UPD:FROM')
        # self.scpi_write('RAD:NR5G:PLAY:VXT:PRE')
        self.scpi_write('RAD:NR5G:PLAY:SEL VXT')
        self.scpi_write(f'RAD:NR5G:PLAY:VXT:INST:ADDR "{vxt_add}"')
        self.scpi_write(f'RAD:NR5G:PLAY:VXT:INST:FREQ {freq}')
        self.scpi_write(f'RAD:NR5G:PLAY:VXT:INST:POW {amplitude}')

    def trigger_conf(self,ext_delay = '0.00998698'):
        self.scpi_write('RAD:NR5G:PLAY:VXT:INST:TRIG:TYPE CONT')
        # self.scpi_write('RAD:NR5G:PLAY:VXT:INST:TRIG EXT')
        self.scpi_write('RADio:NR5G:PLAYback:VXT:INSTrument:TRIGger EXTernal1')
        self.scpi_write('RAD:NR5G:PLAY:VXT:INST:TRIG:EXT:SLOP POS')
        self.scpi_write('RAD:NR5G:PLAY:VXT:INST:TRIG:EXT:DEL:STAT ON')
        self.scpi_write(f'RAD:NR5G:PLAY:VXT:INST:TRIG:EXT:DELay {ext_delay}')

    def genrate_download(self):
        self.scpi_write('RAD:NR5G:PLAY:VXT:CONN')
        time.sleep(3)
        self.scpi_write('RAD:NR5G:WAV:GEN')

if __name__ == "__main__":
    pathwave_address = 'TCPIP0::172.17.144.106::hislip18::INSTR'
    vxt_address = 'TCPIP::172.17.144.2::inst0::INSTR'
    FilePath = r"C:\Automation\FH_Testing_V1.0.0\Results\Base_UL_Apmlitude_42.scp"
    freq = '4.000005'
    amplitude = '-42'
    ext_delay = '0.00998698'
    pathwave_obj = vxt_connection(visa_address=pathwave_address)
    status = pathwave_obj.visa_connection()
    if status != False:
        pathwave_obj.select_nr5G()
        for _ in range(3):
            pathwave_obj.import_scp_file(FilePath=FilePath)
            pathwave_obj.basic_conf(freq=freq,amplitude=amplitude,vxt_add=vxt_address)
            pathwave_obj.trigger_conf(ext_delay=ext_delay)
            pathwave_obj.genrate_download()
            input('Check the trigger...')
        pathwave_obj.device.close()