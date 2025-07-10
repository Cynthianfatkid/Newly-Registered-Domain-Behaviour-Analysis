import json

# Read JSON data from file
with open('YOUR_PATH', 'r') as file:
    json_data = file.read()

# Load JSON data
data = json.loads(json_data)

# Create a dictionary to store domains with the same A and date
domains_with_same_a_and_date = {}

# Iterate through each domain
for domain, info in data.items():
    records = info.get("records", [])
    for record in records:
        date = record.get("date")
        A = record.get("A", [])
        for ip in A:  # Iterate through each IP associated with the domain
            key = (date, ip)
            if key not in domains_with_same_a_and_date:
                domains_with_same_a_and_date[key] = []
            domains_with_same_a_and_date[key].append(domain)

# Write output to a text file
with open('YOUR_PATH', 'w') as output_file:
    output_file.write("Domains with the same A and date:\n")
    previous_date = None
    for (date, ip), domains in sorted(domains_with_same_a_and_date.items()):
        if len(domains) > 1:  # Check if there are more than one domain for this date and IP
            if date != previous_date:
                output_file.write(f"\nDate: {date}\n")
                previous_date = date
            output_file.write(f"IP: {ip}\n")
            output_file.write(f"Domains: {', '.join(domains)}\n\n")
