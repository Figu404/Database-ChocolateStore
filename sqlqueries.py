from ast import Store
from pickle import TRUE
import re
from sqlalchemy import false
from tkinter import messagebox
from sympy import ComputationFailed
from functions import viewinfo
import mysql.connector


def avrage_rate_chocklate(cursor, company, taste):
    query = f"""SELECT chocolate.company, chocolate.taste, AVG(likes.score)
    FROM chocolate JOIN likes ON chocolate.product_number=likes.product_number
    WHERE chocolate.company LIKE %s AND chocolate.taste LIKE %s
    GROUP BY chocolate.taste, chocolate.company ORDER BY AVG(likes.score) DESC"""
    cursor.execute(query, (company + "%", taste + "%"))
    viewinfo(cursor,["company", "taste", "score"])


def stores_popular_chocolate(cursor,store):
    query = f"""SELECT chocolate.company, chocolate.taste, AVG(likes.score)
    FROM chocolate JOIN likes ON chocolate.product_number=likes.product_number
    JOIN sell ON chocolate.product_number = sell.product_number
    WHERE sell.name LIKE %s 
    GROUP BY chocolate.company, chocolate.taste ORDER BY AVG(likes.score) DESC"""
    cursor.execute(query, (store + "%",))
    viewinfo(cursor, ["Company", "Taste", "Avrage score"])


def cheapest_chocolate(cursor, store):
    query = f"""SELECT store.name, store.address, MIN(sell.price)
    FROM store JOIN sell ON store.name=sell.name
    WHERE store.name LIKE %s
    GROUP BY store.name, store.address ORDER BY MIN(sell.price) ASC"""
    cursor.execute(query, (store + "%",))
    viewinfo(cursor,["Name","Adress", "Lowest price"])


def personal_scores(cursor, personal_number):
    cursor.execute(f"""SELECT company, taste, score 
                    FROM likes JOIN chocolate ON likes.product_number = chocolate.product_number 
                    WHERE likes.personal_code = %s ORDER BY score DESC;""", (personal_number,))
    viewinfo(cursor, ["Comany", "Taste", "Score"])


def shoppers(cursor, store):
    query = f"""SELECT * FROM shoppers WHERE name LIKE %s """
    cursor.execute(query,(store + "%",))
    viewinfo(cursor, ["personal_code", "city", "store", "pay"])


def inexpensive_chocolate(cursor, company, taste):
    cursor.execute(f"""SELECT store.name, store.address, company, taste, MIN(sell.price)
    FROM store JOIN sell ON store.name=sell.name
    JOIN chocolate ON chocolate.product_number=sell.product_number
    WHERE chocolate.company LIKE %s AND chocolate.taste LIKE %s
    GROUP BY store.name, store.address, company, taste ORDER BY MIN(sell.price)  ASC;""", (company + "%", taste + "%"))
    viewinfo(cursor,["Store_name", "Adress", "Company_name", "Taste", "Lowest price"])

def find_productnumber(cursor,company,taste):
    cursor.execute(f"""SELECT product_number, company, taste
    FROM chocolate
    WHERE chocolate.company LIKE %s AND chocolate.taste LIKE %s;""", (company + "%", taste + "%"))
    viewinfo(cursor,["Product_number", "Company_name", "Taste"])

def get_visits(cursor, personal_code):
    cursor.execute("SELECT name, date, time, pay FROM visit WHERE visit.personal_code = %s ;", (personal_code,))
    viewinfo(cursor, ("Store name", "Date", "Time", "Payed"))

def add_scores(cursor, personal_code, product_number, score, cnx):
    cursor.execute("SELECT * FROM chocolate WHERE product_number = %s ", (product_number,))
    copy = list(cursor)
    if len(copy) == 0:
        return (False, "Product does not exist")
    try:
        score = int(score)
    except ValueError:
        return (False, "score is not an int")
    if score <= 10 and 0 <= score:

        msgBox = messagebox.askquestion ('Add score',f'Are you sure you want to add score\nscore:{score} | for chocolate: {copy[0][2]} | from the company:{copy[0][1]}"',icon = 'warning')
        if msgBox == "yes":
            try:
                # Inserts the values:
                cursor.execute(f"INSERT INTO likes VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE likes.score = %s;", (personal_code, product_number, score, score))
            except mysql.connector.Error as err:
                return (False, f"Could not insert {err}")  # If the insert has failed.
            else:
                cnx.commit()
                return (True, f"Inserted score:{score} | for chocolate: {copy[0][2]} | from the company:{copy[0][1]}")
        else:
            return (False, "Acction canceled")
    else:
        return (False, "score is not between zero and 10")
   
    # 
    #     return schema.insert_new_data(cursor, "",))
    # 