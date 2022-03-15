from textwrap import fill
import tkinter as tk
from tkinter import END, messagebox, RIGHT, Y, NO, CENTER
import mysql.connector
from sqlalchemy import column
import sqlqueries as sql
from ScrollableFrame import ScrollableFrame


def viewinfo(cursor, columns):
    view = tk.Tk()
    view.title('PythonGuides')
    view.geometry('1000x500')
    view['bg'] = '#AC99F2'
    game_frame = tk.Frame(view)
    game_frame.pack()
    game_scroll = tk.Scrollbar(game_frame)
    game_scroll.pack(side=RIGHT, fill=Y)
    my_game = tk.ttk.Treeview(game_frame,yscrollcommand=game_scroll.set)
    my_game.pack()
    game_scroll.config(command=my_game.yview)
    my_game['columns'] = columns
    my_game.column("#0", width=0,  stretch=NO)
    i = 0
    for j in columns:
        my_game.heading(j,text=j,anchor=CENTER)
    
    for e in cursor:
        my_game.insert(parent='',index='end',iid=i,text='', values=e)
        i+=1
    my_game.pack()
    # answer = tk.Tk()
    # answer.geometry("400x250")
    # frame = tk.Frame(answer)
    # frame.pack()
    # for n in range(len(columns)):
    #     e=tk.Label(frame,width=10,text=columns[n],borderwidth=2, relief='ridge',anchor='w',bg='orange')
    #     e.grid(row=0,column=n)
    # i = 1
    # for planets in cursor: 
    #     for j in range(len(planets)):
    #         e = tk.Label(frame, width=10, text=planets[j], borderwidth=2,relief='ridge', anchor="w")  
    #         e.grid(row=i, column=j) 
    #         #e.insert(END, planets[j])
    #     i=i+1