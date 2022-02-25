#!/usr/bin/env python3
from ev3dev2.sensor.lego import TouchSensor, ColorSensor
from ev3dev2.sound import Sound
from time import sleep

cl = ColorSensor()
ts = TouchSensor()
sound = Sound()

# Stop program by long-pressing touch sensor button
while not ts.is_pressed:
    print(cl.color_name)
    # sound.speak(cl.color_name)
    sleep(1)