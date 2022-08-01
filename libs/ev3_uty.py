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
import os

from ev3dev2.auto import *
from time import sleep
from tkinter import *
from tkinter import ttk
import typing

haveDisplay = os.environ.get('DISPLAY')


class Ev3Uty:

    __slots__ = [
        'entry_var',
        'root',
        'debug',
        'infrared',
        'color_sensor',
        'ts'
    ]


    def __init__(self, root, debug=False):
        """
        Constructs the Ev3 utility class.
        root is the tkinter root.
        """
        self.entry_var = None
        self.root = root
        self.debug = debug

        try:
            self.infrared = InfraredSensor()
        except:
            self.infrared = None

        try:
            self.color_sensor = ColorSensor()
        except:
            self.color_sensor = None
        try:
            self.ts = TouchSensor()
        except:
            self.ts = None

        try:
            self.us = UltrasonicSensor()
        except:
            self.us = None

        self.sound = Sound()

        if self.infrared:
            self.maybe_print("Found IR")
        if self.color_sensor:
            self.maybe_print("found color sensor")
        if self.ts:
            self.maybe_print("Found touch sensor")
        if self.us:
            self.maybe_print("Found untrasonic sensor")

        self.sound = Sound()

        self.motors = [m for m in list_motors()]
        self.motors.sort(key=lambda m: m.address)
        i = 0
        for m in self.motors:
            self.maybe_print("motor[" + str(i) + "]={address: " + str(m.address) + ", driver: " + m.driver_name +
                             ", position=" + str(m.position) + ", stop_action: " + str(m.stop_action))
            i += 1

        self.motor_speeds = [50, 50, 50, 50]

        self.parm_vals = {}
        self.motor_data = {}

    def maybe_print(self, what):
        if self.debug:
            print(what)

    def make_parameters_frame(self, root, parm_labels):
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
            self.parm_vals[parm_label] = value_label
            next_row += 1
        return frm

    def do_it_clicked(self):
        command = self.entry_var.get()
        self.maybe_print("Doing: " + command)
        result = eval(command)
        result_text = "eval(" + command + ") = " + str(result)
        self.maybe_print(result_text)
        self.result_label['text'] = result_text
        self.entry_var.set("")
        pass

    def make_input_frame(self, root):
        self.entry_var = StringVar()
        frame = ttk.Frame(root, padding=10)
        self.entry = ttk.Entry(frame, width=30, textvariable=self.entry_var)
        self.entry.focus()
        self.entry.pack()
        do_it_button = ttk.Button(frame, text="Do it", command=self.do_it_clicked)
        do_it_button.pack(fill='x', expand=True, pady=10)
        self.result_label = ttk.Label(frame, text="Will hold results")
        self.result_label.pack(fill='x', expand=True, pady=10)
        return frame

    def make_motor_frame(self, root, motor_index):
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
        self.motor_data[motor_index] = data
        return frm

    def make_motors_frames(self, root):
        for i in range(len(self.motors)):
            frm = self.make_motor_frame(root, i)
            frm.pack(fill=X)

    def make_interface_main(self):
        self.root.title("Robot Control Panel")
        self.root.geometry("400x400-2000-800")
        captions = ["buttons"]
        if self.color_sensor:
            captions.append("color")
        if self.infrared:
            captions.append("ir proximity")
        if self.us:
            captions.append("ultrasonic")
        if self.ts:
            captions.append("touch")
        parm_frame = self.make_parameters_frame(self.root, captions)
        parm_frame.pack(fill=X)
        inp_frame = self.make_input_frame(self.root)
        inp_frame.pack(fill=X)
        self.make_motors_frames(self.root)
        return self.root

    if haveDisplay:
        root = make_interface_main()

    selected_motor_index = 0

    actions = {}

    # Button assignments
    sel_plus_1 = ("top_left", 1)

    def sel_add_1(self):
        global selected_motor_index
        selected_motor_index += 1

    def sel_sub_1(self):
        global selected_motor_index
        selected_motor_index -= 1

    actions[(sel_plus_1, True)] = sel_add_1
    actions[(sel_plus_1, False)] = sel_sub_1

    sel_plus_2 = ("bottom_left", 1)

    def sel_add_2(self):
        global selected_motor_index
        selected_motor_index += 2

    def sel_sub_2(self):
        global selected_motor_index
        selected_motor_index -= 2

    actions[(sel_plus_2, True)] = sel_add_2
    actions[(sel_plus_2, False)] = sel_sub_2

    sel_plus_3 = ("top_left", 2)

    def sel_add_3(self):
        global selected_motor_index
        selected_motor_index += 3

    def sel_sub_3(self):
        global selected_motor_index
        selected_motor_index -= 3

    actions[(sel_plus_3, True)] = sel_add_3
    actions[(sel_plus_3, False)] = sel_sub_3

    trumpet = ("bottom_left", 2)

    def do_trumpet(self):
        self.sound.play_file('elephant_call.wav')

    actions[(trumpet, True)] = do_trumpet

    def sel_motor_stop(self):
        self.motors[selected_motor_index].off()

    def sel_motor_move(self, speed):
        self.motors[selected_motor_index].on(speed)

    move_forward = ("top_right", 1)

    actions[(move_forward, True)] = lambda: self.sel_motor_move(25)
    actions[(move_forward, False)] = sel_motor_stop

    move_backward = ("bottom_right", 1)

    actions[(move_backward, True)] = lambda: sel_motor_move(-25)
    actions[(move_backward, False)] = sel_motor_stop

    def show_buttons(self, the_buttons):
        if haveDisplay:
            self.parm_vals['buttons']['text'] = str(the_buttons)
        else:
            self.maybe_print("buttons=" + str(the_buttons))

    def show_color(self):
        color = cl.color_name
        if haveDisplay:
            self.parm_vals['color']['text'] = color
        else:
            self.maybe_print("Color=" + color)

    def show_ir_proximity(self):
        dist = str(ir.proximity)
        if haveDisplay:
            self.parm_vals['ir proximity']['text'] = dist
        else:
            self.maybe_print("ir proximity=" + dist)

    def show_ultrasonic(self):
        dist = str(us.distance_centimeters)
        if haveDisplay:
            self.parm_vals['ultrasonic']['text'] = dist
        else:
            self.maybe_print("ultrasonic=" + dist)

    def show_touch(self):
        dist = str(ts.is_pressed)
        if haveDisplay:
            self.parm_vals['touch']['text'] = dist
        else:
            self.maybe_print("Touch Pressed=" + dist)

    def process_button_change(self, delta):
        if delta in actions:
            actions[delta]()

    def my_on_change(self, changed_buttons):
        state = ir._state
        self.maybe_print("ir.state=" + str(state))
        self.maybe_print("changed_buttons=" + str(changed_buttons))
        result = []
        for button, channel, dummy in changed_buttons:
            is_in = (button, channel) in state
            result.append(((button, channel), is_in))
        self.maybe_print("result=" + str(result))
        show_buttons(result)
        for delta in result:
            process_button_change(delta)

    sound.play_file("../sounds/animals/snake_hiss.wav")

    def show_motor(self, motor_index):
        m = motors[motor_index]
        data = self.motor_data[motor_index]
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

    def show_motors(self):
        for i in range(len(motors)):
            show_motor(i)
        pass

    ir.on_change = my_on_change

    def main(self):
        if haveDisplay:
            self.root.update()

        while True:
            if self.infrared:
                self.infrared.process()
            if self.color_sensor:
                self.show_color()
            if self.infrared:
                self.show_ir_proximity()
            if self.us:
                self.show_ultrasonic()
            if self.ts:
                self.show_touch()
            self.show_motors()
            if haveDisplay:
                self.root.update()
            sleep(0.01)

class Client:

    def __init__(self, root, uty: Ev3Uty, debug=False):
        self.root = root
        self.uty = uty
        self.debug = debug
        pass

    def main(self):
        pass

if __name__ == '__main__':
    the_root = Tk()
    the_uty = Ev3Uty(the_root, True)
    client = Client(the_root, the_uty, True)
    client.main()
