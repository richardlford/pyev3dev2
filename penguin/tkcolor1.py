#!/usr/bin/env python3
from ev3dev2.sensor.lego import TouchSensor, ColorSensor
from ev3dev2.sound import Sound
from ev3dev2.sensor.lego import InfraredSensor
from time import sleep
import os
haveDisplay = os.environ.get('DISPLAY')
if haveDisplay:
    from tkinter import *
    from tkinter import ttk
    root = Tk()
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    lbl = ttk.Label(frm, text="Current color=")
    lbl.grid(column=0, row=0)
    color_label = ttk.Label(frm, text="")
    color_label.grid(column=1, row=0)
    buttonsCaption = ttk.Label(frm, text="Buttons=")
    buttonsCaption.grid(column=0, row=1)
    buttonsLabel = ttk.Label(frm, text="")
    buttonsLabel.grid(column=1, row=1)

cl = ColorSensor()
ts = TouchSensor()
sound = Sound()
ir = InfraredSensor()
# Set the remote to channel 1


def show_color(the_color):
    if haveDisplay:
        color_label['text'] = the_color
        root.update()
    else:
        print("Color=" + the_color)


def show_buttons(the_buttons):
    if haveDisplay:
        buttonsLabel['text'] = str(the_buttons)
    else:
        print("buttons=" + str(the_buttons))


def top_left_channel_1_action(state):
    move()


def bottom_left_channel_1_action(state):
    move()


def top_right_channel_1_action(state):
    move()


def bottom_right_channel_1_action(state):
    move()


def move():
    buttons = ir.buttons_pressed()  # a list
    show_buttons(buttons)

# Associate the event handlers with the functions defined above


ir.on_channel1_top_left = top_left_channel_1_action
ir.on_channel1_bottom_left = bottom_left_channel_1_action
ir.on_channel1_top_right = top_right_channel_1_action
ir.on_channel1_bottom_right = bottom_right_channel_1_action

if haveDisplay:
    root.update()

# Stop program by long-pressing touch sensor button
while not ts.is_pressed:
    ir.process()
    sleep(0.01)
    clr = cl.color_name
    show_color(clr)