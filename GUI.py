import tkinter as tk
from tkinter import END, messagebox
import mysql.connector

# Start connection to server

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

def start(cursor):

        
    def customer(personal_code):
        cursor.execute(f"SELECT * FROM customer WHERE personal_code = '{personal_code}'")
        copy = list(cursor)
        if len(copy) == 0:
            tk.messagebox.showerror(title="Error!", message="Not a valid personal_code")
            return
        nam = tk.Tk()
        for row in copy:
            nam.title(f"{row[1]} {row[2]} ({personal_code})")

        def chocolate_score():
            planet = ent.get()
            cursor.execute(f"SELECT * FROM planets WHERE name LIKE '%{planet}%'")
            column_names = ["name", "data?", "vet ej"]
            viewinfo(cursor, column_names)
        
        cursor.execute(f"CREATE VIEW {personal_code} AS first_name, last_name, product_number, name FROM customer RIGHT likes JOIN ON , visit")
        
        nam.geometry("400x250")
        label = tk.Label(nam, text="Skriv in personnummer: ", padx=10, pady=10)
        label.grid(row=1, column=1)
        ent = tk.Entry(nam)
        ent.grid(row=1,column=2)
        button = tk.Button(nam, text="visa", command=chocolate_score)
        button.grid(row=1, column=3)
        

    def menu():
        men = tk.Tk()
        men.title("Menu!")
        frame = tk.Frame(men)
        frame.pack()
        ent = tk.Entry(frame, text="Personnummer")
        ent.grid(row=1, column=2)
        button = tk.Button(frame, text="Kund!", command=lambda : customer(ent.get()))
        button.grid(row=1, column=3)
        label = tk.Label(frame, text="Skriv in personnummer(XXXX-XX-XX-xxxx):")
        label.grid(row=1, column=1)
        button = tk.Button(men, text="Choklad personal")
        button.pack()
        button = tk.Button(men, text="butik personal")
        button.pack()
        men.mainloop()
    menu()
