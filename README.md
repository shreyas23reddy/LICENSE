# LICENSE


(License-Automation) shreredd@SHREREDD-M-856H License-Automation % python3 license.py -h              

usage: license.py [-h] 
[-a ADDRESS] 
[-p PORT] 
[-u USERNAME] 
[-pw PASSWORD]
{all,sid} ...


_______________________________________________________


positional arguments:
 
 {all,sid}   
 'all' - run script on all sites 
 'sid' - run script on a specific site

________________________________________________________

optional arguments:
  -h, --help            show this help message and exit
  
  -a ADDRESS, --address ADDRESS vManage IP address
  
  -p PORT, --port PORT  vManage port
  
  -u USERNAME, --username USERNAME vManage username
  
  -pw PASSWORD, --password PASSWORD vManage password



__________________________________________________________

(License-Automation) shreredd@SHREREDD-M-856H License-Automation % python3 license.py -a 10.10.10.1 -p 8443 -u admin -pw Admin all

Gathering the data from ASR1002-X-FOX1- 40.40.40.1
Gathering the data from ASR1002-X-FOX - 40.40.40.2
Gathering the data from C8K-ABF8617A-C561-B082 - 20.20.20.1
Gathering the data from C8K-E911BA8F-BC - 20.20.20.2
Gathering the data from ISR4431/K9-FOC2 - 120.120.120.1
Gathering the data from ISR4331/K9-FLM - 110.110.110.1
Gathering the data from CSR-FD1EE2F1 - 105.105.105.1
Gathering the data from CSR-54674ABC- 105.105.105.2

        Please view the license-01-18-2023_24-56-34.csv for the license teir and aggregate info per site



_____________________________________________________________

(License-Automation) shreredd@SHREREDD-M-856H License-Automation % python3 license.py -a 10.10.10.1 -p 8443 -u admin -pw Admin sid -h 

usage: license.py sid [-h] -id ID

optional arguments:
  -h, --help  show this help message and exit
  -id ID

_______________________________________________________________

(License-Automation) shreredd@SHREREDD-M-856H License-Automation % python3 license.py -a 10.10.10.1 -p 8443 -u admin -pw Admin sid -id 40
 Gathering the data from ASR1002-X-FOX1933G4DD - 40.40.40.1 
 Gathering the data from ASR1002-X-FOX1932G6PC - 40.40.40.2 

        Please view the license-01-18-2023_10-15-12.csv for the license teir and aggregate info per site


