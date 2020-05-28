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
# Our code recorded CPU temperature and sensor-hat readings for temperature, humidity
# and a bunch of other stuff (coordinates, gyroscope...)just in case.
# Now we get rid of them to make a more manageable file
#
############################################################################

import csv

new_rows_list = []
with open('input.csv', mode='r') as entrada:
    reader = csv.reader(entrada)
    #next(reader) # skips (header row)
    for row in reader:
        new_row = [row[0], row[3], row[4], row[5], row[6]]
        new_rows_list.append(new_row)
    entrada.close()   # <---IMPORTANT

with open('output.csv', mode='w') as sortida:
    writer = csv.writer(sortida, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerows(new_rows_list)
    sortida.close()

