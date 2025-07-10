from ipwhois import IPWhois
from datetime import date
from datetime import timedelta

today = date.today()
yesterday = today - timedelta(days = 15)

def query_asn_for_domain(domain):
    try:
        # Perform an IP Whois lookup for the domain
        ip = IPWhois(domain)
        result = ip.lookup_whois()
        # Extract the ASN information from the result
        asn = result['asn']
        return asn
    except Exception as e:
        return str(e)
def query_asn_for_domains(domains):
    asn_results = {}
    for domain in domains:
        asn_results[domain] = query_asn_for_domain(domain)
    return asn_results

def main():
    # List of domain names to query ASN records for
    with open("YOUR_PATH"+str(yesterday)+"/ips.txt" , "r") as f:
        domain_names = f.read().splitlines()
    
    # Query ASN records for the list of domain names
    results = query_asn_for_domains(domain_names)
    
    # Save the results
    with open("YOUR_PATH"+str(yesterday)+"/asnlookup.txt", mode="a") as file:
        for domain, asn in results.items():
            file.write(f"IP: {domain}, ASN: {asn}\n")

if __name__ == "__main__":
    main()
