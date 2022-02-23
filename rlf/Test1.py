#!/usr/bin/env python3

from time import sleep

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank, SpeedRPM
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds
print("Executed from EV3")
m = LargeMotor(address=OUTPUT_A)
m.on_for_rotations(rotations=5, speed=SpeedRPM(500))
