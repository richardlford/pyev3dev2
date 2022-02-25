#!/usr/bin/env python3
from ev3dev2.motor import MoveTank, MediumMotor, MoveSteering, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from time import sleep

tank_pair = MoveTank(OUTPUT_B, OUTPUT_C)
# drive in a turn for 10 rotations of the outer (faster) motor
tank_pair.on_for_rotations(left_speed=50, right_speed=75, rotations=10)
