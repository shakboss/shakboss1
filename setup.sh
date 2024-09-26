#!/bin/bash

# Function to display the menu
display_menu() {
    echo "=============================="
    echo "      Domain HTTP Scanner      "
    echo "=============================="
    echo "1. Scan Domains"
    echo "2. Exit"
    echo "=============================="
}

# Function to scan domains from a file
scan_domains() {
    read -p "Enter the path to the domains file: " domains_file
    if [[ ! -f $domains_file ]]; then
        echo "File not found!"
        return
    fi

    while IFS= read -r domain; do
        echo "Scanning domain: $domain"
        scan_http_request "$domain"
        scan_cdn "$domain"
        scan_ssl "$domain"
        scan_sni "$domain"
        scan_methods "$domain"
        echo "--------------------------------"
    done < "$domains_file"
}

# Function to scan HTTP request
scan_http_request() {
    local domain=$1
    response=$(curl -s -o /dev/null -w "%{http_code}" "$domain")
    echo "HTTP Response Code: $response"
}

# Function to scan for CDN
scan_cdn() {
    local domain=$1
    cdn_check=$(curl -s -I "$domain" | grep -i "via:")
    if [[ -n $cdn_check ]]; then
        echo "CDN Detected: $cdn_check"
    else
        echo "No CDN detected."
    fi
}

# Function to scan SSL
scan_ssl() {
    local domain=$1
    ssl_check=$(echo | openssl s_client -connect "$domain:443" 2>/dev/null | grep "Certificate chain")
    if [[ -n $ssl_check ]]; then
        echo "SSL Certificate Found."
    else
        echo "No SSL Certificate Found."
    fi
}

# Function to scan SNI
scan_sni() {
    local domain=$1
    sni_check=$(echo | openssl s_client -connect "$domain:443" -servername "$domain" 2>/dev/null)
    if [[ -n $sni_check ]]; then
        echo "SNI Supported."
    else
        echo "SNI Not Supported."
    fi
}

# Function to scan HTTP methods
scan_methods() {
    local domain=$1
    methods=$(curl -s -X OPTIONS "$domain" -i | grep "Allow:")
    echo "Allowed HTTP Methods: ${methods:8}"
}

# Main script execution
while true; do
    display_menu
    read -p "Select an option: " option
    case $option in
        1) scan_domains ;;
        2) echo "Exiting..."; exit 0 ;;
        *) echo "Invalid option. Please try again." ;;
    esac
done
