#!/usr/bin/env python3
from ev3dev2.motor import MoveSteer, OUTPUT_A, OUTPUT_B
from ev3dev2.sensor.lego import TouchSensor
from time import sleep

ts = TouchSensor()
steer_pair = MoveSteer(OUTPUT_A, OUTPUT_B)

steer_pair.on_for_rotations(steering=-20, speed=75, rotations=10)

while not ts.is_pressed:  # while touch sensor is not pressed
    sleep(0.01)

steer_pair.off()
sleep(5)
