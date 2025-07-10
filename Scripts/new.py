import json
import dns.resolver
import time
from datetime import date
from datetime import timedelta

today = date.today()
yesterday = today - timedelta(days = 5)

def query_dns_records(domain_names):
  """Queries DNS records for a list of domain names.

  Args:
    domain_names: A list of domain names.

  Returns:
    A list of DNS records, one for each domain name in the input list.
  """

  records = {}
  for domain_name in domain_names:
    resolver = dns.resolver.Resolver()
    resolver.timeout = 20 
    resolver.lifetime = 80
    try:
      a_records = resolver.resolve(domain_name, "A")
      mx_records = resolver.resolve(domain_name, "MX")
      ns_records = resolver.resolve(domain_name, "NS")
      txt_records = resolver.resolve(domain_name, "TXT")
      soa_records = resolver.resolve(domain_name, "SOA")
      aaaa_records = resolver.resolve(ns_records[0].to_text(), "AAAA")
      #cname_records = resolver.resolve(domain_name, "CNAME")

      record = {
        domain_name:{
          "records":[
            {"date": str(today),
              "A": [a_record.to_text() for a_record in a_records],
              "AAAA": [aaaa_record.to_text() for aaaa_record in aaaa_records],
              "MX": [mx_record.to_text() for mx_record in mx_records],
              "NS": [ns_record.to_text() for ns_record in ns_records],
              "TXT": [txt_record.to_text() for txt_record in txt_records],
              "SOA": [soa_records[0].to_text()],
              #"CNAME": cname_records[0].to_text(),
            }
          ]
        }
      }

      records.update(record)
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers, dns.resolver.LifetimeTimeout):
      continue

  return records

def main():
  # Read the domain names from a file.
  with open("YOUR_PATH"+ str(yesterday) + ".txt" , "r") as f:
    domain_names = f.read().splitlines()

  # Query the DNS records for the domain names.
  records = query_dns_records(domain_names)

  #Produce output of the records in the same table in a JSON format.
  with open("YOUR_PATH"+str(today)+".json", "a") as outfile:
        json.dump(records, outfile, indent=4)

if __name__ == "__main__":
  main()
