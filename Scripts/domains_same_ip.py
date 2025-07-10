import json
from datetime import date
from datetime import timedelta

today = date.today()
yesterday = today - timedelta(days = 15)

# Load the JSON data
with open("YOUR_PATH.json") as f:
    data = json.load(f)

# Function to search for domains associated with each IP
def search_domains(ip_list):
    ip_domains = {}
    for ip in ip_list:
        ip_domains[ip] = {}
        for domain, records in data.items():
            domain_count = 0
            for record in records['records']:
                if ip in record.get('A', []) or ip in record.get('AAAA', []):
                    domain_count += 1
            if domain_count > 0:
                ip_domains[ip][domain] = domain_count
    return ip_domains

# Read the list of IPs from a text file
with open("YOUR_PATH"+str(yesterday)+"/ips.txt") as f:
    ip_list = [line.strip() for line in f]

# Search for domains associated with each IP
ip_domains = search_domains(ip_list)

# Write the output to a text file
with open("YOUR_PATH"+str(yesterday)+"/domains_same_ip.txt", mode='a') as file:
    for ip, domains in ip_domains.items():
        file.write(f"IP: {ip}\n")
        file.write("Domains:\n")
        for domain, count in domains.items():
            file.write(f"- {domain}, {count}\n")
        file.write("\n")

print("Output written to domains_same_ip.txt file.")
