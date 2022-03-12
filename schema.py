from mysql.connector import errorcode
import mysql.connector
import csv
import msvcrt as m
# Start connection to server
cnx = mysql.connector.connect(user='root', password='UJHqn7wVr5',
                              host='127.0.0.1')
# The name of the database
DB_NAME = 'choklad-shop'

# Set where to find the data to insert
shops_location = "data/shops.csv"
kunder_location = "data/kunder.csv"
choklad_location = "data/choklad.csv"
besokare_location = "data/besokare.csv"
saljer_location = "data/saljer.csv"
gillar_location = "data/gillar.csv"

storeColumns = """CREATE TABLE store
                (name nvarchar(50) not null,
                address nvarchar(50),
                primary key(name))"""
customerColumns = """CREATE TABLE customer
                (personal_code nvarschar(15) not null,
                first_name nvarchar(50),
                last_name nvarchar(50),
                city nvarchar(50),
                primary ket(personal_code))"""
chocolateColumns = """CREATE TABLE chocolate
                (product_number int not null,
                company nvarchar(50)"""

# Creating a cursor for the connection
cursor = cnx.cursor()

# Insert the data in the tables
def insert_tabledata(cursor, location, table):
    try:
        with open(location) as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)  # Skip first row
            
    except FileNotFoundError:
        print("Sorry, the file " + table + "does not exist.")


# Creating the database with the right tables and data
def create_database(cursor, DB_NAME):
    try:
        # Try to create database
        cursor.execute(f"CREATE DATABASE {DB_NAME} DEFAULT " +
                       "CHARACTER SET 'utf8'")
    except mysql.connector.Error as err:
        # Show error message and exit
        print("Faild to create database {}".format(err))
        exit(1)
    print(f"Database {DB_NAME} created.")
    # Use database
    cnx.database = DB_NAME
    create_table(cursor, storeColumns)
    create_table(cursor, "CREATE TABLE species" +
                         "(name nvarchar(50) not null, " +
                         "classification nvarchar(50), " +
                         "designation nvarchar(50), average_height int, " +
                         "skin_colors nvarchar(50), " +
                         "hair_colors nvarchar(50), " +
                         "eye_colors nvarchar(50), " +
                         "average_lifespan nvarchar(50)," +
                         " language nvarchar(50), homeworld nvarchar(50), " +
                         "primary key(name))")


# Create table with sql command.
def create_table(cursor, sql):
    try:
        # Try to create table
        print("Creating table species: ")
        cursor.execute(sql)
    except mysql.connector.Error as err:
        # If error message says that table alredy exist print it
        # else print error message
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            # Created the table
            print(err.msg)
        m.getch()
    else:
        # Created the table
        print("OK")


# The menu
def menu():
    # print all the
    print("1. List all planets.")
    print("2. Search for planet details.")
    print("3. Search for species with height higher than given number.")
    print("4. What is the most likely desired climate of the given species?")
    print("5. What is the avarage lifespan per species classification?")
    print("Q. Quit")
    print("-"*9)
    # Ask what to do
    choice = input("Please choose one option: ")
    print("-"*9)
    if choice == "1":
        # List all planets
        cursor.execute("SELECT name FROM planets")
        printCommand(cursor)
    elif choice == "2":
        # Search for planet details
        planet = input("Enter name of a planet: ")
        print("-"*9)
        cursor.execute(f"SELECT * FROM planets WHERE name LIKE '%{planet}'")
        data = cursor.fetchall()
        cursor.execute("SHOW COLUMNS FROM planets")
        columns = cursor.fetchall()
        y = 0
        for row in data:
            if not(y == 0):
                print("- "*9)
            y += 1
            i = 0
            for value in row:
                if not i == 0:
                    print(", ")
                print(columns[i][0] + ":", value, end="")
                i += 1
            print()
    elif choice == "3":
        # Search for species with height higher than given number
        try:
            # Try to pars to int
            h = int(input("Enter a number: "))
            print("-"*9)
            cursor.execute("SELECT name FROM species " +
                           f"WHERE average_height > {h}")
            printCommand(cursor)
        # Print Error
        except ValueError:
            print("That is not a number")
        except mysql.connector.Error as err:
            print(err)
    elif choice == "4":
        # What is the most likely desired climate of the given species?
        name = input("Enter name of the species: ")
        print("-"*9)
        # Find all species names like the input and find there homeplanets and
        # the homplanets climate
        cursor.execute("SELECT species.name, climate FROM planets" +
                       " RIGHT JOIN species ON planets.name" +
                       " = species.homeWorld WHERE planets.name IN " +
                       "(SELECT homeWorld FROM " +
                       f"species WHERE species.name LIKE '%{name}%')")

        # Print a table from the information
        print("_"*60)
        print("|{:^25} | {:^30}|".format("Species", "Climate"))
        print("|" + "="*26 + "|" + "="*31 + "|")
        i = 0
        for (name, climate) in cursor:
            if not i == 0:
                print("|" + "-"*26 + "|" + "-"*31 + "|")
            print("|{:^25} | {:^30}|".format(name, climate if
                                             climate is not None else "None"))
            i += 1
        print("¨"*60)

    elif choice == "5":
        # What is the avarage lifespan per species classification?
        cursor.execute("SELECT DISTINCT(classification) FROM species")
        for e in cursor.fetchall():
            if e[0] is not None:
                cursor.execute("SELECT AVG(average_lifespan) FROM species " +
                               f"WHERE classification = '{e[0]}'")
                average_lifespan = cursor.fetchall()[0][0]
                print(e[0]+":", average_lifespan if
                      average_lifespan != 0 else "indefinite")
    elif choice.upper() == "Q":
        return()
    else:
        print("The option does not exist please choose 1, 2, 3, 4, 5 or Q")
    m.getch()
    print("-"*9)
    menu()


# Try to use DATABASE and if it crashes create it
try:
    cursor.execute(f"USE {DB_NAME}")
except mysql.connector.Error as err:
    # Database does not exist
    print("Database {} does not exist".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        # Create database
        create_database(cursor, DB_NAME)
        # Inssert database in tables
        insert_tabledata(cursor, planets_location, "planets")
        insert_tabledata(cursor, species_location, "species")
    else:
        print(err)


# Start the program
menu()
cursor.close()
# Close the connection to the database.
cnx.close()
