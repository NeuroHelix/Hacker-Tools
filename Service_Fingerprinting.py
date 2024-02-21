import sys
import argparse
import socket

## Send get request and recieve response ## 
def get_service_banner(ip, port):
    try:
        ## Create a socket object ## 
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect((ip, int(port)))
        ## Send a get request to that socket ##
        sock.send(b"GET / HTTP/1.1\r\nHost: " + ip.encode() + b"\r\n\r\n")
        banner = sock.recv(1024) # Save the response as a string ## 
        sock.close() ## Close the socket ## 

        return banner.decode('utf-8', errors='ignore')
    except Exception:
        return None

## Manages data and prints to screen ## 
def main():
    parser = argparse.ArgumentParser(description='Service Banner Scanner') 
    parser.add_argument('ip', help='IP address to scan')
    parser.add_argument('-p', '--ports', required=True, help='Ports to scan (comma-separated)')
## Recieves IP address and port numbers as input from the command line ##
    
    args = parser.parse_args() ## Parse and format for further use in the program ## 

    ip = args.ip
    ports = [port.strip() for port in args.ports.split(',')]

    print(f"Scanning IP: {ip}")
    for port in ports:
        print(f"Scanning port {port} on IP {ip}")
        banner = get_service_banner(ip, port)
        if banner:
            print(f"Service banner for port {port} on IP {ip}:\n{banner}\n")
        else:
            print(f"No service banner found for port {port} on IP {ip}\n")
            ## Iterates through all ports provided, calls the get_service_banner function and inform the user if it is successfull or not ## 

if __name__ == "__main__":
    main()