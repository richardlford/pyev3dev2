#!/usr/bin/env python3
from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_B
from ev3dev2.sensor.lego import TouchSensor
from time import sleep

ts = TouchSensor()
tank_pair = MoveTank(OUTPUT_A, OUTPUT_B)

tank_pair.on(left_speed=30, right_speed=30)

while not ts.is_pressed:  # while touch sensor is not pressed
    sleep(0.01)

tank_pair.off()
sleep(5)
