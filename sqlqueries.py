from tkinter import messagebox
from functions import viewinfo
import mysql.connector


# Get the avrage score of a choclate
def avrage_rate_chocklate(cursor, company, taste):
    query = """SELECT chocolate.company, chocolate.taste, AVG(likes.score)
    FROM chocolate JOIN likes ON chocolate.product_number=likes.product_number
    WHERE chocolate.company LIKE %s AND chocolate.taste LIKE %s
    GROUP BY chocolate.taste, chocolate.company
    ORDER BY AVG(likes.score) DESC"""
    cursor.execute(query, (company + "%", taste + "%"))
    viewinfo(cursor, ["company", "taste", "score"])


# Get score from all chocolates in a store
def stores_popular_chocolate(cursor, store):
    query = """SELECT chocolate.company, chocolate.taste, AVG(likes.score)
    FROM chocolate JOIN likes ON chocolate.product_number=likes.product_number
    JOIN sell ON chocolate.product_number = sell.product_number
    WHERE sell.name LIKE %s
    GROUP BY chocolate.company, chocolate.taste
    ORDER BY AVG(likes.score) DESC"""
    cursor.execute(query, (store + "%",))
    viewinfo(cursor, ["Company", "Taste", "Avrage score"])


# Get the cheapest chocolate from a store
def cheapest_chocolate(cursor, store):
    query = """SELECT store.name, store.address, MIN(sell.price)
    FROM store JOIN sell ON store.name=sell.name
    WHERE store.name LIKE %s
    GROUP BY store.name, store.address ORDER BY MIN(sell.price) ASC"""
    cursor.execute(query, (store + "%",))
    viewinfo(cursor, ["Name", "Adress", "Lowest price"])


# Get all the personal scores
def personal_scores(cursor, personal_number):
    cursor.execute("""SELECT company, taste, score
                    FROM likes JOIN chocolate ON
                    likes.product_number = chocolate.product_number
                    WHERE likes.personal_code = %s ORDER BY score DESC;""",
                   (personal_number,))
    viewinfo(cursor, ["Comany", "Taste", "Score"])


# Get all the shoppers from a store
def shoppers(cursor, store):
    query = """SELECT * FROM shoppers WHERE name LIKE %s """
    cursor.execute(query, (store + "%",))
    viewinfo(cursor, ["personal_code", "city", "store", "pay"])


# Get all the cheapest chocolate and where to buy them
def inexpensive_chocolate(cursor, company, taste):
    cursor.execute("""SELECT store.name, store.address, company, taste, MIN(sell.price)
    FROM store JOIN sell ON store.name=sell.name
    JOIN chocolate ON chocolate.product_number=sell.product_number
    WHERE chocolate.company LIKE %s AND chocolate.taste LIKE %s
    GROUP BY store.name, store.address, company, taste
    ORDER BY MIN(sell.price) ASC;""", (company + "%", taste + "%"))
    viewinfo(cursor,
             ["Store_name", "Adress", "Company_name", "Taste", "Lowest price"])


# Find the productnumber of a chocolate
def find_productnumber(cursor, company, taste):
    cursor.execute("""SELECT product_number, company, taste
    FROM chocolate
    WHERE chocolate.company LIKE %s AND chocolate.taste LIKE %s;""",
                   (company + "%", taste + "%"))
    viewinfo(cursor, ["Product_number", "Company_name", "Taste"])


# Get all the vitits from a person
def get_visits(cursor, personal_code):
    cursor.execute("""SELECT name, date, time, pay FROM visit
                    WHERE visit.personal_code = %s ;""", (personal_code,))
    viewinfo(cursor, ("Store name", "Date", "Time", "Payed"))


# Add a score to the table likes
def add_scores(cursor, personal_code, product_number, score, cnx):
    # get the information of what chocolate the user entered and if it exists
    cursor.execute("SELECT * FROM chocolate WHERE product_number = %s ",
                   (product_number,))
    copy = list(cursor)
    # Se if it exists
    if len(copy) == 0:
        return (False, "Product does not exist")
    try:
        # Try to parse the score and if it is a int
        score = int(score)
    except ValueError:
        # return a error message
        return (False, "score is not an int")
    if score <= 10 and 0 <= score:
        # Make a message box to se if you realy wanted to add that score
        msgBox = messagebox.askquestion('Add score', f'''Are you sure you want
        to add score\nscore:{score} | for chocolate: {copy[0][2]} |
        from the company:{copy[0][1]}''', icon='warning')
        if msgBox == "yes":
            # If yes then add it
            try:
                # Inserts the values:
                cursor.execute("""INSERT INTO likes VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE likes.score = %s;""",
                               (personal_code, product_number, score, score))
            except mysql.connector.Error as err:
                # If the insert has failed.
                return (False, f"Could not insert {err}")
            else:
                # If it works commit and send a information message
                cnx.commit()
                return (True, f"""Inserted score:{score} | for chocolate:
                {copy[0][2]} | from the company:{copy[0][1]}""")
        else:
            # If you said no send a canceled message
            return (False, "Acction canceled")
    else:
        # If the input was not inbetween zero and 10 send a error message
        return (False, "score is not between zero and 10")
