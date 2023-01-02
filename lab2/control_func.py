from model import *
from view import *


def request():
    input_command = command_identification()

    if input_command == '1':
        table_name = table()
        column_name = column()
        update(table_name, column_name)
    elif input_command == '2':
        table_name = table()
        add_inf(table_name)
    elif input_command == '3':
        table_name = table()
        column_name = column()
        delete(table_name, column_name, get_data())
    elif input_command == '4':
        table_name = table()
        random(table_name, get_data())
    elif input_command == '5':
        search()
    elif input_command == '0':
        exiting()
    else:
        command_error()
        main()


def main():
    menu()
    request()


if __name__ == '__main__':
    main()
