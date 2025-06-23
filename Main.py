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

        def update_event():
            idx = listbox_events.curselection()
            if not idx:
                return
            event = events[idx[0]]
            name = entry_event_name.get()
            loc = entry_event_location.get()
            if name and loc:
                event.name = name
                event.location = loc
                event.coordinates = Person(name, '', loc).coordinates
                if event.marker:
                    event.marker.delete()
                event.marker = map_widget.set_marker(*event.coordinates, text=event.name)
                refresh_event_list()
                clear_inputs()

        def delete_event():
            idx = listbox_events.curselection()
            if not idx:
                return
            event = events.pop(idx[0])
            if event.marker:
                event.marker.delete()
            refresh_event_list()
            refresh_people_lists()
