from tkinter import *
from tkintermapview import TkinterMapView
import requests
from bs4 import BeautifulSoup


root = Tk()
root.title("Event Manager")
root.geometry("1200x800")

frame_left = Frame(root)
frame_left.pack(side=LEFT, padx=10)

frame_right = Frame(root)
frame_right.pack(side=RIGHT, padx=10)

frame_map = Frame(root)
frame_map.pack()

def add_event():
    name = entry_event_name.get()
    loc = entry_event_location.get()
    if name and loc:
        event = Event(name, loc)
        event.marker = map_widget.set_marker(*event.coordinates, text=name)
        events.append(event)
        refresh_event_list()
        clear_inputs()

def refresh_event_list():
    listbox_events.delete(0, END)
    for event in events:
        listbox_events.insert(END, f"{event.name} ({event.location})")
