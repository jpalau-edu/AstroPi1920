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
# DHT22 sensor has reading errors
# This programs gets rid of error message lines in preraration for
# subsequent calulations
#
############################################################################


import csv

new_rows_list = []
with open('input.csv', mode='r') as entrada:
    reader = csv.reader(entrada)
    next(reader) # skips (header row)
    for row in reader:
        if row[2] != 'ERROR':
            new_row = [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]]
            new_rows_list.append(new_row)
    entrada.close()   # <---IMPORTANT

with open('output.csv', mode='w') as sortida:
    writer = csv.writer(sortida, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerows(new_rows_list)
    sortida.close()

    
    

