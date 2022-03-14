from GUI import viewinfo
import mysql.connector

def avrage_rate_chocklate(cursor):
    query = """SELECT chocolate.company, chocolate.taste, AVG(likes.score)
    FROM chocolate JOIN likes ON chocolate.product_number=likes.product_number
    GROUP BY chocolate.taste, chocolate.company ORDER BY AVG(likes.score) DESC"""
    cursor.execute(query)
    viewinfo(cursor,["company", "taste", "score"])



def cheapest_chocolate(cursor):
    query = """SELECT"""


