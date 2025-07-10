from datetime import datetime

import requests
import time
from datetime import date
from datetime import timedelta

today = date.today()
yesterday = today - timedelta(days = 5)

# get the start time
st = time.time()

print(datetime.now())

def spamhaus_black():
    mal_num = 0
    non_mal_num = 0
    result_string = ""

    for i in blcklist[9:]:
        j = i.strip('127.0.0.1  ')
        req = requests.get('https://apibl.spamhaus.net/lookup/v1/dbl/' + j, headers=headers)

        if req.status_code == 200:
            mal_num += 1
            result_string += f"I found {mal_num} malicious domains\n"
            jsonResponse = req.json()
            x = jsonResponse["resp"][0]
            if x in resp_200_dict.keys():
                result_string += f"{j} {resp_200_dict.get(jsonResponse['resp'][0])}" + "\n"
                result_string += req.content.decode('ascii') + "\n"
        elif req.status_code != 404:
            result_string += f"{j}  {req.status_code} {resp_dict[req.status_code]}" + "\n"
        else:
            non_mal_num += 1
    
    result_string += f"I found {mal_num} malicious websites and {non_mal_num} non malicious or not listed"
    return result_string


def spamhaus_nrd():
    mal_num = 0
    non_mal_num = 0
    malist =[]
    for nrd in nrdlist:
        req = requests.get('https://apibl.spamhaus.net/lookup/v1/dbl/' + nrd, headers=headers)
        if req.status_code == 200:
            mal_num += 1
            print(f"I found {mal_num} malicious domains")
            jsonResponse = req.json()
            x = jsonResponse["resp"][0]
            if x in resp_200_dict.keys():
                malist.append(nrd + " " + resp_200_dict.get(jsonResponse["resp"][0]))
                print(req.content.decode('ascii'))
        elif req.status_code != 404:
            print(f"{nrd}  {req.status_code} {resp_dict[req.status_code]}")
        else:
            non_mal_num += 1
            print(f"{nrd}  {req.status_code} {resp_dict[req.status_code]}")
    return f"Today {datetime.now()} I found {mal_num} malicious websites which are {malist} and {non_mal_num} non malicious or not listed"

with open("YOUR_PATH"+str(yesterday)+".txt", "r") as f:
    nrdlist = f.read().splitlines()
with open("YOUR_PATH"+str(yesterday)+".txt", "r") as f:
    blcklist = f.read().splitlines()

# create a dictionary for the request responses of Spamhaus
resp_dict = dict({200: "OK - At least one record was FOUND",
                  400: "Bad request - there was a syntax error in the request",
                  401: "Authorization failed - please verify a valid DQS key was supplied",
                  403: "Forbidden - Authorization denied",
                  404: "Not found - The record is not listed",
                  406: "Not Acceptable - The requested Content-Type is not supported.",
                  429: "Too Many Requests - Rate limiting in effect, please decrease query rate",
                  504: "Gateway timeout - Query could not be successfully sent"})

# create a dictionary with dict() for the 200 code of response
resp_200_dict = dict({2002: "Domain used for spam",
                      2003: "Spam domain used as a redirector / URL shortener",
                      2004: "Phishing domain",
                      2005: "Malware domain",
                      2006: "Botnet C & C domain",
                      2102: "Origin domain of abused - legit spam",
                      2103: "Origin domain of abused redirector / URL shorteners used for spam",
                      2104: "Abused - legit phishing domain",
                      2105: "Abused - legit malware domain",
                      2106: "Origin domain of abused - legit botnet C & C",
                      3002: "Domain listed in Spamhaus ZRD first observed between 0 and 2 hours ago.",
                      3003: "Domain listed in Spamhaus ZRD first observed between 2 and 3 hours ago.",
                      3004: "Domain listed in Spamhaus ZRD first observed between 3 and 4 hours ago.",
                      3023: "Domain listed in Spamhaus ZRD first observed between 22 and 23 hours ago.",
                      3024: "Domain listed in Spamhaus ZRD first observed between 23 and 24 hours ago."})

headers = {'Authorization': 'YOUR_KEY}
choice = input("Please choose if you want to check the blacklist or the newly registered domains by pressing b or n?\n")
if choice == "b":
    report = spamhaus_black()
    #print(report)
    with open("YOUR_PATH"+str(yesterday)+".txt", 'a', encoding='utf-8') as f:
        f.write(report+"\n")
elif choice == "n":
    report = spamhaus_nrd()
    print(report)
    with open("YOUR_PATH"+str(yesterday)+".txt", 'a', encoding='utf-8') as f:
        f.write(report + "\n")

# get the end time
et = time.time()

# get the execution time
elapsed_time = et - st
print('Execution time:', elapsed_time, 'seconds')
