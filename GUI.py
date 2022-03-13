from argparse import Action
from cProfile import run
from cgitb import text
from distutils import command
from sqlite3 import Cursor
import tkinter as tk
from tkinter import END, messagebox

import mysql.connector

# Start connection to server
cnx = mysql.connector.connect(user='root', password='UJHqn7wVr5',
                              host='127.0.0.1')

DB_name = "strom"


cursor = cnx.cursor()
cursor.execute(f"USE {DB_name}")

def viewinfo(cursor, columns):
    answer = tk.Tk()
    answer.geometry("400x250")
    for n in range(len(columns)):
        e=tk.Label(answer,width=10,text=columns[n],borderwidth=2, relief='ridge',anchor='w',bg='orange')
        e.grid(row=0,column=n)
    i = 1
    for planets in cursor: 
        for j in range(len(planets)):
            e = tk.Label(answer, width=10, text=planets[j], borderwidth=2,relief='ridge', anchor="w")  
            e.grid(row=i, column=j) 
            #e.insert(END, planets[j])
        i=i+1
    
def name():
    def run():
        planet = ent.get()
        cursor.execute(f"SELECT * FROM planets WHERE name LIKE '%{planet}%'")
        column_names = ["name", "data?", "vet ej"]
        viewinfo(cursor, column_names)
    nam = tk.Tk()
    nam.title("Lita upp din planet")
    nam.geometry("400x250")
    label = tk.Label(nam, text="Enter name of a planet: ", padx=10, pady=10)
    label.grid(row=1, column=1)
    ent = tk.Entry(nam)
    ent.grid(row=1,column=2)
    button = tk.Button(nam, text="search", command=run)
    button.grid(row=1, column=3)
    

def menu():
    men = tk.Tk()
    men.title("Menu!")
    button = tk.Button(men, text="name", command=name)
    button.pack()
    button = tk.Button(men, text="annan funktion")
    button.pack()
    men.mainloop()

menu()
