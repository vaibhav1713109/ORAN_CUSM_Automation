Kindly update the below-required information in the "README.md" file in the corresponding Repo root level.

README.md File Should Contain following info:

    1.OS & System Configuration
    2.Required Package/Library related Installation Steps with Version.
    3.Compile and Build Steps.
    4.Build Artifacts/Image Output Path.
    5.Kindly add the .gitignore file based on your project.

Repo URL: https://gitlab.vvdntech.com:8081/oran_qa_automation/radi_bn28.git

***Keysight ORAN Studio-Automation***

This repository is created for performing CU plane Conformance and funcional test cases which include below process.
*  Load Instrumentconfig.xml file so that mac of RU will be added in oran.
*  Making M plane connection 
*  Chacking Sync
*  Carrier Activation and checking sync
*  Scp Generation 
*  Pcap Generation
*  Pcap load and play stimulus
*  Vxt Configuration
*  ORB Generation
*  VSA Configuration
*  Report Generation and Result Declaration
*  Send Notification in Space.

 
 
**OS & System Configuration**
*  OpenSSH should be intsall
*  10G/25G SFP
*  Windows OS
*  KTM Switch 
*  ORAN Studio
*  VXT 

**Used Libraries:**
* Python >=3.7
* ncclient >=0.6.12
* PyVISA >=1.12.0
* PyVISA-py >=0.5.3
* pandas >=2.0.0
* pythonnet >=3.0.1
* fpdf2>=2.5.5
* lxml==4.8.0
* ifcfg>=0.22
* pytest>=7.0.1
* requests>=2.27.1
* tabulate>=0.8.10
* xmltodict>=0.13.0
* pyqt5>=5.15.6
* scapy>=2.5.0
* httplib2>=0.21.0

**Installation**
* python -m pip install --upgrade pip
* pip install -r CUPLANE/Requirement/requirement.txt

**Usage**
* Run with command line
    * Fill all the required data present requirement/inputs.ini file
    * **TDD RU**
        * Go to CUPLANE/TDD directory
        * Run below command
        * python TDD_Config.py 
    * **FDD RU**
        * Go to CUPLANE/FDD directory
        * Run below command
        * python FDD_Config.py

> Note: 
> * Keysight ORAN Api services should be started.
> * Mplane connector should be connect for checking sync, activating the carrier and changing compression.
>  * Whenever mac will be changed or ru is boot u have press "No" when popup message come for Sync so that instrumentconfig.xml will be load for the syncronization and adding mac in ORS application.



***M-Plane Automation***

The repository is been build for M & S Plane optimisation in the Fronthual Interface

 
 
**OS & System Configuration**
*  Linux PC
*  DHCP Server should be install
*  OpenSSH should be intsall
*  10G/25G SFP

**Used Libraries:**
* Python >=3.7
* ncclient >=0.6.12
* fpdf2>=2.5.5
* lxml==4.8.0
* ifcfg>=0.22
* pytest>=7.0.1
* requests>=2.27.1
* tabulate>=0.8.10
* xmltodict>=0.13.0
* pyqt5>=5.15.6
* scapy>=2.5.0
* httplib2>=0.21.0

**Installation**
* python -m pip install --upgrade pip
* pip install -r ORAN-Automation/MPlane_Conformance/requirements.txt

**Setup Diagram**

![./](/Automation_Images/setup_diagram.png)

**Flow Chart**

![./](/Automation_Images/M_Plane_Flow_chart.png)


**File Structure**


* File Structure of Root Directory

![./](/Automation_Images/file_structure_root_dir.png)


**Usage**
* Run with GUI
    * Go to the GUI directory.
    * Run below command
    * sudo python login.py
* Run with terminal
    * Go to M Plane Conformance directory
    * Run below command
    * python config.py
    * sudo python M_CTC_ID_{Test_Case_ID}.py

> Note: 
> * fill all the credentials which will be asked. 
>  *  run first config.py file before running the test cases so that all the latest data will be updated in inputs.ini file 

**GUI Snapshots**

![./](/Automation_Images/GUI_LOGIN.png)

![./](/Automation_Images/GUI_HOME_DHCP.png)

![./](/Automation_Images/GUI_TC1_1.png)

![./](/Automation_Images/GUI_TC_1_OUT.png)
