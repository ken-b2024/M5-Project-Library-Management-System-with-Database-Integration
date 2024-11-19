from os import name
from library_db_connect import connect_database
import re
author_dict = {}

conn = connect_database()
if conn is not None:
    cursor = conn.cursor()

class Author:
    def __init__(self,name,biography):
        self.__name = name
        self._biography = biography

    def set_name(self,author_name):
        self.__name = author_name
    def get_name(self):
        return self.__name

    def AuthorOpsMenu():
        author_menu = [
            '1. Add a new author',
            '2. View author details',
            '3. Display all authors',
            '4. Return to Main Menu'
        ]
        print("\nAuthor Operations\n")
        print("Menu", *author_menu, sep='\n')

    @staticmethod
    def add_author(ISNI):
        author_name = input("Enter the name of the author: ")
        for pattern in ISNI:
            ISNI = input("Enter the last four digits of the author's ISNI: ")
            pattern = (r"\d{4}")
            if re.search(pattern, ISNI):
                print("\n ISNI successfully added.")
                break
            else:
                print("\nISNI format is invalid. Try again...")
        author_bio = input("Enter the Author's biography: ")
        query = 'INSERT INTO authors (ISNI,name,biography) VALUES(%s,%s,%s)'
        cursor.execute(query,(ISNI,author_name,author_bio))
        conn.commit()
        query_display = 'SELECT * FROM authors WHERE isni = %s'
        cursor.execute(query_display,[ISNI])
        result = cursor.fetchall()
        print("\nAuthor:", result, sep='\n')
        print("\nAuthor has been succesfully added")


    @staticmethod
    def view_author():
        ISNI = input("Enter the last four of the author's ISNI: ")
        query = 'SELECT * FROM authors WHERE isni = %s'
        cursor.execute(query,[ISNI])
        result = cursor.fetchall()
        print("\nFetching author details...\n")
        print("\nAuthor Info:", result, sep='\n')

    @staticmethod
    def display_authors():
        query = 'SELECT * FROM authors'
        cursor.execute(query)
        result = cursor.fetchall()
        print("\nFetching author database...\n")
        print("Authors:", *result, sep='\n')

while True:
    Author.AuthorOpsMenu()
    try:
        author_menu_action = int(input("\nSelect an option: "))
        if author_menu_action == 1:
            Author.add_author('ISNI')
        if author_menu_action == 2:
            Author.view_author()
        if author_menu_action == 3:
            Author.display_authors()
        if author_menu_action == 4:
            print("\nReturning to Main Menu...")
            break
    except ValueError:
        print("\nInvalid input. Please try again...")

# Close cursor and connection properly at the end
cursor.close()
conn.close()