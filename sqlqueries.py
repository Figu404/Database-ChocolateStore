from ast import Store

from sympy import ComputationFailed
from functions import viewinfo
import mysql.connector

def avrage_rate_chocklate(cursor, company):
    query = f"""SELECT chocolate.company, chocolate.taste, AVG(likes.score)
    FROM chocolate JOIN likes ON chocolate.product_number=likes.product_number
    WHERE chocolate.company LIKE "%{company}%"
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


def shoppers(cursor):
    query = """SELECT * FROM shoppers"""
    cursor.execute(query)
    viewinfo(cursor, ["personal_code", "city", "pay"])
    

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
