import tkinter as tk
from tkinter import END, messagebox
from xml.dom.minidom import ReadOnlySequentialNamedNodeMap
from matplotlib.pyplot import text
import mysql.connector
import sqlqueries as sql
from functions import viewinfo
# Start connection to server


def start(cursor):
    def customer(personal_code):
        try:
            cursor.execute(f"SELECT * FROM customer WHERE personal_code = '{personal_code}'")
            copy = list(cursor)
        except mysql.connector.Error:
            tk.messagebox.showerror(title="Error!", message="Not a valid personal_code")
            return
        if len(copy) == 0:
            tk.messagebox.showerror(title="Error!", message="Not a valid personal_code")
            return
        nam = tk.Tk()
        for row in copy:
            nam.title(f"{row[1]} {row[2]} ({personal_code})")

        nam.geometry("600x400")
        label = tk.Label(nam, text= "", padx=10, pady=10)
        label.grid(row=0, column=2)
        label = tk.Label(nam, text="Insert company name: ", padx=10, pady=10)
        label.grid(row=1, column=1)
        company = tk.Entry(nam)
        company.grid(row=1,column=2)
        label = tk.Label(nam, text="Insert taste: ", padx=10, pady=10)
        label.grid(row=1, column=3)
        taste = tk.Entry(nam)
        taste.grid(row=1,column=4)
        button = tk.Button(nam, text="Search", command=lambda : sql.inexpensive_chocolate(cursor, company.get(), taste.get()))
        button.grid(row=1, column=5)



    def Chocolate_personal():
        choco = tk.Tk()
        choco.title("Chocolate personal")
        choco.geometry("400x250")
        label = tk.Label(choco, text="Calculate avarage scores", padx=10, pady=10)
        label.grid(row=0, column=2)
        label = tk.Label(choco, text="Enter company name", padx=10, pady=10)
        label.grid(row=1, column=1)
        company = tk.Entry(choco)
        company.grid(row=1, column=2)
        button = tk.Button(choco, text="visa", command=lambda : sql.avrage_rate_chocklate(cursor, company.get()))
        button.grid(row=1, column=3)

    def store_personal():
        store = tk.Tk()
        store.title("Store personal")
        store.geometry("1000x500")
        label = tk.Label(store, text="Find the lowest price from all the stores", padx=10, pady=10)
        label.grid(row=1, column=1)
        button = tk.Button(store, text="visa", command=lambda : sql.expensive_chocolate(cursor))
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
        button = tk.Button(men, text="Choklad personal", command = Chocolate_personal)
        button.pack()
        button = tk.Button(men, text="butik personal", command=store_personal)
        button.pack()
        men.mainloop()
    menu()
