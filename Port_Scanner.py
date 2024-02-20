import os
from scapy.all import ICMP, IP, sr1, TCP, sr
from ipaddress import ip_network
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

print_lock = Lock() ##Ensures Threadsafe printing ##

## Ping a single host ##
def ping(host): ## Receives Host IP as argument ## 
    response = sr1(IP(dst=str(host))/ICMP(), timeout=1, verbose=0) ##Sends out ICMP packet to trigger response ##
    if response is not None:
        return str(host)
    return None


## Ping sweep across the network (range)##
def ping_sweep(network, netmask):
    live_hosts = []

    num_threads = os.cpu_count() ##Ammount of threads determined based automatically on number of cpu cores ##
    hosts = list(ip_network(network + '/' + netmask).hosts()) ## Calculate range of potential IP's ##
    total_hosts = len(hosts) ##Total ammount of hosts ##
    
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = {executor.submit(ping, host): host for host in hosts} ## Uses ping function defined above to list every single ip on the host's network ##
        for i, future in enumerate(as_completed(futures), start=1):
            host = futures[future]
            result = future.result()
            with print_lock:
                print(f"Scanning: {i}/{total_hosts}", end="\r")
                if result is not None:
                    print(f"\nHost {host} is online.")
                    live_hosts.append(result)

    return live_hosts


## Scan a single port ##
def scan_port(args):
    ip, port = args
    response = sr1(IP(dst=ip)/TCP(dport=port, flags="S"), timeout=1, verbose=0) ## Sends SYN packet ##
    if response is not None and response[TCP].flags == "SA": ## Checks to see if a SYN ACK was recieved ##
        return port
    return None

def port_scan(ip, ports): ##Same logic as ping sweep, except determines whick ports are open instead ##
    open_ports = []

    num_threads = os.cpu_count()
    total_ports = len(ports)
    
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = {executor.submit(scan_port, (ip, port)): port for port in ports}
        for i, future in enumerate(as_completed(futures), start=1):
            port = futures[future]
            result = future.result()
            with print_lock:
                print(f"Scanning {ip}: {i}/{total_ports}", end="\r")
                if result is not None:
                    print(f"\nPort {port} is open on host {ip}")
                    open_ports.append(result)

    return open_ports

## Scan range of ports ##
def get_live_hosts_and_ports(network, netmask):
    live_hosts = ping_sweep(network, netmask)

    host_port_mapping = {}
    ports = range(1, 1024)
    for host in live_hosts:
        open_ports = port_scan(host, ports)
        host_port_mapping[host] = open_ports

    return host_port_mapping

## Performs Network Scan and gives results ##
if __name__ == "__main__":
    import sys
    network = sys.argv[1]
    netmask = sys.argv[2]
    host_port_mapping = get_live_hosts_and_ports(network, netmask)
    for host, open_ports in host_port_mapping.items():
        print(f"\nHost {host} has the following open ports: {open_ports}")


