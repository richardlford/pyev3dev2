from tkinter import *
from tkinter import ttk
import tk

parm_vals = {}

xcenter=105
ycenter=105
oval_radius=5

def mymotion(event):
    global scale_var, scale_var2, hello, world, oval, canvas
    x = event.x
    y = event.y
    scale_var.set(x-105)
    scale_var2.set(y-105)
    hello['text'] = str(x-105)
    world['text'] = str(y-105)
    canvas.coords(oval, x-oval_radius, y-oval_radius,
                        x+oval_radius, y+oval_radius)
    pass

def make_frame1(root):
    global hello, world
    frame = ttk.Frame(root)
    hello = Label(frame, text="hello", relief=RAISED, borderwidth=4, border=True)
    hello.grid(row=1, column=1)
    world = Label(frame, text="world")
    world.grid(row=2, column=3)
    Label(frame, relief=SUNKEN, borderwidth=4, bg="red").grid(row=2, column=2)
    Label(frame).grid(row=2, column=1)
    return frame


def main():
    global scale_var, scale_var2, oval, canvas
    root = Tk()
    root.title("Robot Control Panel")
    root.geometry("410x850-2000-800")
    f1 = make_frame1(root)
    f1.pack()
    scale_var = DoubleVar()
    sc = Scale(root, from_=-100.0, to=100.0, label="speed", orient=HORIZONTAL, length=400,
               relief=RAISED, sliderrelief=GROOVE, sliderlength=10, tickinterval=50.0,
               variable=scale_var)
    sc.pack()
    scale_var2 = DoubleVar()
    sc2 = Scale(root, from_=-100.0, to=100.0, label="speed2", orient=VERTICAL, length=400,
               relief=RAISED, sliderrelief=GROOVE, sliderlength=10, tickinterval=50.0,
               variable=scale_var2)
    sc2.pack()
    f2 = ttk.Frame(root)
    canvas = Canvas(f2, relief=RAISED, width=210, height=210)
    canvas.delete()
    canvas.bind("<Button1-Motion>", mymotion)
    canvas.create_rectangle(5, 5, 205, 205)
    canvas.pack()
    oval = canvas.create_oval(xcenter-oval_radius, ycenter-oval_radius,
                              xcenter+oval_radius, ycenter+oval_radius, fill='red')
    f2.pack()
    root.mainloop()

if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
