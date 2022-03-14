import tkinter as tk
from tkinter import END, messagebox
import mysql.connector
import sqlqueries as sql
from ScrollableFrame import ScrollableFrame

def viewinfo(cursor, columns):
    answer = tk.Tk()
    answer.geometry("400x250")
    scroll = ScrollableFrame(answer)
    frame = tk.Frame(scroll)
    frame.pack()
    for n in range(len(columns)):
        e=tk.Label(frame,width=10,text=columns[n],borderwidth=2, relief='ridge',anchor='w',bg='orange')
        e.grid(row=0,column=n)
    i = 1
    for planets in cursor: 
        for j in range(len(planets)):
            e = tk.Label(frame, width=10, text=planets[j], borderwidth=2,relief='ridge', anchor="w")  
            e.grid(row=i, column=j) 
            #e.insert(END, planets[j])
        i=i+1