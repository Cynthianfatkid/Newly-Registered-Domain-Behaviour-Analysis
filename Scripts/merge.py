import json
from datetime import date
from datetime import timedelta

today = date.today()
#today = today.strftime("%d_%m_%Y")
yesterday = today - timedelta(days = 1)

def merge_records(file1, file2):
    # Step 1: Read the content of both JSON files
    with open(file1, 'r') as f1:
        json_data1 = json.load(f1)

    with open(file2, 'r') as f2:
        json_data2 = json.load(f2)

    # Step 2: Merge records
    for domain, data2 in json_data2.items():
        if domain in json_data1:
            # Update existing records or add new records
            existing_records = json_data1[domain]["records"]
            new_records = data2["records"]
            for new_record in new_records:
                if new_record not in existing_records:
                    existing_records.append(new_record)
        else:
            # If the domain doesn't exist in the first file, add it
            json_data1[domain] = data2

    # Step 3: Write the merged dictionary back to file1
    with open(file1, 'w') as f1:
        json.dump(json_data1, f1, indent=2)

# Example usage:
file1_path = 'YOUR_PATH'
file2_path = 'YOUR_PATH'+str(today)+'.json'

merge_records(file1_path, file2_path)
