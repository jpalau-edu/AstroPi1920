#! /bin/bash

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
# bash script to increase CPU temperatures
# in order to show effect on sensehat temperature and humidity readings
# for two times it uses a series of 4 sysbench runs preceded by stabilisation lapse of 10 min
# it shows onscreen CPU temp before each sysbench instance and records to log file
#
#############################################################################

day=$(date +"%Y%m%d-%H%M%S")
touch CPUvsSENSE-stresser-log_${day}.txt
for n in {1..2}
do 
	now=$(date +"%Y%m%d-%H%M%S")
	echo $now
	echo $now >> CPUvsSENSE-stresser-log_${day}.txt
	sleep 600 # per defecte són segons sinó 5m300)
	for i in {1..4}
	do
		now=$(date +"%Y%m%d-%H%M%S")
		temp=$(/opt/vc/bin/vcgencmd measure_temp)
		echo $now","$i","$temp
		echo $now","$i","$temp >> CPUvsSENSE-stresser-log_${day}.txt
		echo >> CPUvsSENSE-stresser-log_${day}.txt
		sysbench --test=cpu --cpu-max-prime=20000 --num-threads=4 run >> CPUvsSENSE-stresser-log_${day}.txt
		echo "---------------------------" >> CPUvsSENSE-stresser-log_${day}.txt
		echo >> CPUvsSENSE-stresser-log_${day}.txt	
	done
now=$(date +"%Y%m%d-%H%M%S")
temp=$(/opt/vc/bin/vcgencmd measure_temp)
echo $now","$i","$temp
echo $now","$i","$temp >> CPUvsSENSE-stresser-log_${day}.txt
echo "===========================" >> CPUvsSENSE-stresser-log_${day}.txt
echo >> CPUvsSENSE-stresser-log_${day}.txt
done

