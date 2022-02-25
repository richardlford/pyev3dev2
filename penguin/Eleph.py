#!/usr/bin/env python3

# Todo:
# 1. Copy to separate file customized for Elephant
# 2. Modularize so usable in other projects
# 3. Bind return to do the evaluation
# 4. Get working on surface to see how UI works.
#    E.G. Could we use canvas like joystick?
# 5. Try out gyro
# 6. For the elephant.py, translate actions
#    to regular python.

import tkinter

from ev3dev2.auto import *

from time import sleep
import os

print("Starting")

ir = InfraredSensor()
cl = ColorSensor()
ts = TouchSensor()
# us = UltrasonicSensor()
sound = Sound()

haveDisplay = os.environ.get('DISPLAY')
if haveDisplay:
    from tkinter import *
    from tkinter import ttk

parm_vals = {}

def make_parameters_frame(root, parm_labels):
    global buttonsLabel
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    ttk.Label(frm, text="Property").grid(column=0, row=0)
    ttk.Label(frm, text="|").grid(column=1, row=0)
    ttk.Label(frm, text="Property Value").grid(column=2, row=0)
    ttk.Label(frm, text="-------------").grid(column=0, row=1)
    ttk.Label(frm, text="|").grid(column=1, row=1)
    ttk.Label(frm, text="-----------------------------").grid(column=2, row=1)
    next_row = 2
    for parm_label in parm_labels:
        ttk.Label(frm, text=parm_label).grid(column=0, row=next_row)
        ttk.Label(frm, text="|").grid(column=1, row=next_row)
        value_label = ttk.Label(frm, text="")
        value_label.grid(column=2, row=next_row)
        parm_vals[parm_label] = value_label
        next_row += 1
    return frm


def do_it_clicked():
    global entry, entry_var, result_label
    command = entry_var.get()
    print("Doing: " + command)
    result = eval(command)
    result_text = "eval(" + command + ") = " + str(result)
    print(result_text)
    result_label['text'] = result_text
    entry_var.set("")
    pass


def make_input_frame(root):
    global entry, entry_var, result_label
    entry_var = tkinter.StringVar()
    frame = ttk.Frame(root, padding=10)
    entry = ttk.Entry(frame, width=30, textvariable=entry_var)
    entry.focus()
    entry.pack()
    do_it_button = ttk.Button(frame, text="Do it", command=do_it_clicked)
    do_it_button.pack(fill='x', expand=True, pady=10)
    result_label = ttk.Label(frame, text="Will hold results")
    result_label.pack(fill='x', expand=True, pady=10)
    return frame


def make_interface_main():
    root = Tk()
    root.title("Robot Control Panel")
    root.geometry("400x400-2000-800")
    # parm_frame = make_parameters_frame(root, ["buttons", "color", "ir proximity", "ultrasonic", "touch"])
    parm_frame = make_parameters_frame(root, ["buttons", "color", "touch"])
    parm_frame.pack(fill=tkinter.X)
    inp_frame = make_input_frame(root)
    inp_frame.pack(fill=tkinter.X)

    # layout on the root window
    #root.columnconfigure(0, weight=1)
    #root.columnconfigure(1, weight=1)

    #parm_frame.grid(column=0, row=0)
    #inp_frame.grid(column=0, row=1)
    return root


if haveDisplay:
    root = make_interface_main()

trunk_motor = Motor(OUTPUT_A)
head_motor = Motor(OUTPUT_B)
leg_motor = Motor(OUTPUT_C)
rear_motor = Motor(OUTPUT_D)
motors = (trunk_motor, head_motor, leg_motor, rear_motor)

selected_motor_index = 0

actions = {}

# Button assignments
sel_plus_1 = ("top_left", 1)


def sel_add_1():
    global selected_motor_index
    selected_motor_index += 1


def sel_sub_1():
    global selected_motor_index
    selected_motor_index -= 1


actions[(sel_plus_1, True)] = sel_add_1
actions[(sel_plus_1, False)] = sel_sub_1

sel_plus_2 = ("bottom_left", 1)


def sel_add_2():
    global selected_motor_index
    selected_motor_index += 2


def sel_sub_2():
    global selected_motor_index
    selected_motor_index -= 2


actions[(sel_plus_2, True)] = sel_add_2
actions[(sel_plus_2, False)] = sel_sub_2


sel_plus_3 = ("top_left", 2)


def sel_add_3():
    global selected_motor_index
    selected_motor_index += 3


def sel_sub_3():
    global selected_motor_index
    selected_motor_index -= 3


actions[(sel_plus_3, True)] = sel_add_3
actions[(sel_plus_3, False)] = sel_sub_3


trumpet = ("bottom_left", 2)


def do_trumpet():
    sound.play_file('elephant_call.wav', play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)


actions[(trumpet, True)] = do_trumpet


def sel_motor_stop():
    motors[selected_motor_index].off()


def sel_motor_move(speed):
    if (selected_motor_index == 0) and ts.is_pressed and (speed < 0):
        # Do not go higher
        return
    motors[selected_motor_index].on(speed)


move_forward = ("top_right", 1)

actions[(move_forward, True)] = lambda: sel_motor_move(25)
actions[(move_forward, False)] = sel_motor_stop

move_backward = ("bottom_right", 1)

actions[(move_backward, True)] = lambda: sel_motor_move(-25)
actions[(move_backward, False)] = sel_motor_stop


def show_buttons(the_buttons):
    if haveDisplay:
        parm_vals['buttons']['text'] = str(the_buttons)
    else:
        print("buttons=" + str(the_buttons))

def show_color():
    color = cl.color_name
    if haveDisplay:
        parm_vals['color']['text'] = color
    else:
        print("Color="+color)


def show_ir_proximity():
    dist = str(ir.proximity)
    if haveDisplay:
        parm_vals['ir proximity']['text'] = dist
    else:
        print("ir proximity="+dist)


#def show_ultrasonic():
#    dist = str(us.distance_centimeters)
#    if haveDisplay:
#        parm_vals['ultrasonic']['text'] = dist
#    else:
#        print("ultrasonic="+dist)


def show_touch():
    dist = str(ts.is_pressed)
    if haveDisplay:
        parm_vals['touch']['text'] = dist
    else:
        print("Touch Pressed="+dist)


def process_button_change(delta):
    if delta in actions:
        actions[delta]()


def my_on_change(changed_buttons):
    state = ir._state
    print("ir.state=" + str(state))
    print("changed_buttons=" + str(changed_buttons))
    result = []
    for button, channel, dummy in changed_buttons:
        is_in = (button, channel) in state
        result.append(((button, channel), is_in))
    print("result=" + str(result))
    show_buttons(result)
    for delta in result:
        process_button_change(delta)


ir.on_change = my_on_change

if haveDisplay:
    root.update()

sw = StopWatch()

# Stop program by long-pressing touch sensor button
while True:
    ir.process()
    show_color()
    # show_ir_proximity()
    # show_ultrasonic()
    show_touch()
    if ts.is_pressed:
        if trunk_motor.speed < 0:
            trunk_motor.off()

        if sw.is_started:
            if sw.value_ms > 3000:
                sw.restart()
                do_trumpet()
        else:
            sw.start()
            do_trumpet()

    root.update()
    sleep(0.01)
