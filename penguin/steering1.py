#!/usr/bin/env python3
from ev3dev2.motor import MediumMotor, MoveSteering, OUTPUT_A, OUTPUT_D
from time import sleep

steer_pair = MoveSteering(OUTPUT_A, OUTPUT_D, motor_class=MediumMotor)

steer_pair.on_for_seconds(steering=0, speed=50, seconds=2)

# You must use a matching pair of motors, so you can't pair a large motor with a medium motor.
