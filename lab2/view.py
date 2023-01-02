import sys


def command_error():
    print("ERROR: You have to enter the number from 0 to 5")


def command_identification():
    return input('Enter command : ')


def table():
    print('Your table name: customers , orders , products')
    return input('Enter table name: ')


def column():
    return input('Enter column name: ')


def get_old_data():
    return input('Enter old value: ')


def get_new_data():
    return input('Enter new value: ')


def get_data():
    return input('Enter value: ')


def row():
    return int(input('Enter value: '))


def table_invalid():
    print('The table name is wrong ERROR')
    sys.exit()


def exiting():
    print('Exiting')
    sys.exit()

def menu():
    print()
    print("Update press 1")
    print("Add press 2")
    print("Delete press 3")
    print("Random press 4")
    print("Search press 5")
    print('EXIT press 0')
    print()