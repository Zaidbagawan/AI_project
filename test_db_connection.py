import psycopg
from getpass import getpass

try:
    password = getpass("Enter PostgreSQL password: ")

    connection = psycopg.connect(
        host="localhost",
        port=5432,
        dbname="semantic_search_db",
        user="postgres",
        password=password
    )

    print("Successfully connected to PostgreSQL!")

    connection.close()
    print("Database connection closed.")

except psycopg.Error as error:
    print("Database connection failed:", error)