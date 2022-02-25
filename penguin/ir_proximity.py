#!/usr/bin/env python3
from ev3dev2.sensor.lego import TouchSensor, InfraredSensor
from ev3dev2.led import Leds
from time import sleep

# Connect infrared and touch sensors to any sensor ports
ir = InfraredSensor()
ts = TouchSensor()
leds = Leds()

leds.all_off() # stop the LEDs flashing (as well as turn them off)
# is_pressed and proximity are not functions and do not need parentheses
while not ts.is_pressed:  # Stop program by pressing the touch sensor button
    if ir.proximity < 40*1.4: # to detect objects closer than about 40cm
        leds.set_color('LEFT',  'RED')
        leds.set_color('RIGHT', 'RED')
    else:
        leds.set_color('LEFT',  'GREEN')
        leds.set_color('RIGHT', 'GREEN')

    sleep (0.01) # Give the CPU a rest
