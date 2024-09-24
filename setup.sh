bash
#!/bin/bash

# Function to display usage
usage() {
    echo "Usage: $0 <IP_RANGE> [PORTS]"
    echo "  IP_RANGE     The range of IP addresses to scan (e.g., 192.168.1.0/24)"
    echo "  PORTS        Comma-separated list of ports to scan (default: 1-65535)"
    exit 1
}

# Function to scan for live hosts
scan_hosts() {
    local ip_range="$1"
    local ports="$2"

    echo "Scanning for live hosts in the range: $ip_range..."

    # Use nmap to find live hosts
    nmap -sn "$ip_range" -oG - | awk '/Up$/{print $2}' > live_hosts.txt

    if [[ -s live_hosts.txt ]]; then
        echo "Live hosts found:"
        cat live_hosts.txt
        echo ""

        # Scan for open ports on live hosts
        if [[ -n "$ports" ]]; then
            echo "Scanning for open ports ($ports) on live hosts..."
            nmap -p "$ports" -iL live_hosts.txt
        else
            echo "Scanning for open ports (1-65535) on live hosts..."
            nmap -p 1-65535 -iL live_hosts.txt
        fi
    else
        echo "No live hosts found in the specified range."
    fi
}

# Main script execution
if [[ $# -lt 1 ]]; then
    usage
fi

IP_RANGE="$1"
PORTS="$2"

# Validate IP range using regex
if ! [[ "$IP_RANGE" =~ ^([0-9]{1,3}\.){3}[0-9]{1,3}(/([0-9]|[1-2][0-9]|3[0-2]))?$ ]]; then
    echo "Error: Invalid IP range format."
    exit 1
fi

# Start scanning
scan_hosts "$IP_RANGE" "$PORTS"
