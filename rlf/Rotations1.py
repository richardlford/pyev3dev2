#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor
from ev3dev2.motor import SpeedDPS, SpeedRPM, SpeedRPS, SpeedDPM
from time import sleep

lm = LargeMotor()
#lm.on_for_rotations(speed=50, rotations=5)
lm.on(speed=45)
#lm.off()
lm.wait_until_not_moving()
print("Done")
lm.off()



