import sys
from scapy.all import ICMP, IP, sr1
from netaddr import IPNetwork

## Recieves a given network and netmask from the user. ##
def ping_sweep(network, netmask):
    live_hosts = []
    total_hosts = 0
    scanned_hosts = 0

## Performs a ping sweep. ##
    ip_network = IPNetwork(network + '/' + netmask)
    for host in ip_network.iter_hosts():
        total_hosts += 1

    for host in ip_network.iter_hosts():
        scanned_hosts += 1
        print(f"Scanning: {scanned_hosts}/{total_hosts}", end="\r")
        response = sr1(IP(dst=str(host))/ICMP(), timeout=1, verbose=0)
## Returns list of live hosts. ##        
        if response is not None:
            live_hosts.append(str(host))
            print(f"Host {host} is online.")

    return live_hosts
## Recieves user's input from command line and passes it to the ping_sweep function ##
if __name__ == "__main__":
    network = sys.argv[1]
    netmask = sys.argv[2]

    live_hosts = ping_sweep(network, netmask)
    print("Completed\n")
    print(f"Live hosts: {live_hosts}")
