from tkinter import *
from tkintermapview import TkinterMapView
import requests
from bs4 import BeautifulSoup


class Person:
    def __init__(self, name, surname, location):
        self.name = name
        self.surname = surname
        self.location = location
        self.coordinates = self.get_coordinates()
        self.marker = None

    def get_coordinates(self):
        try:
            url = f"https://pl.wikipedia.org/wiki/{self.location}"
            html = requests.get(url).text
            soup = BeautifulSoup(html, 'html.parser')
            lon = float(soup.select('.longitude')[1].text.replace(',', '.'))
            lat = float(soup.select('.latitude')[1].text.replace(',', '.'))
            return lat, lon
        except:
            return 52.23, 21.01


class Event:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.coordinates = Person(name, '', location).coordinates
        self.klienci = []
        self.pracownicy = []
        self.marker = None


events = []
selected_client_index = None
selected_worker_index = None


def refresh_event_list():
    listbox_events.delete(0, END)
    for event in events:
        listbox_events.insert(END, f"{event.name} ({event.location})")


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


def clear_inputs():
    for entry in [entry_event_name, entry_event_location, entry_person_name, entry_person_surname, entry_person_location]:
        entry.delete(0, END)


def add_event():
    name = entry_event_name.get()
    loc = entry_event_location.get()
    if name and loc:
        event = Event(name, loc)
        event.marker = map_widget.set_marker(*event.coordinates, text=name)
        events.append(event)
        refresh_event_list()
        clear_inputs()


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
        event.coordinates = event.coordinates = Person(name, '', loc).coordinates
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


def show_all_events():
    map_widget.delete_all_marker()
    for event in events:
        event.marker = map_widget.set_marker(*event.coordinates, text=event.name)


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


def on_client_select(evt):
    global selected_client_index
    idx = listbox_clients.curselection()
    if not idx:
        return
    selected_client_index = idx[0]
    event_idx = listbox_events.curselection()
    if not event_idx:
        return
    person = events[event_idx[0]].klienci[selected_client_index]
    entry_person_name.delete(0, END)
    entry_person_name.insert(0, person.name)
    entry_person_surname.delete(0, END)
    entry_person_surname.insert(0, person.surname)
    entry_person_location.delete(0, END)
    entry_person_location.insert(0, person.location)


def on_worker_select(evt):
    global selected_worker_index
    idx = listbox_workers.curselection()
    if not idx:
        return
    selected_worker_index = idx[0]
    event_idx = listbox_events.curselection()
    if not event_idx:
        return
    person = events[event_idx[0]].pracownicy[selected_worker_index]
    entry_person_name.delete(0, END)
    entry_person_name.insert(0, person.name)
    entry_person_surname.delete(0, END)
    entry_person_surname.insert(0, person.surname)
    entry_person_location.delete(0, END)
    entry_person_location.insert(0, person.location)


def edit_selected_person(role):
    global selected_client_index, selected_worker_index
    idx = listbox_events.curselection()
    if not idx:
        return
    event = events[idx[0]]
    if role == 'klient' and selected_client_index is not None:
        person = event.klienci[selected_client_index]
    elif role == 'pracownik' and selected_worker_index is not None:
        person = event.pracownicy[selected_worker_index]
    else:
        return
    person.name = entry_person_name.get()
    person.surname = entry_person_surname.get()
    person.location = entry_person_location.get()
    person.coordinates = person.get_coordinates()
    if person.marker:
        person.marker.delete()
    person.marker = map_widget.set_marker(*person.coordinates, text=f"{person.name} {person.surname}")
    clear_inputs()
    refresh_people_lists()


def delete_selected_person(role):
    global selected_client_index, selected_worker_index
    idx = listbox_events.curselection()
    if not idx:
        return
    event = events[idx[0]]
    if role == 'klient' and selected_client_index is not None:
        person = event.klienci.pop(selected_client_index)
        selected_client_index = None
    elif role == 'pracownik' and selected_worker_index is not None:
        person = event.pracownicy.pop(selected_worker_index)
        selected_worker_index = None
    else:
        return
    if person.marker:
        person.marker.delete()
    clear_inputs()
    refresh_people_lists()


root = Tk()
root.title("Event Manager")
root.geometry("1200x800")

frame_left = Frame(root)
frame_left.pack(side=LEFT, padx=10)

Label(frame_left, text="Event").pack()
entry_event_name = Entry(frame_left)
entry_event_name.pack()
entry_event_location = Entry(frame_left)
entry_event_location.pack()
Button(frame_left, text="Dodaj", command=add_event).pack()
Button(frame_left, text="Edytuj", command=update_event).pack()
Button(frame_left, text="Usuń", command=delete_event).pack()
listbox_events = Listbox(frame_left, height=10)
listbox_events.pack()
Button(frame_left, text="Pokaż wszystkie eventy", command=show_all_events).pack()
Button(frame_left, text="Pokaż klientów", command=lambda: show_people('klient')).pack()
Button(frame_left, text="Pokaż pracowników", command=lambda: show_people('pracownik')).pack()

frame_right = Frame(root)
frame_right.pack(side=RIGHT, padx=10)
Label(frame_right, text="Osoba").pack()
entry_person_name = Entry(frame_right)
entry_person_name.pack()
entry_person_surname = Entry(frame_right)
entry_person_surname.pack()
entry_person_location = Entry(frame_right)
entry_person_location.pack()
Button(frame_right, text="Dodaj klienta", command=lambda: add_person('klient')).pack()
Button(frame_right, text="Edytuj klienta", command=lambda: edit_selected_person('klient')).pack()
Button(frame_right, text="Usuń klienta", command=lambda: delete_selected_person('klient')).pack()
Button(frame_right, text="Dodaj pracownika", command=lambda: add_person('pracownik')).pack()
Button(frame_right, text="Edytuj pracownika", command=lambda: edit_selected_person('pracownik')).pack()
Button(frame_right, text="Usuń pracownika", command=lambda: delete_selected_person('pracownik')).pack()

Label(frame_right, text="Klienci").pack()
listbox_clients = Listbox(frame_right, height=6)
listbox_clients.pack()
listbox_clients.bind("<<ListboxSelect>>", on_client_select)

Label(frame_right, text="Pracownicy").pack()
listbox_workers = Listbox(frame_right, height=6)
listbox_workers.pack()
listbox_workers.bind("<<ListboxSelect>>", on_worker_select)

frame_map = Frame(root)
frame_map.pack()
map_widget = TkinterMapView(frame_map, width=1000, height=700)
map_widget.pack()
map_widget.set_position(52.23, 21.01)
map_widget.set_zoom(6)

root.mainloop()