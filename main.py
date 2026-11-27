import database
from menus import main_menu


def main():
    database.create_tables()
    main_menu.main_menu()


if __name__ == "__main__":
    main()