from ast import Store
from functions import viewinfo
import mysql.connector

def avrage_rate_chocklate(cursor):
    query = """SELECT chocolate.company, chocolate.taste, AVG(likes.score)
    FROM chocolate JOIN likes ON chocolate.product_number=likes.product_number
    GROUP BY chocolate.taste, chocolate.company ORDER BY AVG(likes.score) DESC"""
    cursor.execute(query)
    viewinfo(cursor,["company", "taste", "score"])


def expensive_chocolate(cursor):
    query = """SELECT store.name, store.address, MIN(sell.price)
    FROM store JOIN sell ON store.name=sell.name
    GROUP BY store.name, store.address ORDER BY MIN(sell.price) DESC"""
    cursor.execute(query)
    viewinfo(cursor,["Name","Adress", "Lowest price"])


def big_shoppers(cursor):
    query = """SELECT customer.personal_code, customer.address, visit.pay 
    FROM costumer JOIN visit ON customer.personal_code=visit.personal_code
    GROUP BY customer.personal_code, customer_address ORDER BY visit.pay DESC"""
    cursor.execute(query)
    viewinfo(cursor,["Personal_Code", "City", "pay"])

def inexpensive_chocolate(cursor, company, taste):
    cursor.execute(f"""SELECT store.name, store.address, company, taste, MIN(sell.price)
    FROM store JOIN sell ON store.name=sell.name
    JOIN chocolate ON chocolate.product_number=sell.product_number
    WHERE chocolate.company LIKE "%{company}%" AND chocolate.taste LIKE "%{taste}%"
    GROUP BY store.name, store.address, company, taste ORDER BY MIN(sell.price)  ASC;""")

def peoples_score(cursor):
    
    query = """SELECT """
