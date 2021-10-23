try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

import requests
from time import sleep

link = "http://192.168.0.103"

def event_handle(event):
    # Replace the window's title with event.type: input key
    if event.keysym == 'w':
        motor = "front_AB"
    elif event.keysym == "s":
        motor = "back_AB"
    elif event.keysym == "a":
        motor = "front_A"
    elif event.keysym == "d":
        motor = "front_B"


    try:
        requests.get(f"{link}/{motor}")
    except:
        pass

    root.title("{}: {}".format(str(event.type), event.keysym))
    print(f"{event.type}, {event.keysym}")

def event_commom(event):
    try:
        requests.get(f"{link}/CLOSE")
        requests.get(f"{link}/CLOSE")
    except:
        pass

if __name__ == '__main__':
    root = tk.Tk()
    event_sequence = '<KeyPress>'
    root.bind(event_sequence, event_handle)
    root.bind('<KeyRelease>', event_commom)
    root.mainloop()