# This Python file uses the following encoding: utf-8
import requests
import json
import sys
import argparse
import time
import paho.mqtt.client as mqtt
from datetime import datetime

# cmd: --host 192.168.1.100 --user User --pwd password --broker 127.0.0.1:1883 --update 20

def create_parser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('--host', required=True)
    parser.add_argument ('--user', required=True)
    parser.add_argument ('--pwd', required=True)
    parser.add_argument ('--broker', default = "127.0.0.1:1883")
    parser.add_argument ('--update', default = 60, type = int)

    return parser

if __name__ == "__main__":
    parser = create_parser()
    namespace = parser.parse_args()
    print (namespace, flush=True)

url_thermal_str = "https://%s/rest/v1/Chassis/1/Thermal" % namespace.host

while True:
    print("---- " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " ----", flush=True)
    requests_url = requests.get(url_thermal_str, verify=False, auth=(namespace.user, namespace.pwd), timeout=5)
    data_content = requests_url.content  # Content of response
    parsed_string = json.loads(data_content)
    json_array = parsed_string["Temperatures"]

    for item in json_array:
        print(item['Name'] + " [" + item['PhysicalContext'] + "] : " + str(item['ReadingCelsius']), flush=True)
    time.sleep(namespace.update)  # seconds
