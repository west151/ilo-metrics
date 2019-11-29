# This Python file uses the following encoding: utf-8
import requests
import json
import sys
import argparse
import time
import paho.mqtt.client as mqtt
from datetime import datetime

topic_01_inlet_ambient="hp_microserver/01_inlet_ambient"
topic_02_cpu="hp_microserver/02_cpu"
topic_03_p1_dimm_1_2="hp_microserver/03_p1_dimm_1_2"
topic_04_hd_max="hp_microserver/04_hd_max"
topic_05_chipset="hp_microserver/05_chipset"
topic_06_chipset_zone="hp_microserver/06_chipset_zone"
topic_07_vr_p1_zone="hp_microserver/07_vr_p1_zone"
topic_09_ilo_zone="hp_microserver/09_ilo_zone"
topic_11_pci_1_zone="hp_microserver/11_pci_1_zone"
topic_12_sys_exhaust="hp_microserver/12_sys_exhaust"

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

broker_address = namespace.broker.split(':')[0]
broker_port = int(namespace.broker.split(':')[1])

mqttc = mqtt.Client("client-001")
mqttc.connect(broker_address, broker_port, 60)
mqttc.loop_start()

url_thermal_str = "https://%s/rest/v1/Chassis/1/Thermal" % namespace.host

while True:
    print("---- " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " ----", flush=True)
    requests_url = requests.get(url_thermal_str, verify=False, auth=(namespace.user, namespace.pwd), timeout=5)
    data_content = requests_url.content  # Content of response
    parsed_string = json.loads(data_content)
    json_array = parsed_string["Temperatures"]

    for item in json_array:
        # item['Name'] item['PhysicalContext'] item['ReadingCelsius']
        #
        if item['Name'] == '01-Inlet Ambient':
            mqttc.publish(topic_01_inlet_ambient, item['ReadingCelsius'], qos=0)
            print("publish:" + topic_01_inlet_ambient + " " + str(item['ReadingCelsius']), flush=True)
        #
        if item['Name'] == '02-CPU':
            mqttc.publish(topic_02_cpu, item['ReadingCelsius'], qos=0)
            print("publish:" + topic_02_cpu + " " + str(item['ReadingCelsius']), flush=True)
        #
        if item['Name'] == '03-P1 DIMM 1-2':
            mqttc.publish(topic_03_p1_dimm_1_2, item['ReadingCelsius'], qos=0)
            print("publish:" + topic_03_p1_dimm_1_2 + " " + str(item['ReadingCelsius']), flush=True)
        #
        if item['Name'] == '04-HD Max':
            mqttc.publish(topic_04_hd_max, item['ReadingCelsius'], qos=0)
            print("publish:" + topic_04_hd_max + " " + str(item['ReadingCelsius']), flush=True)
        #
        if item['Name'] == '05-Chipset':
            mqttc.publish(topic_05_chipset, item['ReadingCelsius'], qos=0)
            print("publish:" + topic_05_chipset + " " + str(item['ReadingCelsius']), flush=True)
        #
        if item['Name'] == '06-Chipset Zone':
            mqttc.publish(topic_06_chipset_zone, item['ReadingCelsius'], qos=0)
            print("publish:" + topic_06_chipset_zone + " " + str(item['ReadingCelsius']), flush=True)
        #
        if item['Name'] == '07-VR P1 Zone':
            mqttc.publish(topic_07_vr_p1_zone, item['ReadingCelsius'], qos=0)
            print("publish:" + topic_07_vr_p1_zone + " " + str(item['ReadingCelsius']), flush=True)
        #
        if item['Name'] == '09-iLO Zone':
            mqttc.publish(topic_09_ilo_zone, item['ReadingCelsius'], qos=0)
            print("publish:" + topic_09_ilo_zone + " " + str(item['ReadingCelsius']), flush=True)
        #
        if item['Name'] == '11-PCI 1 Zone':
            mqttc.publish(topic_11_pci_1_zone, item['ReadingCelsius'], qos=0)
            print("publish:" + topic_11_pci_1_zone + " " + str(item['ReadingCelsius']), flush=True)
        #
        if item['Name'] == '12-Sys Exhaust':
           mqttc.publish(topic_12_sys_exhaust, item['ReadingCelsius'], qos=0)
           print("publish:" + topic_12_sys_exhaust + " " + str(item['ReadingCelsius']), flush=True)

    time.sleep(namespace.update)  # seconds

mqttc.disconnect()
mqttc.loop_stop()
