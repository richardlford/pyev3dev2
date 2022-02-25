#!/usr/bin/env python3
from ev3dev2.motor import MoveSteering, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C
from ev3dev2.sensor.lego import TouchSensor
from time import sleep

ts = TouchSensor()
steer_pair = MoveSteering(OUTPUT_A, OUTPUT_B)
mm = MediumMotor(OUTPUT_C)
mm.on(speed=100)

#teer_pair.on_for_rotations(steering=-20, speed=75, rotations=10)
steer_pair.on_for_degrees(steering=-100, speed=100, degrees=1440)
#while not ts.is_pressed:  # while touch sensor is not pressed
#    sleep(0.01)
mm.off()
steer_pair.off()
sleep(5)
