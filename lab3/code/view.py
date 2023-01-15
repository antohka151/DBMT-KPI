import sys

from models import *


def table_invalid():
    print('The table name is wrong ERROR')
    sys.exit()


def column_invalid():
    print("The column name is wrong ERROR")
    sys.exit()


def exiting():
    print('Exiting')
    sys.exit()


def command_error():
    print("ERROR: You have to enter the number from 0 to 4")


def command_identification():
    return input('Enter command : ')


def table():
    print('Your table names: customers, orders, products')
    table_name = input('Enter table name: ')

    tables = {'customers': Customer, 'orders': Order, 'products': Product}
    if table_name not in tables.keys():
        return table_invalid()
    return tables[table_name]


def values_to_add(table_name):
    if table_name == Order:
        print("Please, enter customer id:")
        customer_id = input()
        print("Please, enter product id:")
        product_id = input()

        if not customer_id.isdigit() or not product_id.isdigit():
            print("ERROR: Id should be a number")
            sys.exit()

        return Order(int(customer_id), int(product_id))
    else:
        print(f"Please, enter {'product_name' if table_name == Product else 'name'}")
        return table_name(input())


def column(table_name):
    if table_name == Order:
        return Order.order_id
    elif table_name == Customer:
        return Customer.customer_id
    else:
        return Product.product_id


def get_column(table_name):
    if table_name == Order:
        print('There are 3 columns {customer_id, order_id, product_id}')
        print('Please, choose 1 column:')
        column = input()
        columns = {'customer_id': Order.customer_id, 'order_id': Order.order_id, 'product_id': Order.product_id}
        if column not in columns.keys():
            return column_invalid()
        return columns[column]
    elif table_name == Customer:
        print('There are 2 columns {customer_id, name}')
        print('Please, choose 1 column:')
        column = input()
        columns = {'customer_id': Customer.customer_id, 'name': Customer.name}
        if column not in columns.keys():
            return column_invalid()
        return columns[column]
    else:
        print('There are 2 columns {product_id, product_name}')
        print('Please, choose 1 column:')
        column = input()
        columns = {'product_id': Product.product_id, 'product_name': Product.product_name}
        if column not in columns.keys():
            return column_invalid()
        return columns[column]


def get_data():
    return input('Please, enter column value: ')


def filter_column_data(table_name):
    print("Please, choose column to filter with")
    filter_column = get_column(table_name)
    filter_value = get_data()
    return filter_column, filter_value


def column_to_update_data(table_name):
    print("Please, choose column to update")
    update_column = get_column(table_name)
    update_value = get_data()
    return update_column, update_value


def menu():
    print()
    print("SELECT press 1")
    print("ADD press 2")
    print("DELETE press 3")
    print("UPDATE press 4")
    print('EXIT press 0')
    print()
