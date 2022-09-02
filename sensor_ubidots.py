from pickletools import long1
import time
import requests
import math
import random
from tkinter import Variable
import Adafruit_DHT

import RPi.GPIO as GPIO



TOKEN = "BBFF-J8QLbnk0OI8qfh4CGKWxF08BR89J6n"  
DEVICE_LABEL = "rizkiihsan_ubi"   
VARIABLE_LABEL_1 = "LDR"  
VARIABLE_LABEL_2 = "SUHU"
VARIABLE_LABEL_3 = "KELEMBABAN"
VARIABLE_LABEL_4 = "POSISI"








def build_payload(pin_to_circuit, varia_2, varia_3, varia_4):

    GPIO.setmode(GPIO.BOARD)
    pin_to_circuit = 11

    hitung = 0

    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    time.sleep(5)
    GPIO.setup(pin_to_circuit, GPIO.IN)
  
    while (GPIO.input(pin_to_circuit) == GPIO.LOW):

        hitung += 1
    
    DHT_SENSOR = Adafruit_DHT.DHT11
    DHT_PIN = 4
    kelembaban, suhu = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
 
    
             

    value_1 = hitung
    value_2 = suhu
    value_3 = kelembaban
    
    lat = -7.108717
    lng = 106.878470
    

   

    payload = {pin_to_circuit: value_1,
               varia_2: value_2,
               varia_3: value_3,
               varia_4: {"value": 1, "context": {"lat": lat, "lng": lng}}}

    return payload


   


def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    print(req.status_code, req.json())
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True


def main():
    payload = build_payload(
        VARIABLE_LABEL_1, VARIABLE_LABEL_2, VARIABLE_LABEL_3, VARIABLE_LABEL_4)

    print("[INFO] Attemping to send data")
    post_request(payload)
    print("[INFO] finished")


    


if __name__ == '__main__':
    while (True):
        main()
        time.sleep(1)



  
