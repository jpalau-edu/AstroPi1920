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
#
# This code logs CPU temperature, sense-hat and DHT22 readings for temperature and humidity in
# order to compute correction factors for sense-hat readings. DHT22 has been tested for accuracy.
#
# This code is a modification of mainPinuts.py
# SenseHat and DHT22 are mounted on the same raspi 3B (26+2 pin extended header)
# DHT22 sensor is on BCM pins BCM20(readings), BCM21(power), BOARD39(ground),
# gpiozero LED module used for powering DHT22 (gpiozero and Adafruit_DHT both use BCM numbering)
# Ephem and TLE related stuff has been taken out from original code
# RGB LED matrix code has been kept for feedback while running
# 
############################################################################


from sense_hat import SenseHat
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

sense = SenseHat()
sense.clear()
sense.low_light = True

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
logzero.logfile(dir_path+"/get-factor_{}.csv".format(start_time))

# Sets a custom logging.formatter without logger "name"
# usual is -> formatter = logging.Formatter('%(name)s - %(asctime)-15s - %(levelname)s: %(message)s');
formatter = logging.Formatter('%(asctime)-15s,%(levelname)s,%(message)s', '%Y%m%d-%H%M%S');
logzero.formatter(formatter)

# Writes header row (column tags)
logger.info("____Sample,__CPU_Temp,_senseTemp,_sensHumid,_sensePres,__DHT_Temp,_DHT_Humid, _temp_diff, __hum_diff, temp_factor, hum_factor")

start_time = datetime.now() # sets start time as actual real time at starting moment (h:m:s)
now_time = datetime.now() # sets time at any given moment as actual real time at that moment (h:m:s)

# sets RGB color values
R = (255, 0, 0)
G = (0, 255, 0)
B = (0, 0, 255)
O = (0, 0, 0)# sets RGB values for black (OFF)

def hdd(): # sets icons for writing time (green arrow)
    logo = [
    B, B, B, B, B, B, B, B,
    B, O, G, G, G, G, O, B,
    B, O, G, G, G, G, O, B,
    B, O, G, G, G, G, O, B,
    B, G, G, G, G, G, G, B,
    B, O, G, G, G, G, O, B,
    B, O, O, G, G, O, O, B,
    B, B, B, B, B, B, B, B,
    ]
    return logo

def wait1():  # sets icons for waiting time (sand clock 1)
    logo = [
    B, B, B, B, B, B, B, B,
    B, R, R, R, R, R, R, B,
    O, B, R, R, R, R, B, O,
    O, O, B, R, R, B, O, O,
    O, O, B, O, O, B, O, O,
    O, B, O, O, O, O, B, O,
    B, O, O, O, O, O, O, B,
    B, B, B, B, B, B, B, B,
    ]
    return logo

def wait2():  # sets icons for waiting time (sand clock 2)
    logo = [
    B, B, B, B, B, B, B, B,
    B, R, R, O, O, R, R, B,
    O, B, R, R, R, R, B, O,
    O, O, B, R, R, B, O, O,
    O, O, B, R, R, B, O, O,
    O, B, O, O, O, O, B, O,
    B, O, O, O, O, O, O, B,
    B, B, B, B, B, B, B, B,
    ]
    return logo

def wait3():  # sets icons for waiting time (sand clock 3)
    logo = [
    B, B, B, B, B, B, B, B,
    B, R, O, O, O, O, R, B,
    O, B, R, R, R, R, B, O,
    O, O, B, R, R, B, O, O,
    O, O, B, R, R, B, O, O,
    O, B, O, R, R, O, B, O,
    B, O, O, O, O, O, O, B,
    B, B, B, B, B, B, B, B,
    ]
    return logo

def wait4():  # sets icons for waiting time (sand clock 4)
    logo = [
    B, B, B, B, B, B, B, B,
    B, O, O, O, O, O, O, B,
    O, B, R, R, R, R, B, O,
    O, O, B, R, R, B, O, O,
    O, O, B, R, R, B, O, O,
    O, B, O, R, R, O, B, O,
    B, O, O, R, R, O, O, B,
    B, B, B, B, B, B, B, B,
    ]
    return logo

def wait5():  # sets icons for waiting time (sand clock 5)
    logo = [
    B, B, B, B, B, B, B, B,
    B, O, O, O, O, O, O, B,
    O, B, R, O, O, R, B, O,
    O, O, B, R, R, B, O, O,
    O, O, B, R, R, B, O, O,
    O, B, O, R, R, O, B, O,
    B, O, R, R, R, R, O, B,
    B, B, B, B, B, B, B, B,
    ]
    return logo

def wait6():  # sets icons for waiting time (sand clock 6)
    logo = [
    B, B, B, B, B, B, B, B,
    B, O, O, O, O, O, O, B,
    O, B, O, O, O, O, B, O,
    O, O, B, R, R, B, O, O,
    O, O, B, R, R, B, O, O,
    O, B, O, R, R, O, B, O,
    B, R, R, R, R, R, R, B,
    B, B, B, B, B, B, B, B,
    ]
    return logo

def wait7():  # sets icons for waiting time (sand clock 7)
    logo = [
    B, B, B, B, B, B, B, B,
    B, O, O, O, O, O, O, B,
    O, B, O, O, O, O, B, O,
    O, O, B, O, O, B, O, O,
    O, O, B, R, R, B, O, O,
    O, B, R, R, R, R, B, O,
    B, R, R, R, R, R, R, B,
    B, B, B, B, B, B, B, B,
    ]
    return logo

def done():  # sets icon for end of program (green checkmark)
    logo = [
    O, O, O, O, O, O, O, G,
    O, O, O, O, O, O, G, G,
    O, O, O, O, O, G, G, G,
    G, G, O, O, G, G, G, O,
    G, G, G, G, G, G, O, O,
    O, G, G, G, G, O, O, O,
    O, O, G, G, O, O, O, O,
    O, O, O, O, O, O, O, O,
    ]
    return logo

icons = [wait1, wait2, wait3, wait4, wait5, wait6, wait7]

sample_counter = 1
led.on() # DHT22 sensor power on

while (now_time < start_time + timedelta(minutes=10)): # loop cycles as long as actual real time is less than start_time + timedelta
    try:
        sense.set_pixels(hdd()) # displays "writing on memory" icon (green arrow)
        cpu_tempR = round(cpu.temperature, 2)
        senseTempR = round(sense.get_temperature(), 2) # writes data from senseHat sensors
        sensHumidR = round(sense.get_humidity(), 2)
        sensePresR = round(sense.get_pressure(), 2)

        DHT_Humid, DHT_Temp = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
        

        if DHT_Humid is not None and DHT_Temp is not None:
            DHT_HumidR = round(DHT_Humid, 2)
            DHT_TempR = round(DHT_Temp, 2)
            
            temp_diff = senseTempR-DHT_TempR
            hum_diff = sensHumidR-DHT_HumidR
            temp_factorR = round((cpu_tempR-senseTempR)/(senseTempR-DHT_TempR), 2)
            hum_factorR = round((cpu_tempR-sensHumidR)/(sensHumidR-DHT_HumidR), 2)
            
            logger.info("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s", sample_counter, cpu_tempR, senseTempR, sensHumidR, sensePresR,\
             DHT_TempR, DHT_HumidR, temp_diff, hum_diff, temp_factorR, hum_factorR)
            
            sample_counter+=1
        
        else:
            #print("Sensor failure. Check wiring.");
            logger.info("%s,%s", errormsg1, errormsg2)

        sleep(7.5) # fraction accounts for loop delay, intended to log data every 30 seconds approx

        for n in range (0,3):
            for x in range (0,7):
                sense.set_pixels(icons[x]())
                sleep(1.5)

        now_time = datetime.now() # updates actual real time

    except Exception as e:
        logger.error("An error occurred: " + str(e))

sense.set_pixels(done()) # displays green checkmark

sleep(2)
sense.clear() # matrix off
led.off()# DHT22 sensor power off

