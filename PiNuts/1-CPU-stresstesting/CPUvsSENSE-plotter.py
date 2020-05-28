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
# Program to plot data sense-hat readings and corresponding CPU temperatures
# data was logged by modified version of mainPinuts.py
#
#############################################################################

import csv
from matplotlib import pyplot as plt

x = []
cpu = []
sense_temp = []
sense_hum = []
sense_pres = []

with open('inputfile.csv', mode='r') as inputfile:
    reader = csv.reader(inputfile)
    next(reader) # skips header row, comment out if none
    for row in reader:
        x.append(row[2])
        cpu.append(row[3])
        sense_temp.append(row[4])
        sense_hum.append(row[5])
        sense_pres.append(row[6])
      
# Lists are alphanumeric, can't be plotted. Need to converted into int or float types
x = [int(i) for i in x]
cpu = [round(float(i), 1) for i in cpu]
sense_temp = [round(float(i), 1) for i in sense_temp]
sense_hum = [round(float(i), 1) for i in sense_hum]
#  pressure values divided by 100 to bring them closer to temperature ranges
sense_pres = [round((float(i)/100), 1) for i in sense_pres]


plt.title('Effect of CPU temperature on sense hat readings', fontsize=26, fontweight='bold')
plt.xlabel('Time', fontsize=24, fontweight='bold')
plt.xticks(fontsize=18, fontweight='bold')
plt.ylabel('Values: ºC, %, dbar', fontsize=24, fontweight='bold')
plt.yticks(fontsize=18, fontweight='bold')

plt.ylim(0, 100)

plt.plot(x,cpu, linewidth=3, label='cpu')
plt.plot(x,sense_temp, linewidth=5, label='sense_temp')
plt.plot(x,sense_hum, linewidth=5, label='sense_hum')
plt.plot(x,sense_pres, linewidth=5, label='sense_pres')


plt.legend(["cpu_temp", "sense_temp", "sense_hum", "sense_pres"], fontsize=28)

plt.show() 

