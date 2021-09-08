try:                        # In order to be able to import tkinter for
    import tkinter as tk    # either in python 2 or in python 3
except ImportError:
    import Tkinter as tk

import requests
from time import sleep


def event_handle(event):
    # Replace the window's title with event.type: input key
    try:
        requests.get("http://192.168.0.105/CLOSE_LED")
    except:
        pass

    root.title("{}: {}".format(str(event.type), event.keysym))
    print(f"{event.type}, {event.keysym}")

def event_commom(event):
    try:
        requests.get("http://192.168.0.105/OPEN_LED")
    except:
        pass

if __name__ == '__main__':
    root = tk.Tk()
    event_sequence = '<KeyPress>'
    root.bind(event_sequence, event_handle)
    root.bind('<KeyRelease>', event_commom)
    root.mainloop()