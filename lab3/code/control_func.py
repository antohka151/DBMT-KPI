from crud import *
from view import *


def request():
    input_command = command_identification()

    # Select function.
    if input_command == '1':
        table_name = table()
        select(table_name)

    # Add function.
    elif input_command == '2':
        table_name = table()
        add(values_to_add(table_name))

    # Delete function.
    elif input_command == '3':
        table_name = table()
        filter_column, filter_value = filter_column_data(table_name)
        delete(table_name, filter_column, filter_value)

    # Update function.
    elif input_command == '4':
        table_name = table()
        filter_column, filter_value = filter_column_data(table_name)
        update_column, update_value = column_to_update_data(table_name)
        update(table_name, filter_column, filter_value, update_column, update_value)

    # Exit from menu.
    elif input_command == '0':
        exiting()

    else:
        command_error()
        main()

    main()


def main():
    menu()
    request()


if __name__ == '__main__':
    # Uncomment to create new database.
    # recreate_database()
    main()
