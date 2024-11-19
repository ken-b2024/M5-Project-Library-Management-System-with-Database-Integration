class AppMenu:
    @staticmethod
    def main_menu():
        menu_items = ['1. Book Operations',
                    '2. User Operations',
                    '3. Author Operations',
                    '4. Quit'
    ]
        print("\nWelcome to the Library Management System with Database Integration!")
        print("\nMain Menu:", *menu_items, sep='\n')

while True:
    if __name__ == '__main__':
        AppMenu.main_menu()
        try:
            menu_selection = int(input("\nSelect Menu Item (1-4): "))
            if menu_selection == 1:
                from BookOperations import Book
            if menu_selection == 2:
                from UserOperations import User
            if menu_selection == 3:
                from AuthorOperations import Author
            if menu_selection == 4:
                print("\nThank you for using the Library Management System with Database Integration!\n")
                break
        except ValueError:
            print("\nThat is not a valid selection. Try again...")