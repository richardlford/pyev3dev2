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

try:
    ir = InfraredSensor()
except:
    ir = None

try:
    cl = ColorSensor()
except:
    cl = None
try:
    ts = TouchSensor()
except:
    ts = None

try:
    us = UltrasonicSensor()
except:
    us = None

if ir:
    print("Found IR")
if cl:
    print("found color sensor")
if ts:
    print("Found touch sensor")
if us:
    print("Found untrasonic sensor")

sound = Sound()

motors = [m for m in list_motors()]
motors.sort(key=lambda m: m.address)
i = 0
for m in motors:
    print("motor["+str(i)+"]={address: "+str(m.address)+", driver: "+m.driver_name+
          ", position="+str(m.position)+", stop_action: "+str(m.stop_action))
    i += 1

motor_speeds = [50, 50, 50, 50]
#motora = Motor(OUTPUT_A)
#motorb = Motor(OUTPUT_B)
#motorc = Motor(OUTPUT_C)
#motord = Motor(OUTPUT_D)
#motors = (motora, motorb, motorc, motord)

haveDisplay = os.environ.get('DISPLAY')
if haveDisplay:
    from tkinter import *
    from tkinter import ttk

parm_vals = {}

def make_parameters_frame(root, parm_labels):
    global buttonsLabel
    frm = ttk.Frame(root, padding=10)
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

motor_data={}

def make_motor_frame(root, motor_index):
    frm = ttk.Frame(root, padding=10)
    next_row = 0
    data = {}
    ttk.Label(frm, text="-------------").grid(column=0, row=next_row)
    ttk.Label(frm, text="|").grid(column=1, row=next_row)
    ttk.Label(frm, text="-----------------------------").grid(column=2, row=next_row)
    next_row += 1
    ttk.Label(frm, text="Motor#").grid(column=0, row=next_row)
    ttk.Label(frm, text="|").grid(column=1, row=next_row)
    ttk.Label(frm, text=str(motor_index)).grid(column=2, row=next_row)
    next_row += 1
    parm_label = "address"
    ttk.Label(frm, text=parm_label).grid(column=0, row=next_row)
    ttk.Label(frm, text="|").grid(column=1, row=next_row)
    value_label = ttk.Label(frm, text="")
    value_label.grid(column=2, row=next_row)
    data[parm_label] = value_label
    next_row += 1
    parm_label = "driver"
    ttk.Label(frm, text=parm_label).grid(column=0, row=next_row)
    ttk.Label(frm, text="|").grid(column=1, row=next_row)
    value_label = ttk.Label(frm, text="")
    value_label.grid(column=2, row=next_row)
    data[parm_label] = value_label
    next_row += 1
    parm_label = "position"
    ttk.Label(frm, text=parm_label).grid(column=0, row=next_row)
    ttk.Label(frm, text="|").grid(column=1, row=next_row)
    value_label = ttk.Label(frm, text="")
    value_label.grid(column=2, row=next_row)
    data[parm_label] = value_label
    next_row += 1
    parm_label = "stop_action"
    ttk.Label(frm, text=parm_label).grid(column=0, row=next_row)
    ttk.Label(frm, text="|").grid(column=1, row=next_row)
    value_label = ttk.Label(frm, text="")
    value_label.grid(column=2, row=next_row)
    data[parm_label] = value_label
    next_row += 1
    parm_label = "speed"
    ttk.Label(frm, text=parm_label).grid(column=0, row=next_row)
    ttk.Label(frm, text="|").grid(column=1, row=next_row)
    value_label = ttk.Label(frm, text="")
    value_label.grid(column=2, row=next_row)
    data[parm_label] = value_label
    next_row += 1
    parm_label = "is_running"
    ttk.Label(frm, text=parm_label).grid(column=0, row=next_row)
    ttk.Label(frm, text="|").grid(column=1, row=next_row)
    value_label = ttk.Label(frm, text="")
    value_label.grid(column=2, row=next_row)
    data[parm_label] = value_label
    next_row += 1
    parm_label = "is_ramping"
    ttk.Label(frm, text=parm_label).grid(column=0, row=next_row)
    ttk.Label(frm, text="|").grid(column=1, row=next_row)
    value_label = ttk.Label(frm, text="")
    value_label.grid(column=2, row=next_row)
    data[parm_label] = value_label
    next_row += 1
    parm_label = "is_holding"
    ttk.Label(frm, text=parm_label).grid(column=0, row=next_row)
    ttk.Label(frm, text="|").grid(column=1, row=next_row)
    value_label = ttk.Label(frm, text="")
    value_label.grid(column=2, row=next_row)
    data[parm_label] = value_label
    next_row += 1
    parm_label = "is_overloaded"
    ttk.Label(frm, text=parm_label).grid(column=0, row=next_row)
    ttk.Label(frm, text="|").grid(column=1, row=next_row)
    value_label = ttk.Label(frm, text="")
    value_label.grid(column=2, row=next_row)
    data[parm_label] = value_label
    next_row += 1
    parm_label = "is_stalled"
    ttk.Label(frm, text=parm_label).grid(column=0, row=next_row)
    ttk.Label(frm, text="|").grid(column=1, row=next_row)
    value_label = ttk.Label(frm, text="")
    value_label.grid(column=2, row=next_row)
    data[parm_label] = value_label
    next_row += 1
    motor_data[motor_index] = data
    return frm

def make_motors_frames(root):
    for i in range(len(motors)):
        frm = make_motor_frame(root, i)
        frm.pack(fill=tkinter.X)

def make_interface_main():
    root = Tk()
    root.title("Robot Control Panel")
    root.geometry("400x400-2000-800")
    captions = ["buttons"]
    if cl:
        captions.append("color")
    if ir:
        captions.append("ir proximity")
    if us:
        captions.append("ultrasonic")
    if ts:
        captions.append("touch")
    parm_frame = make_parameters_frame(root, captions)
    parm_frame.pack(fill=tkinter.X)
    inp_frame = make_input_frame(root)
    inp_frame.pack(fill=tkinter.X)
    make_motors_frames(root)
    return root

if haveDisplay:
    root = make_interface_main()


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
    sound.play_file('elephant_call.wav')


actions[(trumpet, True)] = do_trumpet


def sel_motor_stop():
    motors[selected_motor_index].off()


def sel_motor_move(speed):
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


def show_ultrasonic():
    dist = str(us.distance_centimeters)
    if haveDisplay:
        parm_vals['ultrasonic']['text'] = dist
    else:
        print("ultrasonic="+dist)


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
sound.play_file("../sounds/animals/snake_hiss.wav")
def show_motor(motor_index):
    m = motors[motor_index]
    data = motor_data[motor_index]
    data["address"]["text"] = m.address
    data["driver"]["text"] = m.driver_name
    data["position"]["text"] = str(m.position)
    data["stop_action"]["text"] = m.stop_action
    data["speed"]["text"] = str(m.speed)
    data["is_running"]["text"] = str(m.is_running)
    data["is_ramping"]["text"] = str(m.is_ramping)
    data["is_holding"]["text"] = str(m.is_holding)
    data["is_overloaded"]["text"] = str(m.is_overloaded)
    data["is_stalled"]["text"] = str(m.is_stalled)
    pass

def show_motors():
    for i in range(len(motors)):
        show_motor(i)
    pass

ir.on_change = my_on_change

if haveDisplay:
    root.update()

# Stop program by long-pressing touch sensor button
while True:
    ir.process()
    if cl:
        show_color()
    if ir:
        show_ir_proximity()
    if us:
        show_ultrasonic()
    if ts:
        show_touch()
    show_motors()
    root.update()
    sleep(0.01)
