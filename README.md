# Hacker-Tools
A collection of python network scanners and other tools.
Only use on devices/networks you own or have permission to do so on.

Name of script, followed by input (input 1, input 2) and resulted output:


Ping_Sweeper:
input (subnet, netmask)
output = list of live ips on the network you are scanning


Port_Scanner:
input (subnet, netmask)
output = (open IP's + open ports)

Service_Fingerprint:
input (IP, port numbers)
output = service banner & version numbers

OS_Fingerprint:
input (IP, port numbers)
output = service banner & version numbers, saves data to scan_results.csv

KeyLogger:
replace "C:/path/to/logger" with your own file path where you will keep the key logger. This is also where log files will be stored. Note: Windows defender will try to delete this file if you run it, so be sure to set up an exclusion!



