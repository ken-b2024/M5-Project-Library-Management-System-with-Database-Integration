import re
from library_db_connect import connect_database

conn = connect_database()
if conn is not None:
    cursor = conn.cursor()

class User:
    
    def UserOpsMenu():
        user_menu = [
            '1. Add a new user',
            '2. View user details',
            '3. Display all users',
            '4. Return to Main Menu'
    ]
        print("\nUser Operations\n")
        print("Menu:", *user_menu, sep='\n')

    @staticmethod
    def new_user(lib_id,birth_date):
        first_name = input("Enter the first name of user: ").capitalize()
        last_name = input("Enter the last name of user: ").capitalize()
        for pattern in lib_id:
            lib_id = input("Enter the user's library ID number (format: xxxxx): ")
            pattern = (r"\d{5}")
            if re.match(pattern,lib_id):
                print("Library ID was successfully added")
                break
            else:
                print("\nID format is invalid. Try again...")
        for pattern in birth_date:
            birth_date = input("Enter the bithdate of user (format: xx/xx/xxxx): ")
            pattern = (r"\d{2}/\d{2}/\d{4}")
            if re.search(pattern, birth_date):
                print("Birthdate was successfully added.")
                break
            else:
                print("\nBirthdate format is invalid. Try again...")
        query = 'INSERT INTO users (first_name,last_name,lib_id,birth_date) VALUES (%s,%s,%s,%s)'
        cursor.execute(query,(first_name,last_name,lib_id,birth_date))
        conn.commit()
        print(f"\nThe account for {first_name} has been created successfully")

    @staticmethod
    def view_user():
        lib_id = input("Enter the user's Library ID number: ")
        query = 'SELECT * FROM users WHERE lib_id = %s'
        cursor.execute(query,[lib_id])   
        result = cursor.fetchone()     
        print("\nFetching user details...")
        print("\nUser Details:",result, sep='\n')

    def display_users():
        query = 'SELECT * FROM users'
        cursor.execute(query)
        result = cursor.fetchall()
        print("\nFetching users...")
        print("\nUsers:", *result, sep='\n')


while True:
    User.UserOpsMenu()
    try:
        user_menu_action = int(input("\nSelect an option: "))
        if user_menu_action == 1:
            User.new_user('lib_id','birth_date')
        if user_menu_action == 2:
            User.view_user()
        if user_menu_action == 3:
            User.display_users()
        if user_menu_action == 4:
            print("\nReturning to main menu...")
            break
    except ValueError:
        print("\nInput is invalid. Please try again...")

# Close cursor and connection properly at the end
cursor.close()
conn.close()