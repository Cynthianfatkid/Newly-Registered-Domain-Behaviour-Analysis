'''
Script that extracts the domains with 1 record from the results of domains_same_ip.py
'''
from datetime import date
from datetime import timedelta

today = date.today()
yesterday = today - timedelta(days = 16)

def extract_domains_with_number_one(input_file, output_file):
    with open(input_file, 'r') as file:
        content = file.readlines()

    domains_with_one = []

    for line in content:
        if line.strip().startswith('-') and ', 1' in line:
            domain = line.split(',')[0].strip()[2:]
            domains_with_one.append(domain)

    with open(output_file, 'a') as file:
        for domain in domains_with_one:
            file.write(domain + '\n')

if __name__ == "__main__":
    input_file = "YOUR_PATH"+str(yesterday)+"/domains_same_ip.txt"
    output_file = "YOUR_PATH.txt"
    extract_domains_with_number_one(input_file, output_file)
