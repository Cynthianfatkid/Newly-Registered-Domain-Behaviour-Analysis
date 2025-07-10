import shodan
from vtapi3 import VirusTotalAPIIPAddresses, VirusTotalAPIError
from greynoise import GreyNoise
#from censys.search import CensysHosts
import requests
import json
import ipaddress
from datetime import date, timedelta
import os

def check_ip_in_firehol(ip):
    firehol_lists_directory = "YOUR_PATH"
    for filename in os.listdir(firehol_lists_directory):
        if filename.endswith(".ipset"):
            with open(os.path.join(firehol_lists_directory, filename), "r") as file:
                if ip in file.read():
                    return True
    return False

today = date.today()
yesterday = today - timedelta(days = 5)

SHODAN_API_KEY = "YOUR_API_KEY"
VT_API_KEY = "YOUR_API_KEY"
GREY_API_KEY = "YOUR_API_KEY"
#CENCYS_ID = "YOUR_API_KEY"
#CENCYS_SECRET = "YOUR_API_KEY"
ABUSEIP_API_KEY = "YOUR_API_KEY"

with open("YOUR_PATH"+str(yesterday)+".txt", "r") as file:
    ips = file.read().splitlines()

count = 0 #counter for checked IPs

def shodan_search(target):
    s_api = shodan.Shodan(SHODAN_API_KEY)
    try:
        host = s_api.host(target, history=True)
        with open("YOUR_PATH+".json", "a") as outfile:
            json.dump(host, outfile, indent=4)
    except shodan.APIError as error:
        if error == "No information available for that IP.":
            pass
        else:
            pass

def vt_search(target):
    vt_api_ip_addresses = VirusTotalAPIIPAddresses(VT_API_KEY)
    try:
        result = vt_api_ip_addresses.get_report(target)
    except VirusTotalAPIError as err:
        print(err, err.err_code)
    else:
        if vt_api_ip_addresses.get_last_http_error() == vt_api_ip_addresses.HTTP_OK:
            result = json.loads(result)
            result = json.dumps(result, sort_keys=False, indent=4)
            vt_results.write(result)
        else:
            print('HTTP Error [' + str(vt_api_ip_addresses.get_last_http_error()) +']')

def grey_search(target):
    grey_api = GreyNoise(api_key=GREY_API_KEY, offering='community')
    try:
        t = target.strip('\\n')
        res = grey_api.ip(t)
        with open("YOUR_PATH"+str(yesterday)+".json", "a") as outfile:
            json.dump(res, outfile, indent=4)
    except Exception as error:
        pass

"""def censys_search(target):
    c_api = CensysHosts(api_id=CENCYS_ID, api_secret=CENCYS_SECRET)
    t = target.strip('\\n')
    host = c_api.view(t)
    with open("censys_data.json", "a") as outfile:
        json.dump(host, outfile)
"""

def abuseip_search(target):
    url = 'https://api.abuseipdb.com/api/v2/check'
    t = target.strip('\\n')
    if ipaddress.ip_address(t).is_private is False:
        headers = {
            'Key': ABUSEIP_API_KEY,
            'Accept': 'application/json',
        }
        params = {
            'maxAgeInDays': 200,
            'ipAddress': t,
            'verbose': ''
        }
        r = requests.get(url, headers=headers, params=params)
        json_Data = json.loads(r.content)
        if 'errors' in json_Data:
            print(f"Error: {json_Data['errors'][0]['detail']}")
            exit(1)
        else:
            with open("YOUR_PATH"+str(yesterday)+".json", "a") as outfile:
                json.dump(json_Data, outfile, indent=4)

def save_firehol_results(ips):
    with open("YOUR_PATH"+str(yesterday)+".txt", "a") as output_file:
        for ip in ips:
            if check_ip_in_firehol(ip):
                output_file.write(ip + "\n")

for ip in ips:
    count += 1
    shodan_search(ip)
    #vt_search(ip)
    grey_search(ip)
    #censys_search(ip)
    abuseip_search(ip)

save_firehol_results(ips)

print("Number of checked IPs: "+ str(count))
#ips.close()
#vt_results.close()
