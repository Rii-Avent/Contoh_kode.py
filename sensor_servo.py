
from itertools import count
import RPi.GPIO as GPIO
import time

import requests
import math
import random
from tkinter import Variable
import Adafruit_DHT





GPIO.setmode(GPIO.BOARD)


GPIO.setup(12,GPIO.OUT)
servo1 = GPIO.PWM(12,50) 
servo1.start(0)
print ("Servo1 dijalankan")
time.sleep(2)

GPIO.setup(18,GPIO.OUT)
servo2 = GPIO.PWM(18,50)
servo2.start(0)
print ("Servo2 dijalankan")
time.sleep(2)

GPIO.setmode(GPIO.BOARD)
pin_to_circuit = 11


def rc_time (pin_to_circuit):
    resist = 0
    duty = 2
    
    
   
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    time.sleep(2)




   
    GPIO.setup(pin_to_circuit, GPIO.IN)
  
   
    while (GPIO.input(pin_to_circuit) == GPIO.LOW):
        resist += 1
    

    rh_now = 0
    suhu_now = 0
    DHT_SENSOR = Adafruit_DHT.DHT11
    DHT_PIN = 4
    rh, suhu = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if rh is not None:
        rh_now = rh
    if suhu is not None:
        suhu_now = suhu


    
    
    if (resist > 0 and resist < 600) and (rh_now  >= 70) and (suhu_now <=26): #Siang, Kelembaban tinggi, suhu rendah
        print("KONDISI PERTAMA SESUAI, GORDEN TERBUKA")

        servo1.ChangeDutyCycle(0)
        servo2.ChangeDutyCycle(0)
        time.sleep(0.01)
        servo1.ChangeDutyCycle(12)
        servo2.ChangeDutyCycle(duty)
        time.sleep(1)
        servo1.ChangeDutyCycle(0)
        servo2.ChangeDutyCycle(0)
        
       


    elif (resist > 0 and resist < 600) and (rh_now <= 70) and (suhu_now >= 27) : 
        print("KONDISI KEDUA SESUAI, GORDEN DITUTUP")
        servo1.ChangeDutyCycle(12)
        servo2.ChangeDutyCycle(0)
        servo2.ChangeDutyCycle(duty)
    
    elif (resist > 600 ) and (rh_now  >= 70) and (suhu_now <=26): # Malam, kelembaban tinggi, dan suhu rendah
        print("KONDISI KETIGA SESUAI, GORDEN TERTUTUP")
       
        servo1.ChangeDutyCycle(0)
        servo2.ChangeDutyCycle(0)
        time.sleep(0.01)
        servo1.ChangeDutyCycle(duty)
        servo2.ChangeDutyCycle(12)
        time.sleep(1)
        servo1.ChangeDutyCycle(0)
        servo2.ChangeDutyCycle(0)



    elif (resist > 600 ) and (rh_now <= 70) and (suhu_now >= 27): 
        print("KONDISI KEEMPAT SESUAI, GORDEN DIBUKA")
       
        servo1.ChangeDutyCycle(duty)
        servo2.ChangeDutyCycle(0)
        servo2.ChangeDutyCycle(12)

if __name__ == '__main__':
    while (True):
     rc_time(pin_to_circuit)
     time.sleep(0.01)

    
