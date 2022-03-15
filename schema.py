from mysql.connector import errorcode
import mysql.connector
import csv
import os
import GUI
import sqlqueries as sq
# Start connection to server
# Filips lösenord UJHqn7wVr5
cnx = mysql.connector.connect(user='root', password='UJHqn7wVr5',
                              host='127.0.0.1', charset='utf8')

DB_NAME = 'chocolate_shop'

cursor = cnx.cursor()



# Set where to find the data to insert
store_location = "data\\store.csv"
customer_location = "data/customer.csv"
chocolate_location = "data/chocolate.csv"
visit_location = "data/visit.csv"
sell_location = "data/sell.csv"
likes_location = "data/likes.csv"

storeColumns = """CREATE TABLE store
                (name nvarchar(50) not null,
                address nvarchar(50),
                primary key(name))"""
customerColumns = """CREATE TABLE customer
                (personal_code nvarchar(50) not null,
                first_name nvarchar(50),
                last_name nvarchar(50),
                city nvarchar(50),
                primary key(personal_code))"""
chocolateColumns = """CREATE TABLE chocolate
                (product_number varchar(50) not null,
                company nvarchar(50),
                taste nvarchar(50),
                primary key(product_number))"""
visitColumns = """CREATE TABLE visit
                (name nvarchar(50),
                personal_code nvarchar(15) not null,
                date nvarchar(15) not null,
                time nvarchar(15) not null,
                pay float(15),
                primary key(personal_code,date,time))"""
sellColumns = """CREATE TABLE sell
                (name nvarchar(50) not null,
                product_number varchar(50) not null,
                price float(15),
                primary key(name,product_number))"""
likesColumns = """CREATE TABLE likes
                (personal_code nvarchar(15) not null,
                product_number varchar(50) not null,
                score float(15),
                primary key(personal_code,product_number))"""
queryShoppers = """CREATE VIEW shoppers
                AS SELECT customer.personal_code, customer.city, MAX(visit.pay) 
                FROM customer JOIN visit ON customer.personal_code=visit.personal_code
                GROUP BY customer.personal_code, customer.city ORDER BY MAX(visit.pay) DESC"""


def create_database(cursor, DB_NAME):
    # Creates the database:
    try:
        cursor.execute("""CREATE DATABASE {} DEFAULT CHARACTER SET
        'utf8'""".format(DB_NAME))
        print("created")
    # If the connection fails:
    except mysql.connector.Error as err:
        print("Faild to create database {}".format(err))
        exit(1)


def create_table(cursor, tables):
    # Creates a table:
    try:
        print("Creating table: ")
        cursor.execute(tables)
    # If the connection fails:
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")


def insert_into_table(cursor, file, table):
    # Read the csv files with tha data:
    data = open(file)
    read_file = csv.reader(data)
    header = next(read_file)  # To not include the titles in the file as values
    # Creates a string that is being used to insert values into tables.
    new_row = "("
    for column in header:
        new_row += "NULLIF(%s,'NA'), "  # Makes the "NA"s to Mysqls "NULL".
    newest_row = new_row[:-1][:-1]  # Deleting the two last charecters.
    newest_row += ")"
    for row in read_file:
        try:
            # Inserts the values:
            cursor.execute(f"INSERT INTO {table} VALUES {newest_row};", row)
        except mysql.connector.Error as err:
            print(err.msg, row)  # If the insert has failed.
        else:
            cnx.commit()
    data.close()


try:
    # If the database already exists:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exist".format(DB_NAME))
    # If the database does not exist, the database is being created:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor, DB_NAME)
        print("Database created succesfully")
        cnx.database = DB_NAME
        # Creats the tables:
        create_table(cursor, storeColumns)
        create_table(cursor, customerColumns)
        create_table(cursor, chocolateColumns)
        create_table(cursor, visitColumns)
        create_table(cursor, sellColumns)
        create_table(cursor, likesColumns)
        # Insert the data into tables from the csv files:
        insert_into_table(cursor, store_location, "store")
        insert_into_table(cursor, customer_location, "customer")
        insert_into_table(cursor, chocolate_location, "chocolate")
        insert_into_table(cursor, visit_location, "visit")
        insert_into_table(cursor, sell_location, "sell")
        insert_into_table(cursor, likes_location, "likes")
        cursor.execute(queryShoppers)
    else:
        print(err)

GUI.start(cursor)
print("hallå!!")    
