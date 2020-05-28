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
# Thanks to 2019 teams Robotiseurs, ApplePi and Astroraga for sharing their code
#   https://github.com/ecolestandre/astropi2019
#   https://github.com/ApplePi-Crew/AstroPi_MissionSpaceLab_2018-19
#   https://github.com/CoderDojoTrento/AstroPi_2018-19
#
############################################################################
#
# This code logs CPU temperature, sense-hat readings for temperature, pressure,
# humidity and a bunch of other stuff (coordinates, gyroscope...) into a csv file. 
# Meanwhile the RGB LED matrix shows diferents patterns as feedback.
#
############################################################################


import ephem
import math
from sense_hat import SenseHat
from gpiozero import CPUTemperature
import os
import logging
import logzero
from logzero import logger
from datetime import datetime
from datetime import timedelta
from time import sleep

# NORAD Two-Line Element Sets Current Data
name = "ISS (ZARYA)"
line1 = "1 25544U 98067A   20040.38944444  .00001231  00000-0  30376-4 0  9996"
line2 = "2 25544  51.6443 265.7441 0005014 245.2793  99.5753 15.49152210212043"

iss = ephem.readtle(name, line1, line2)

sense = SenseHat()
sense.clear()
sense.low_light = True

cpu = CPUTemperature()

# Sets current dir
dir_path = os.path.dirname(os.path.realpath(__file__))

# Sets a logfile name for csv file
logzero.logfile(dir_path+"/pinuts-data010.csv")

# Sets a custom logging.formatter without logger "name"
# usual is -> formatter = logging.Formatter('%(name)s - %(asctime)-15s - %(levelname)s: %(message)s');
formatter = logging.Formatter('%(asctime)-15s - %(levelname)s: %(message)s', '%Y-%m-%d %H:%M:%S');
logzero.formatter(formatter)

# Writes header row (column tags)
logger.info("___Sample,_lat_deg,_lon_deg,_CPU_Temp,_____Temp,____Press,____Humid,_____Roll,____Pitch,______Yaw,\
_____MagX,_____MagY,_____MagZ,_____AccX,_____AccY,_____AccZ,____GyroX,____GyroY,____GyroZ")

start_time = datetime.now() # sets start time as actual real time at starting moment (h:m:s)
now_time = datetime.now() # sets time at any given moment as actual real time at that moment (h:m:s)

sample_counter = 1

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

while (now_time < start_time + timedelta(minutes=2)): # loop cycles as long as actual real time is less than start_time + timedelta
    try:
        sense.set_pixels(hdd()) # displays writing on memory icon (green arrow)
        
        iss.compute() # computes latitude and longitude in case it might be useful later
        lat_deg = float(round(math.degrees(iss.sublat), 4)) # latitude and longitude format to degrees only, rounded to 4 decimals
        lon_deg = float(round(math.degrees(iss.sublong), 4))
        
        cpu_temp = round(cpu.temperature, 2)
        
        temp = round(sense.get_temperature(), 2) # writes data from senseHat sensors
        pres = round(sense.get_pressure(), 2)
        hum = round(sense.get_humidity(), 2)
        
        o = sense.get_orientation() # writes orientation data from gyroscope
        pitch = round(o["pitch"], 4)
        roll = round(o["roll"], 4)
        yaw = round(o["yaw"], 4)
        
        mag = sense.get_compass_raw() # writes data from magnetometer
        magX = round(mag["x"], 4)
        magY = round(mag["y"], 4)
        magZ = round(mag["z"], 4)
        
        acc = sense.get_accelerometer_raw() # writes data from accelerometer
        accX = round(acc["x"], 4)
        accY = round(acc["y"], 4)
        accZ = round(acc["z"], 4)
        
        gyro = sense.get_gyroscope_raw() # writes data from gyroscope
        gyroX = round(gyro["x"], 4)
        gyroY = round(gyro["y"], 4)
        gyroZ = round(gyro["z"], 4)
        
        logger.info("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s", sample_counter, lat_deg, lon_deg, cpu_temp, temp, pres, hum,\
                    pitch, roll, yaw, magX, magY, magZ, accX, accY, accZ, gyroX, gyroY, gyroZ)
        
        sample_counter+=1
        
        sleep(2.85) # fraction accounts for loop delay, intended to log data every 10 seconds approx
        
        for x in range (0,7):
            sense.set_pixels(icons[x]())
            sleep(1)
            
        now_time = datetime.now() # updates actual real time
        
    except Exception as e:
        logger.error("An error occurred: " + str(e))
        
sense.set_pixels(done()) # displays green checkmark

# afegit respecte mainPI12.py, que mostri green checkmark nomes durant 5 segons i esborri
sleep(5)
sense.clear()
