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
# Since reverse_geocoder library results are inaccurated,
# we plot the ISS path during our experiment to have a better idea as to what locations 
# has ISS passed over (yellow dots are for day and blue for night)
# Inspired on 
#     https://projects.raspberrypi.org/en/projects/where-is-the-space-station
#
############################################################################

import turtle
import csv

# sets screen named "finestra" and its parameters (dimensions, coordinates range, background)
finestra= turtle.Screen()
finestra.setup(720, 360)
finestra.setworldcoordinates(-180, -90, 180, 90)
finestra.bgpic('map.gif')


# sets a turtle named "punt" and its parameters (color, visibilty, pencil status)
# since turtle won't show, orientation desn't matter
punt = turtle.Turtle()
punt.color('yellow')
punt.hideturtle()
punt.penup()


with open('ISS-posttracker-input.csv', mode='r') as entrada:
    reader = csv.reader(entrada)
    next(reader) # skips header row
    for row in reader:
        y, x = (round(float(row[3]), 0), round(float(row[4]), 0))
        
        if row[6] == 'Day':
            punt.goto(x, y) # turtle goes to X,Y
            punt.color('yellow')
            punt.dot(5) # turtle stamps a yellow dot on X,Y
        
        else:
            punt.goto(x, y) # turtle goes to X,Y
            punt.color('blue')
            punt.dot(5) # turtle stamps a blue dot on X,Y
                       
            
    entrada.close()   # <---IMPORTANT
    





