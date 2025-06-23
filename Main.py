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

            def add_person(role):
                idx = listbox_events.curselection()
                if not idx:
                    return
                event = events[idx[0]]
                name = entry_person_name.get()
                surname = entry_person_surname.get()
                loc = entry_person_location.get()
                if name and surname and loc:
                    person = Person(name, surname, loc)
                    (event.klienci if role == 'klient' else event.pracownicy).append(person)
                    clear_inputs()
                    refresh_people_lists()

                    def refresh_people_lists():
                        listbox_clients.delete(0, END)
                        listbox_workers.delete(0, END)
                        idx = listbox_events.curselection()
                        if not idx:
                            return
                        event = events[idx[0]]
                        for k in event.klienci:
                            listbox_clients.insert(END, f"{k.name} {k.surname} ({k.location})")
                        for p in event.pracownicy:
                            listbox_workers.insert(END, f"{p.name} {p.surname} ({p.location})")

def show_people(role):
    idx = listbox_events.curselection()
    if not idx:
        return
    event = events[idx[0]]
    map_widget.delete_all_marker()
    people = event.klienci if role == 'klient' else event.pracownicy
    for person in people:
        person.marker = map_widget.set_marker(*person.coordinates, text=f"{person.name} {person.surname}")
    refresh_people_lists()