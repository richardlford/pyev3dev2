#!/usr/bin/env python3
from ev3dev2.sensor.lego import TouchSensor, UltrasonicSensor
from ev3dev2.led import Leds
from time import sleep

# Connect ultrasonic and touch sensors to any sensor port
us = UltrasonicSensor()
ts = TouchSensor()
leds = Leds()

leds.all_off()  # stop the LEDs flashing (as well as turn them off)
prev_dist = 0
while not ts.is_pressed:
    dist = us.distance_centimeters
    if dist != prev_dist:
        print("New dist=" + str(dist))
        prev_dist = dist

    if dist < 40:  # to detect objects closer than 40cm
        # In the above line you can also use inches: us.distance_inches < 16
        leds.set_color('LEFT',  'RED')
        leds.set_color('RIGHT', 'RED')
    else:
        leds.set_color('LEFT',  'GREEN')
        leds.set_color('RIGHT', 'GREEN')

    sleep(0.01)  # Give the CPU a rest
