############################################################################
#
# TEAM PiNuts
#
# Institut d'Altafulla, Tarragona (Spain)
#
# MISSION SPACE LAB 2020: What is the "felt" temperature on ISS?
#
############################################################################
#
# This code logs DHT22 readings for subsequent testing of accuracy
# This code is a modification of mainPinuts.py
# SenseHat and DHT22 are mounted on the same raspi 3B (26 pin extended header)
# DHT22 sensor is on BCM pins BCM20(readings), BCM21(power), BOARD39(ground),
# gpiozero LED module used for powering DHT22 (gpiozero and Adafruit_DHT both use BCM numbering)
# RGB LED matrix code has been taken out for simplicity
# Ephem and TLE related stuff has also been taken out
#
############################################################################


from gpiozero import CPUTemperature
import os
import logging
import logzero
from logzero import logger
from datetime import datetime
from datetime import timedelta
from time import sleep

import Adafruit_DHT
from gpiozero import LED

cpu = CPUTemperature()


start_time = datetime.now().strftime("%Y%m%d-%H%M%S")

led = LED(21) # used to power DHT22 sensor

DHT_SENSOR = Adafruit_DHT.DHT22 # sensor model
DHT_PIN = 20 # DHT22 readings

errormsg1 = "ERROR"
errormsg2 = "Sensor failure. Check wiring."

# Sets current dir
dir_path = os.path.dirname(os.path.realpath(__file__))

# Sets a logfile name for csv file
logzero.logfile(dir_path+"/calibraDHT22_NoSense_{}.csv".format(start_time))

# Sets a custom logging.formatter without logger "name"
# usual is -> formatter = logging.Formatter('%(name)s - %(asctime)-15s - %(levelname)s: %(message)s');
formatter = logging.Formatter('%(asctime)-15s,%(levelname)s,%(message)s', '%Y%m%d-%H%M%S');
logzero.formatter(formatter)

# Writes header row (column tags)
logger.info("____Sample,__CPU_Temp,__DHT_Temp,_DHT_Humid")

start_time = datetime.now() # sets start time as actual real time at starting moment (h:m:s)
now_time = datetime.now() # sets time at any given moment as actual real time at that moment (h:m:s)


sample_counter = 1
led.on() # DHT22 sensor power on

while (now_time < start_time + timedelta(minutes=180)): # loop cycles as long as actual real time is less than start_time + timedelta
    try:
        cpu_temp = round(cpu.temperature, 2)

        DHT_Humid, DHT_Temp = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)

        if DHT_Humid is not None and DHT_Temp is not None:
            DHT_HumidR = round(DHT_Humid, 2)
            DHT_TempR = round(DHT_Temp, 2)
            logger.info("%s,%s,%s,%s", sample_counter, cpu_temp, DHT_TempR, DHT_HumidR)
            sample_counter+=1
        else:
            #print("Sensor failure. Check wiring.");
            logger.info("%s,%s", errormsg1, errormsg2)

        sleep(7.5) # fraction accounts for loop delay, intended to log data every 30 seconds approx

        for n in range (0,3):
            for x in range (0,7):
                # previously in this line -> sense.set_pixels(icons[x]())
                sleep(1)

        now_time = datetime.now() # updates actual real time

    except Exception as e:
        logger.error("An error occurred: " + str(e))

sleep(2)
led.off()# DHT22 sensor power off

