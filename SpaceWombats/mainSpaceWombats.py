############################################################################
# 
# TEAM SPACE WOMBATS
#
# Institut d'Altafulla, Tarragona (Spain)
# 
# MISSION SPACE LAB 2020: Are wildfire burn scars visible from space?
# 
############################################################################
# NoIR camera takes pictures with the blue filter on about every 10 seconds and loggs
# corresponding coordinates into a csv file as well as into picture's EXIF data.
# Pictures are taken at maximum resolution (2592x1944) and saved in jpeg format.
# In order to save storage space and skip night pictures the code tests for day or night 
# before shooting. This is achieved by using the PyEphem astronomy library to measure the height
# of the sun above horizon for the location ISS was passing over. 
# 
############################################################################
#
# Thansk to 2019 teams Robotiseurs, ApplePi and Astroraga for sharing their code
#   https://github.com/ecolestandre/astropi2019
#   https://github.com/ApplePi-Crew/AstroPi_MissionSpaceLab_2018-19
#   https://github.com/CoderDojoTrento/AstroPi_2018-19
#
############################################################################


import os
import ephem
import logging
import logzero
from logzero import logger
from datetime import datetime
from datetime import timedelta
import math
from picamera import PiCamera
from time import sleep


# Sets current dir
dir_path = os.path.dirname(os.path.realpath(__file__))

# NORAD Two-Line Element Sets Current Data
name = "ISS (ZARYA)"
line1 = "1 25544U 98067A   20040.38944444  .00001231  00000-0  30376-4 0  9996"
line2 = "2 25544  51.6443 265.7441 0005014 245.2793  99.5753 15.49152210212043"
iss = ephem.readtle(name, line1, line2)

# Sets restrictive custom twilight angle in degrees for day/night detection so as to/not to take picture
sun = ephem.Sun()
twilight_deg = round(float(0))


# Sets a logfile name for csv file
logzero.logfile(dir_path+"/swombats-data01.csv")


# Sets a custom logging.formatter without logger "name"
# usual is -> formatter = logging.Formatter('%(name)s - %(asctime)-15s - %(levelname)s: %(message)s');
formatter = logging.Formatter('%(asctime)-15s,%(levelname)s,%(message)s', '%Y-%m-%d %H:%M:%S');
logzero.formatter(formatter)

# Writes header row (column tags)
logger.info("photo_counter, lat_deg, lon_deg, sun_angle_deg, day_or_night")


cam = PiCamera()
cam.resolution = (2592,1944) # Highest valid resolution for V1 camera

def get_latlon():
    iss.compute() # Gets the lat/long values from ephem and write to EXIF data

    long_value = [float(i) for i in str(iss.sublong).split(":")]

    if long_value[0] < 0:

        long_value[0] = abs(long_value[0])
        cam.exif_tags['GPS.GPSLongitudeRef'] = "W"
    else:
        cam.exif_tags['GPS.GPSLongitudeRef'] = "E"
    cam.exif_tags['GPS.GPSLongitude'] = '%d/1,%d/1,%d/10' % (long_value[0], long_value[1], long_value[2]*10)

    lat_value = [float(i) for i in str(iss.sublat).split(":")]

    if lat_value[0] < 0:

        lat_value[0] = abs(lat_value[0])
        cam.exif_tags['GPS.GPSLatitudeRef'] = "S"
    else:
        cam.exif_tags['GPS.GPSLatitudeRef'] = "N"

    cam.exif_tags['GPS.GPSLatitude'] = '%d/1,%d/1,%d/10' % (lat_value[0], lat_value[1], lat_value[2]*10)


start_time = datetime.now() # sets start time as actual real time at starting moment (h:m:s)
now_time = datetime.now() # sets time at any given moment as actual real time at that moment (h:m:s)

photo_counter = 1

while (now_time < start_time + timedelta(minutes=178)): # loop cycles as long as actual real time is less than start_time + timedelta
    try:
        cam.start_preview()
        sleep(3)

        iss.compute()
        observer = ephem.Observer() # sets a sun observer with ISS coordinates and zero elevation
        observer.lat, observer.long, observer.elevation = iss.sublat, iss.sublong, 0

        lat_deg = float(round(math.degrees(iss.sublat), 6)) # latitude and longitude format to degrees only, rounded to 6 decimals
        lon_deg = float(round(math.degrees(iss.sublong), 6))
        sun.compute(observer)
        sun_angle_deg = float(round(math.degrees(sun.alt), 6)) # sun altitude format to degrees only, rounded to 6 decimals

        day_or_night = "Day" if sun_angle_deg > twilight_deg else "Night"

        if sun_angle_deg > twilight_deg: # if day time, takes picture and logs data
            get_latlon()
            cam.capture(dir_path+"/swombats_"+ str(photo_counter).zfill(3)+".jpg")
            logger.info("%s,%s,%s,%s,%s", photo_counter, lat_deg, lon_deg, sun_angle_deg, day_or_night)
            photo_counter+=1
        else: # if night time, logs data, doesn't take picture
            logger.info("%s,%s,%s,%s,%s", photo_counter, lat_deg, lon_deg, sun_angle_deg, day_or_night)

        cam.stop_preview()

        sleep(6.2) #  fraction accounts for loop's runtime delay (intended to log data every 10 seconds approx)
        now_time = datetime.now() # updates actual real time

    except Exception as e:
        logger.error("An error occurred: " + str(e))
