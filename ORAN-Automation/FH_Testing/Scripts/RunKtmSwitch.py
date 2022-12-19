import clr,time,os

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
clr.AddReference(f"{root_dir}/Dependencies/Keysight.KtMSwitch.Fx40.dll")
from Keysight.KtMSwitch import *

def run_ktmswitch(pxi_address:str,port_channel:str):
    try:
        port = port_channel[1]
        channel = port_channel[-1]
        print("------------------Starting the Channel no. {0}---------------------------\n\n\n".format(channel))
        driver = KtMSwitch(pxi_address,True,True)
        print("Device_Identifier:  ".upper(), driver.Identity.Identifier)
        print("Device_Revision:    ".upper(), driver.Identity.Revision)
        print("Device_Vendor:      ".upper(), driver.Identity.Vendor)
        print("Device_Description: ".upper(), driver.Identity.Description)
        print("Device_Model:       ".upper(), driver.Identity.InstrumentModel)
        print("Device_FirmwareRev: ".upper(), driver.Identity.InstrumentFirmwareRevision)
        print("Device_Serial :    ".upper(), driver.System.SerialNumber)
        print("Device_Simulate:   ".upper(), driver.DriverOperation.Simulate)
        print('\n')
        print(f"Closing Port {port}, channel {channel}.")
        ch_status = driver.Route.CloseChannel(f"p{port}ch{channel}")
        time.sleep(1)
        status = driver.Route.IsChannelClosed(f"p{port}ch{channel}")
        ## Make sure port 1, channel reports that it is closed
        if status:
            print(f"Channel {channel} , port 1 reported it was closed, as expected.")
            return True
        else:
            print(f"ERROR: Channel {channel} , port 1 reported as open.  Should be closed.")
            print('-'*50)
            print('\n\n Please Connect the Type C USB with RF Switch...')
            print('-'*50)
            return False
    except Exception as e:
        print(f"RunKtmSwitch error : {e}")
        print('-'*50)
        print('\n\n Please Connect the Type C USB with RF Switch...')
        print('-'*50)
        return False
    finally:
        print("Driver Closed")
        driver.Close()


if __name__ == "__main__":
    chn_status = run_ktmswitch("PXI10::0-0.0::INSTR", f"p1ch3")