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
