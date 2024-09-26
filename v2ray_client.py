import requests
import ssl
import socket
from urllib.parse import urlparse

def load_domains(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def scan_http_request(domain):
    try:
        response = requests.get(domain)
        return response.status_code, response.headers
    except requests.RequestException as e:
        return None, str(e)

def scan_ssl(domain):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                return ssock.version()
    except Exception as e:
        return str(e)

def scan_cdn(domain):
    try:
        response = requests.get(domain)
        cdn_providers = ['Cloudflare', 'Akamai', 'Amazon CloudFront']
        for provider in cdn_providers:
            if provider in response.headers.get('Server', ''):
                return provider
        return "No CDN detected"
    except requests.RequestException as e:
        return str(e)

def scan_sni(domain):
    try:
        port = 443
        context = ssl.create_default_context()
        with socket.create_connection((domain, port)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                return ssock.server_hostname
    except Exception as e:
        return str(e)

def scan_http_methods(domain):
    methods = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'HEAD']
    results = {}
    for method in methods:
        try:
            response = requests.request(method, domain)
            results[method] = response.status_code
        except requests.RequestException as e:
            results[method] = str(e)
    return results

def main():
    print("Welcome to the Domain HTTP Scan Tool")
    domains = load_domains('domains.txt')
    
    while True:
        print("\nMenu:")
        print("1. Scan HTTP Request")
        print("2. Scan SSL")
        print("3. Scan CDN")
        print("4. Scan SNI")
        print("5. Scan HTTP Methods")
        print("6. Exit")
        
        choice = input("Select an option (1-6): ")
        
        if choice == '6':
            print("Exiting the tool.")
            break
        
        domain = input("Enter the domain (e.g., https://example.com): ")
        
        if domain not in domains:
            print("Domain not found in the loaded list.")
            continue
        
        if choice == '1':
            status_code, headers = scan_http_request(domain)
            print(f"HTTP Status Code: {status_code}\nHeaders: {headers}")
        elif choice == '2':
            ssl_version = scan_ssl(domain)
            print(f"SSL Version: {ssl_version}")
        elif choice == '3':
            cdn = scan_cdn(domain)
            print(f"CDN Detected: {cdn}")
        elif choice == '4':
            sni = scan_sni(domain)
            print(f"SNI: {sni}")
        elif choice == '5':
            methods_result = scan_http_methods(domain)
            print(f"HTTP Methods Results: {methods_result}")
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
