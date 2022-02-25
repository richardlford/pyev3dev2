#!/usr/bin/env python3
from ev3dev2.sensor.lego import InfraredSensor
from time import sleep

ir = InfraredSensor()
# Set the remote to channel 1


def top_left_channel_1_action(state):
    print("top_left, state="+str(state))
    move()


def bottom_left_channel_1_action(state):
    move()


def top_right_channel_1_action(state):
    move()


def bottom_right_channel_1_action(state):
    move()


def move():
    buttons = ir.buttons_pressed()  # a list
    print("buttons=" + str(buttons))

# Associate the event handlers with the functions defined above


ir.on_channel1_top_left = top_left_channel_1_action
ir.on_channel1_bottom_left = bottom_left_channel_1_action
ir.on_channel1_top_right = top_right_channel_1_action
ir.on_channel1_bottom_right = bottom_right_channel_1_action

while True:
    ir.process()
    sleep(0.01)
