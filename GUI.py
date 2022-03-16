import tkinter as tk
from tkinter import messagebox
import mysql.connector
import sqlqueries as sql


# Runs the GUI
def start(cursor, cnx):
    # A window for the customers
    def customer(personal_code):
        # A try statment to see if a customer exists or not
        try:
            # Try to find customer
            cursor.execute("SELECT * FROM customer WHERE personal_code = %s",
                           (personal_code,))
            copy = list(cursor)
        except mysql.connector.Error:
            # If the sql commands failes
            tk.messagebox.showerror(title="Error!", message="""Not a valid
                                                personal_code""")
            return
        # If customer do not exist
        if len(copy) == 0:
            tk.messagebox.showerror(title="Error!", message="""Not a valid
                                    personal_code""")
            return
        # Create a window
        nam = tk.Tk()
        # Set the title of the window to the name and personal
        # code of the customer
        for row in copy:
            nam.title(f"{row[1]} {row[2]} ({personal_code})")
        # Force the window to open in this size
        nam.geometry("800x400")
        # Creating the interface
        label = tk.Label(nam, text="Find the cheapest chocolate:", padx=10,
                         pady=10, font=('Helvetica', 12, 'bold'))
        label.grid(row=0, column=2)
        label = tk.Label(nam, text="Insert company name: ", padx=10, pady=10)
        label.grid(row=1, column=1)
        company = tk.Entry(nam)
        company.grid(row=1, column=2)
        label = tk.Label(nam, text="Insert taste: ", padx=10, pady=10)
        label.grid(row=1, column=3)
        taste = tk.Entry(nam)
        taste.grid(row=1, column=4)
        button = tk.Button(nam, text="Search", command=lambda:
                           sql.inexpensive_chocolate(cursor, company.get(),
                                                     taste.get()))
        button.grid(row=1, column=5)

        label = tk.Label(nam, text="Find all your ratings and visits:",
                         padx=10, pady=10, font=('Helvetica', 12, 'bold'))
        label.grid(row=2, column=2)
        frame = tk.Frame(nam)
        frame.grid(row=3, column=2)
        button = tk.Button(frame, text="Ratings", command=lambda:
                           sql.personal_scores(cursor, personal_code))
        button.grid(row=0, column=1, padx=10)
        button = tk.Button(frame, text="Visits", command=lambda:
                           sql.get_visits(cursor, personal_code))
        button.grid(row=0, column=2, padx=10)

        # A function to call when the button to add a score is pushed
        def add_score():
            val = sql.add_scores(cursor, personal_code, product_number.get(),
                                 score.get(), cnx)
            if val[0]:
                tk.messagebox.showinfo(title="Added score", message=val[1])
            else:
                tk.messagebox.showerror(title="Error!", message=val[1])

        label = tk.Label(nam, text="Add a new score:", padx=10,
                         pady=10, font=('Helvetica', 12, 'bold'))
        label.grid(row=4, column=2)
        label = tk.Label(nam, text="*Insert product number: ",
                         padx=10, pady=10)
        label.grid(row=5, column=1)
        product_number = tk.Entry(nam)
        product_number.grid(row=5, column=2)
        label = tk.Label(nam, text="*Insert score: ", padx=10, pady=10)
        label.grid(row=5, column=3)
        score = tk.Entry(nam)
        score.grid(row=5, column=4)
        button = tk.Button(nam, text="Enter", command=add_score)
        button.grid(row=5, column=5)

        label = tk.Label(nam, text="""Find the the product
                         number of a chocolate:""", padx=10, pady=10,
                         font=('Helvetica', 12, 'bold'))
        label.grid(row=6, column=2)
        label = tk.Label(nam, text="Insert company name: ", padx=10, pady=10)
        label.grid(row=7, column=1)
        company2 = tk.Entry(nam)
        company2.grid(row=7, column=2)
        label = tk.Label(nam, text="Insert taste: ", padx=10, pady=10)
        label.grid(row=7, column=3)
        taste2 = tk.Entry(nam)
        taste2.grid(row=7, column=4)
        button = tk.Button(nam, text="Search", command=lambda:
                           sql.find_productnumber(cursor, company2.get(),
                                                  taste2.get()))
        button.grid(row=7, column=5)

    # Create the window for the chocolate staff
    def Chocolate_personal():
        choco = tk.Tk()
        choco.title("Chocolate personal")
        choco.geometry("1000x500")
        label = tk.Label(choco, text="Calculate avarage scores", padx=10,
                         pady=10, font=('Helvetica', 12, 'bold'))
        label.grid(row=0, column=2)
        label = tk.Label(choco, text="Enter company name:", padx=10, pady=10)
        label.grid(row=1, column=1)
        company = tk.Entry(choco)
        company.grid(row=1, column=2)
        label = tk.Label(choco, text="Enter taste name", padx=10, pady=10)
        label.grid(row=1, column=3)
        taste = tk.Entry(choco)
        taste.grid(row=1, column=4)
        button = tk.Button(choco, text="Search", command=lambda:
                           sql.avrage_rate_chocklate(cursor, company.get(),
                                                     taste.get()))
        button.grid(row=1, column=5)

    # Create the window for the store staff
    def store_personal():
        store = tk.Tk()
        store.title("Store personal")
        store.geometry("1000x500")
        stor = tk.Entry(store)
        stor.grid(row=0, column=2)
        label = tk.Label(store, text="Enter store name:", padx=10, pady=10,
                         font=('Helvetica', 12, 'bold'))
        label.grid(row=0, column=1)
        label = tk.Label(store, text="Find stores most popular chocolate:",
                         padx=10, pady=10)
        label.grid(row=3, column=1)
        button = tk.Button(store, text="Search", command=lambda:
                           sql.stores_popular_chocolate(cursor, stor.get()))
        button.grid(row=3, column=2)
        label = tk.Label(store, text="Find the lowest price from stores:",
                         padx=10, pady=10)
        label.grid(row=1, column=1)
        button = tk.Button(store, text="Search", command=lambda:
                           sql.cheapest_chocolate(cursor, stor.get()))
        button.grid(row=1, column=2)
        label = tk.Label(store, text="""Finds shoppers from stores and there
        most expensive vitits:""", padx=10, pady=10)
        label.grid(row=2, column=1)
        button = tk.Button(store, text="Search", command=lambda:
                           sql.shoppers(cursor, stor.get()))
        button.grid(row=2, column=2)

    # Create the window for the menu
    def menu():
        men = tk.Tk()
        men.title("Menu!")
        frame = tk.Frame(men)
        frame.pack()
        ent = tk.Entry(frame, text="Personal code")
        ent.grid(row=1, column=2)
        button = tk.Button(frame, text="Customer", command=lambda:
                           customer(ent.get()))
        button.grid(row=1, column=3)
        label = tk.Label(frame, text="""*Write your personal
                         code(YYYY-MM-DD-XXXX):""")
        label.grid(row=1, column=1)
        button = tk.Button(men, text="Chocolate staff",
                           command=Chocolate_personal)
        button.pack()
        button = tk.Button(men, text="Store staff", command=store_personal)
        button.pack()
        men.mainloop()
    menu()
