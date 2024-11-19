import mysql.connector
from mysql.connector import Error

def connect_database():
    db_name = 'library_management_db'
    user = 'root'
    password = 'MySQL1sLif3!'
    host = 'localhost'

    try:
        conn = mysql.connector.connect(
            database = db_name,
            user = user,
            password = password,
            host = host,
            use_pure = True
        )
            
        print("\nSuccessfully connected to database.")
        return conn

    except Error as e:
        print(f"\nError: {e}")
        return None