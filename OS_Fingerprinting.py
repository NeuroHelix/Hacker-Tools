import argparse
import nmap
import csv
import os
import sys

def scan_host(ip, ports):
    nm = nmap.PortScanner() ## Scans ip and ports provided as arguments above ##
    nm.scan(ip, ports) ## Runs an NMAP scan ##
    host_infos = []   ## Empty list to hold all results ##

    for proto in nm[ip].all_protocols(): ## Iterate through results and append everything to the list ##
        lport = nm[ip][proto].keys()
        for port in lport:
            host_info = {
                'ip': ip,
                'os': nm[ip].get('osclass', {}).get('osfamily', 'Unknown'),
                'port': port,
                'name': nm[ip][proto][port]['name'],
                'product': nm[ip][proto][port]['product'],
                'version': nm[ip][proto][port]['version'],
            }
            host_infos.append(host_info)

    return host_infos

def output_to_csv(output_file, host_info): ## File we want to save to and what we want saved as arguments ## 
    fieldnames = ["ip", "os", "port", "name", "product", "version"] ## Define the field names ##
    file_exists = os.path.isfile(output_file) ## See if file exists ## 
    ## Open in append mode, add header, write host info to file ## 

    with open(output_file, "a") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(host_info)

def main():
    ## Handle commandline input and parse it correctly to be used by the script ## 
    parser = argparse.ArgumentParser(description="Scan a single host for open ports and services")
    parser.add_argument("host", help="The target host IP address")
    parser.add_argument("-p", "--ports", help="Ports to scan", type=str, required=True)
    parser.add_argument("-o", "--output", help="The output file", default="scan_results.csv")
    args = parser.parse_args()

    ip = args.host
    ports = args.ports
    output_file = args.output

    ## Terminal communications for the user ## 
    print(f"Scanning IP: {ip}")
    print(f"Scanning ports: {ports}")

    sys.stdout.write("Scanning ")
    sys.stdout.flush()

    ## Calls scan hosts function, result is saved to host_infos ##
    host_infos = scan_host(ip, ports)
    
    for host_info in host_infos: ## Save host_infos to file ##
        output_to_csv(output_file, host_info)

    ## Print info to terminal for user experience ## 
    print("\n\nScan results:")
    for host_info in host_infos:
        print(f"IP: {host_info['ip']}")
        print(f"OS: {host_info['os']}")
        print(f"Port: {host_info['port']}")
        print(f"Name: {host_info['name']}")
        print(f"Product: {host_info['product']}")
        print(f"Version: {host_info['version']}\n")

if __name__ == "__main__":
    main()