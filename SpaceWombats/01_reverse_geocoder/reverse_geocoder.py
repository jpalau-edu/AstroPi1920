############################################################################
# 
# TEAM SPACE WOMBATS
#
# Institut d'Altafulla, Tarragona (Spain)
# 
# MISSION SPACE LAB 2020: Are wildfire burn scars visible from space?
# 
############################################################################
# 
# We run reverse_geocoder library on csv file to have an initial clue as to what locations
# has ISS passed over.
#
############################################################################

import reverse_geocoder as rg
import csv

new_rows_list = []
with open('reverse_geocoder-input.csv', mode='r') as entrada:
    reader = csv.reader(entrada)
    for row in reader:
        if row[6] == 'Day':
            coordinates = (float(row[3]), float(row[4]))
            results = rg.search(coordinates, mode=1) # default mode = 2
            new_row = [row[2], row[3], row[4], results]
            new_rows_list.append(new_row)
    entrada.close()   # <---IMPORTANT

with open('reverse_geocoder-output.csv', mode='w') as sortida:
    writer = csv.writer(sortida, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerows(new_rows_list)
    sortida.close()
    
    
