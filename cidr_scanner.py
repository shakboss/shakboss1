import ipaddress

def cidr_scanner(cidr):
    try:
        # Create an IPv4 network object from the given CIDR
        network = ipaddress.ip_network(cidr, strict=False)
        
        print(f"Scanning CIDR block: {cidr}")
        print("IP Addresses:")
        
        # Iterate through all the IP addresses in the network
        for ip in network:
            print(ip)

    except ValueError as e:
        print(f"Invalid CIDR block: {e}")

if __name__ == "__main__":
    # Example CIDR block to scan
    CIDR_BLOCK = "104.16.0.0/24"  # Replace with the desired CIDR block
    cidr_scanner(CIDR_BLOCK)-