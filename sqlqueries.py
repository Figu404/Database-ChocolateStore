from functions import viewinfo
import mysql.connector

def avrage_rate_chocklate(cursor):
    query = """SELECT chocolate.company, chocolate.taste, AVG(likes.score)
    FROM chocolate JOIN likes ON chocolate.product_number=likes.product_number
    GROUP BY chocolate.taste, chocolate.company ORDER BY AVG(likes.score) DESC"""
    cursor.execute(query)
    viewinfo(cursor,["company", "taste", "score"])


def cheapest_chocolate(cursor):
    query = """SELECT store.name, store.address, MIN(sell.price)
    FROM store JOIN sell ON store.name=sell.name
    GROUP BY store.name, store.address ORDER BY MIN(sell.price) DESC"""
    cursor.execute(query)
    viewinfo(cursor,["Name","Adress", "Lowest price"])


def stores_popular_chocolate(cursor,input):
    query = """SELECT"""


def shoppers(cursor):
    query = """SELECT * FROM shoppers"""
    cursor.execute(query)
    viewinfo(cursor, ["personal_code", "city", "pay"])



    # """SELECT customer.personal_code, customer.address, visit.pay 
    # FROM costumer JOIN visit ON customer.personal_code=visit.personal_code
    # ORDER BY visit.pay DESC"""
    
    viewinfo(cursor,["Personal_Code", "City", "pay"])


def peoples_score(cursor):
    
    query = """SELECT """
