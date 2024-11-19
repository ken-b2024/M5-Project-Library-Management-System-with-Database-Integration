from library_db_connect import connect_database
import re

library_dict = {}

# Establish database connection
conn = connect_database()
if conn is not None:
    cursor = conn.cursor()

class Book:
    def __init__(self, title, author, genre, ISBN):
        self.__title = title
        self.__author = author
        self.__genre = genre
        self.unique_id = ISBN
        self._availabilty = True

    def get_title(self):
        return self.__title

    def set_title(self, new_title):
        self.__title = new_title

    def get_author(self):
        return self.__author

    def set_author(self, new_author):
        self.__author = new_author

    def get_genre(self):
        return self.__genre

    def set_genre(self, new_genre):
        self.__genre = new_genre

    @staticmethod
    def BookOpsMenu():
        book_menu = [
            '1. Add a new book',
            '2. Borrow a book',
            '3. Return a book',
            '4. Search for a book',
            '5. Display all books',
            '6. Return to Main Menu'
        ]
        print("\nBook Operations\n")
        print("Menu:", *book_menu, sep='\n')

    @staticmethod
    def add_book(title, author, genre, ISBN):
        while True:  # Validate ISBN format
            ISBN = input("Please enter the ISBN of the book (format: xxx-x): ")
            if re.fullmatch(r"\d{3}-\d", ISBN):
                print("ISBN successfully added.")
                break
            else:
                print("\nInvalid ISBN format. Try again...")

        title = input("Enter the Title: ")
        author = input("Enter the Author: ")
        genre = input("Enter the Genre: ")

        try:
            # Fixed SQL query to include all necessary columns
            query = '''INSERT INTO books (ISBN, Title, Author, Genre, Availability) VALUES(%s, %s, %s, %s, 1)'''
            cursor.execute(query, (ISBN, title, author, genre))
            conn.commit()
        except Exception as e:
            print(f"\nError adding book: {e}")
        else:
            print(f"\n{title} has been successfully added to the library database!")

    @staticmethod
    def borrow_book(ISBN):
        ISBN = input("Please enter the ISBN of the book (format: xxx-x): ")
        query = 'SELECT * FROM books WHERE isbn = %s AND availability = 1'
        cursor.execute(query, [ISBN])
        result = cursor.fetchone()

        if result:
            print("\nBook Info:", result)
            borrow_action = input("\nDo you want to borrow this book (y/n): ")
            if borrow_action.lower() == 'y':
                try:
                    query_update = 'UPDATE books SET availability = 0 WHERE isbn = %s'
                    cursor.execute(query_update, [ISBN])
                    conn.commit()
                    print("\nBook has been successfully marked as Unavailable.")
                except Exception as e:
                    print(f"Error borrowing book: {e}")
            else:
                print("\nReturning to menu...")
        else:
            print("\nBook is not available or does not exist.")

    @staticmethod
    def return_book(ISBN):
        ISBN = input("Please enter the ISBN of the book (format: xxx-x): ")
        query = 'SELECT * FROM books WHERE isbn = %s AND availability = 0'
        cursor.execute(query, [ISBN])
        result = cursor.fetchone()

        if result:
            try:
                query_update = 'UPDATE books SET availability = 1 WHERE isbn = %s'
                cursor.execute(query_update, [ISBN])
                conn.commit()
                print("\nBook has been successfully marked as Available.")
            except Exception as e:
                print(f"Error returning book: {e}")
        else:
            print("\nThis book is already in stock or does not exist.")

    @staticmethod
    def search_for_book(ISBN):
        ISBN = input("Please enter the ISBN of the book (format: xxx-x): ")
        query = 'SELECT * FROM books WHERE isbn = %s'
        cursor.execute(query, [ISBN])
        result = cursor.fetchone()

        if result:
            print("\nBook Info:", result)
        else:
            print("\nBook does not exist.")

    @staticmethod
    def display_book():
        query = 'SELECT * FROM books'
        cursor.execute(query)
        result = cursor.fetchall()

        if result:
            print("\nFetching book details...\n")
            for book in result:
                print(book)
        else:
            print("\nNo books available in the library.")

# Main program loop
while True:
    Book.BookOpsMenu()
    try:
        book_menu_action = int(input("\nSelect an option: "))
        if book_menu_action == 1:
            Book.add_book('title', 'author', 'genre', 'ISBN')
        elif book_menu_action == 2:
            Book.borrow_book('ISBN')
        elif book_menu_action == 3:
            Book.return_book('ISBN')
        elif book_menu_action == 4:
            Book.search_for_book('ISBN')
        elif book_menu_action == 5:
            Book.display_book()
        elif book_menu_action == 6:
            print("\nReturning to main menu...")
            break
    except ValueError:
        print("\nInvalid input. Please try again.")

# Close cursor and connection properly at the end
cursor.close()
conn.close()