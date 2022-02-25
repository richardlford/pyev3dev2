#!/usr/bin/env python3
from tkinter import *
from tkinter import ttk
root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()
label = ttk.Label(frm, text="Hello World!")
label.grid(column=0, row=0)
modbutton = ttk.Button(frm, text="Modify")
modbutton.grid(column=1, row=0)

def modit (arg):
    label["text"] = "Good Bye"

modbutton['command'] = lambda: modit(5)
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=2, row=0)
root.mainloop()

