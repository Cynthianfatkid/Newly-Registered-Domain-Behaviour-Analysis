import json
from neo4j import GraphDatabase

# Neo4j connection parameters
uri = "YOUR_PATH"
username = "your_username"
password = "your_password"

# Function to import DNS data from JSON object
def import_dns_data(tx, dns_data):
    for domain, records in dns_data.items():
        for record in records['records']:
            domain_name = domain
            date = record['date']
            
            # Create or merge date node
            tx.run("MERGE (d:Date {date: $date})", date=date)
            
            # Create or merge domain node
            tx.run("MERGE (dom:Domain {name: $domain_name})", domain_name=domain_name)
            
            # Relationship between domain and date
            tx.run("MATCH (dom:Domain {name: $domain_name}), (d:Date {date: $date}) "
                   "MERGE (dom)-[:OCCURRED_ON]->(d)", domain_name=domain_name, date=date)

            # Extract all record types
            a_records = record.get('A', [])
            aaaa_records = record.get('AAAA', [])
            mx_records = record.get('MX', [])
            ns_records = record.get('NS', [])
            txt_records = record.get('TXT', [])
            soa_records = record.get('SOA', [])
            
            # Create relationships for A records
            for ip_address in a_records:
                tx.run("MERGE (i:IPAddress {address: $ip_address})",
                       ip_address=ip_address)
                tx.run("MATCH (d:Domain {name: $domain_name}), "
                       "(i:IPAddress {address: $ip_address}) "
                       "MERGE (d)-[:RESOLVES_TO]->(i)",
                       domain_name=domain_name, ip_address=ip_address)
            
            # Create relationships for AAAA records
            for ipv6_address in aaaa_records:
                tx.run("MERGE (i:IPAddress {address: $ipv6_address})",
                       ipv6_address=ipv6_address)
                tx.run("MATCH (d:Domain {name: $domain_name}), "
                       "(i:IPAddress {address: $ipv6_address}) "
                       "MERGE (d)-[:RESOLVES_TO]->(i)",
                       domain_name=domain_name, ipv6_address=ipv6_address)
            
            # Create relationships for MX records
            for mx_record in mx_records:
                tx.run("MERGE (m:MailServer {name: $mx_record})",
                       mx_record=mx_record)
                tx.run("MATCH (d:Domain {name: $domain_name}), "
                       "(m:MailServer {name: $mx_record}) "
                       "MERGE (d)-[:USES_MAIL_SERVER]->(m)",
                       domain_name=domain_name, mx_record=mx_record)
            
            # Create relationships for NS records
            for ns_record in ns_records:
                tx.run("MERGE (n:NameServer {name: $ns_record})",
                       ns_record=ns_record)
                tx.run("MATCH (d:Domain {name: $domain_name}), "
                       "(n:NameServer {name: $ns_record}) "
                       "MERGE (d)-[:USES_NAME_SERVER]->(n)",
                       domain_name=domain_name, ns_record=ns_record)
            
            # Create relationships for TXT records
            for txt_record in txt_records:
                tx.run("MERGE (t:TextRecord {value: $txt_record})",
                       txt_record=txt_record)
                tx.run("MATCH (d:Domain {name: $domain_name}), "
                       "(t:TextRecord {value: $txt_record}) "
                       "MERGE (d)-[:HAS_TEXT_RECORD]->(t)",
                       domain_name=domain_name, txt_record=txt_record)
            
            # Create relationships for SOA records
            for soa_record in soa_records:
                tx.run("MERGE (s:SOARecord {value: $soa_record})",
                       soa_record=soa_record)
                tx.run("MATCH (d:Domain {name: $domain_name}), "
                       "(s:SOARecord {value: $soa_record}) "
                       "MERGE (d)-[:HAS_SOA_RECORD]->(s)",
                       domain_name=domain_name, soa_record=soa_record)

# Establish Neo4j connection and run the import transaction
driver = GraphDatabase.driver(uri, auth=(username, password))
with driver.session() as session:
    # Read JSON data from file
    with open('YOUR_PATH', 'r') as file:
        dns_data = json.load(file)
    
    # Import DNS data
    session.write_transaction(import_dns_data, dns_data)

    # Create relationships between domains with the same IP address
    session.run("MATCH (i:IPAddress)<-[:RESOLVES_TO]-(d:Domain) "
                "WITH i, collect(d) AS domains "
                "WHERE size(domains) > 1 "
                "UNWIND domains AS d1 "
                "UNWIND domains AS d2 "
                "WITH d1, d2 "
                "WHERE id(d1) < id(d2) "
                "MERGE (d1)-[:SHARES_IP_WITH]->(d2)")

# Close Neo4j driver
driver.close()
