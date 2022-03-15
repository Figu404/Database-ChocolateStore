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
    WHERE chocolate.company LIKE "%{company}%" AND chocolate.taste LIKE "%{taste}%"
    GROUP BY chocolate.taste, chocolate.company ORDER BY AVG(likes.score) DESC"""
    cursor.execute(query)
    viewinfo(cursor,["company", "taste", "score"])


def cheapest_chocolate(cursor):
    query = """SELECT store.name, store.address, MIN(sell.price)
    FROM store JOIN sell ON store.name=sell.name
    GROUP BY store.name, store.address ORDER BY MIN(sell.price) ASC"""
    cursor.execute(query)
    viewinfo(cursor,["Name","Adress", "Lowest price"])


def stores_popular_chocolate(cursor,store):
    query = f"""SELECT chocolate.company, chocolate.taste, AVG(likes.score)
    FROM chocolate JOIN likes ON chocolate.product_number=likes.product_number
    JOIN sell ON chocolate.product_number = sell.product_number
    WHERE sell.name LIKE "%{store}%" 
    GROUP BY chocolate.company, chocolate.taste ORDER BY AVG(likes.score) DESC"""
    cursor.execute(query)
    viewinfo(cursor, ["Company", "Taste", "Avrage score"])

def cheapest_chocolate(cursor, store):
    query = f"""SELECT store.name, store.address, MIN(sell.price)
    FROM store JOIN sell ON store.name=sell.name
    WHERE store.name LIKE "{store}%"
    GROUP BY store.name, store.address ORDER BY MIN(sell.price) DESC"""
    cursor.execute(query)
    viewinfo(cursor,["Name","Adress", "Lowest price"])

def personal_scores(cursor, personal_number):
    cursor.execute(f"""SELECT company, taste, score 
                    FROM likes JOIN chocolate ON likes.product_number = chocolate.product_number 
                    WHERE likes.personal_code = "{personal_number}" ORDER BY score DESC;""")
    viewinfo(cursor, ["Comany", "Taste", "Score"])

def shoppers(cursor, store):
    query = f"""SELECT * FROM shoppers WHERE name LIKE "{store}%" """
    cursor.execute(query)
    viewinfo(cursor, ["personal_code", "city", "store", "pay"])


def inexpensive_chocolate(cursor, company, taste):
    print(company, taste)
    cursor.execute(f"""SELECT store.name, store.address, company, taste, MIN(sell.price)
    FROM store JOIN sell ON store.name=sell.name
    JOIN chocolate ON chocolate.product_number=sell.product_number
    WHERE chocolate.company LIKE "%{company}%" AND chocolate.taste LIKE "%{taste}%"
    GROUP BY store.name, store.address, company, taste ORDER BY MIN(sell.price)  ASC;""")
    viewinfo(cursor,["Store_name", "Adress", "Company_name", "Taste", "Lowest price"])


def peoples_score(cursor):
    
    query = """SELECT """
def add_scores(cursor, personal_code, product_number, score, cnx):
    cursor.execute(f"SELECT * FROM chocolate WHERE product_number = '{product_number}' ")
    copy = list(cursor)
    if len(copy) == 0:
        return (False, "Product does not exist")
    try:
        score = int(score)
    except ValueError:
        return (False, "score is not an int")
    if abs(score) <= 10:

        msgBox = messagebox.askquestion ('Add score',f'Are you sure you want to add score\nscore:{abs(score)} | for chocolate: {copy[0][2]} | from the company:{copy[0][1]}"',icon = 'warning')
        if msgBox == "yes":
            try:
                # Inserts the values:
                cursor.execute(f"INSERT INTO likes VALUES ('{personal_code}', '{product_number}', {abs(score)}) ON DUPLICATE KEY UPDATE likes.score = {abs(score)};")
            except mysql.connector.Error as err:
                return (False, f"Could not insert {err}")  # If the insert has failed.
            else:
                cnx.commit()
                return (True, f"Inserted score:{abs(score)} | for chocolate: {copy[0][2]} | from the company:{copy[0][1]}")
        else:
            return (False, "Acction canceled")
    else:
        return (False, "score is not between zero and 10")
   
    # 
    #     return schema.insert_new_data(cursor, "",))
    # 