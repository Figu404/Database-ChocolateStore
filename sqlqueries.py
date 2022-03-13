def avrage_rate_chocklate(cursor):
    query_likes = "SELECT product_number FROM chocolate"
    cursor.execute(query_likes)
    product_numbers = cursor.fetchall()
    for n in product_numbers:
        for i in n:
            "SELECT"


