import json
from datetime import date
from datetime import timedelta

today = date.today()
#today = today.strftime("%d-%m-%Y")
yesterday = today - timedelta(days = 5)

def extract_A_values(json_data, output_file):
    with open(json_data, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    unique_A_values = set()

    for domain, domain_data in data.items():
        for record in domain_data.get('records', []):
            A_values = record.get('A',[])
            if A_values:
                unique_A_values.update(A_values)

    with open(output_file, 'w', encoding='utf-8') as txt_file:
        for A_value in unique_A_values:
            txt_file.write(str(A_value) + '\n')

if __name__ == "__main__":
    json_filename = "YOUR_PATH"+str(today)+".json"  # Replace this with your JSON file name
    output_filename = "YOUR_PATH"+str(yesterday)+".txt"    # Replace this with your desired output file name

    extract_A_values(json_filename, output_filename)

    print(f"A values extracted and saved to {output_filename}.")
