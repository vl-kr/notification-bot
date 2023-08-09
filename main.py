import requests
import time
import json
from call import dial
from email_to import send_message

SLEEP_TIME_SECONDS = 10

REGISTRATION_URL = "\n\nhttps://www.old.korona.gov.sk/covid-19-vaccination-form.php"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'sk,en;q=0.8,cs;q=0.5,en-US;q=0.3',
    'Content-Type': 'application/json;charset=utf-8',
    'Origin': 'https://www.old.korona.gov.sk',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://www.old.korona.gov.sk/',
}

data1 = '{"drivein_id":"812"}' # ID for the vaccination center Kuzmanyho
data2 = '{"drivein_id":"875"}' # ID for the vaccination center J. Jiskru

def parse_json(response):
    # returns the response content in an easily readable string
    message = ""
    dct = json.loads(response)
    for item, value in dct.items():
        if item != 'payload': # we will add payload content to the end for better readability
            message += (str(item) + " " + str(value) + "\n")
    message += "PAYLOAD:\n"
    for item in dct['payload']: #
        message += (str(item) + "\n")
    return message

def free_spots_count(string):
    # returns the number of free spots in the first available date, or 0 if no such date exists
    y = json.loads(string)
    for item in y['payload']: # each item represents a single date in a specific vaccination center
        if item['is_closed'] != 1 and int(item['free_capacity']) > 0: # example item:  {'c_date': '2021-02-12', 'is_closed': '0', 'free_capacity': '1'}
            return int(item['free_capacity'])
    return 0

try:
    log_file = open("log.log", "w+")
    response1 = requests.post('https://mojeezdravie.nczisk.sk/api/v1/web/validate_drivein_times_vacc', headers=headers, data=data1)
    response2 = requests.post('https://mojeezdravie.nczisk.sk/api/v1/web/validate_drivein_times_vacc', headers=headers,data=data2)
    while True:
        while response1.status_code == 200 and response2.status_code == 200 and free_spots_count(response1.text) + free_spots_count(response2.text) <= 0:
            print(str(time.strftime("%H:%M:%S", time.localtime())) + ": no free spot, sleeping for " + str(SLEEP_TIME_SECONDS) + " seconds")
            time.sleep(SLEEP_TIME_SECONDS)
            print(str(time.strftime("%H:%M:%S", time.localtime())) + ": woke up, retrying")
            response1 = requests.post('https://mojeezdravie.nczisk.sk/api/v1/web/validate_drivein_times_vacc', headers=headers, data=data1)
            response2 = requests.post('https://mojeezdravie.nczisk.sk/api/v1/web/validate_drivein_times_vacc', headers=headers, data=data2)

        if response1.status_code == 200 and free_spots_count(response1.text) + free_spots_count(response2.text) > 0:
            try:
                message = "Subject: Free spot!\n\nVaccination center: "
                if free_spots_count(response1.text) > 0:
                    message += "Kuzmanyho\n" + parse_json(response1.text) + REGISTRATION_URL
                else:
                    message += "J. Jiskru\n" + parse_json(response2.text) + REGISTRATION_URL
                send_message(message, snd=True)
                log_file.write(str(time.strftime("%H:%M:%S", time.localtime())) + " Message sent:")
                log_file.write(message)
                log_file.write("\ncalling\n")
                dial()
            except Exception as e:
                print(e)
                message = "Subject: Code 200, \n\nJSON parsing failed\n" + response1.text + "\n" + response2.text + REGISTRATION_URL
                send_message(message, snd=True)
                log_file.write(str(time.strftime("%H:%M:%S", time.localtime())) + " Message sent:")
                log_file.write(message)
                log_file.write("\ncalling\n")
                dial()
                exit()
        elif response1.status_code != 200:
            message = "Subject: CODE " + str(response1.status_code) + "\n\n!= 200"
            send_message(message)
            log_file.write(str(time.strftime("%H:%M:%S", time.localtime())) + " Message sent:")
            log_file.write(message)
            log_file.write("\ncalling\n")
            dial()
            exit()
        else:
            log_file.write("\nunknown problem occured\n")
            exit()
        while response1.status_code == 200 and response2.status_code == 200 and free_spots_count(response1.text) + free_spots_count(response2.text) > 0:
            # this loop ensures the same free spot(s) are not reported multiple times
            log_file.write(str(time.strftime("%H:%M:%S", time.localtime())) + " Free spots Kuzmanyho = " + str(free_spots_count(response1.text)) + "\n")
            log_file.write(str(time.strftime("%H:%M:%S", time.localtime())) + " Free spots J.Jiskru = " + str(free_spots_count(response2.text)) + "\n")
            time.sleep(SLEEP_TIME_SECONDS)
            response1 = requests.post('https://mojeezdravie.nczisk.sk/api/v1/web/validate_drivein_times_vacc', headers=headers, data=data1)
            response2 = requests.post('https://mojeezdravie.nczisk.sk/api/v1/web/validate_drivein_times_vacc', headers=headers, data=data2)
        log_file.write(str(time.strftime("%H:%M:%S", time.localtime())) + "Spots are not free anymore!\n")

except Exception as e:
    print(e)
    message = "unknown error (POST REQUEST or JSON parsing)"
    send_message(message)
    dial()


