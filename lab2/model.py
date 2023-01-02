import sys
import time
import psycopg2

from view import *


def db_connect():
    return psycopg2.connect(
        database="KPI_DB",
        user="postgres",
        password="",
        host="localhost",
        port="5432"
    )


def db_error(err):
    print(f"\nError code - {err.pgcode}")
    print(f'WARNING: Error {err}')
    sys.exit(-1)


def table_nf(table_name):
    print(f"ERROR: Table {table_name} was not found in the database")
    sys.exit(-1)


def select_column(table_name, column_name):
    con = db_connect()
    cursor = con.cursor()
    try:
        cursor.execute(f"SELECT {column_name} FROM {table_name}")
        print(f"SELECT {column_name} FROM {table_name}")
        for row in cursor.fetchall():
            print(row)
    except psycopg2.Error as err:
        db_error(err)

    cursor.close()
    con.close()


def random(table_name, n):
    con = db_connect()
    con.set_session(autocommit=True)
    cursor = con.cursor()
    if table_name == 'customers':
        try:
            query = "INSERT INTO customers (name) " \
                    "SELECT  chr(trunc(65+random()*25)::int) || chr(trunc(65 + random()*25)::int) " \
                    f"FROM generate_series(1,{n});"
            cursor.execute(query)
            print(query)
        except psycopg2.Error as err:
            db_error(err)

    elif table_name == 'products':
        try:
            query = "INSERT INTO products (product_name) " \
                    "SELECT  chr(trunc(65+random()*25)::int) || " \
                    "        chr(trunc(65 + random()*25)::int) || chr(trunc(65 + random()*25)::int) " \
                    f"FROM generate_series(1,{n});"
            cursor.execute(query)
            print(query)
        except psycopg2.Error as err:
            db_error(err)

    elif table_name == 'orders':
        try:
            query = "INSERT INTO orders (customer_id, product_id) " \
                    "SELECT ROUND((RANDOM()*((SELECT COUNT(*) FROM customers)-1))+1), " \
                    "       ROUND((RANDOM()*((SELECT COUNT(*) FROM products)-1))+1) " \
                    f"FROM generate_series(1,{n});"
            cursor.execute(query)
            print(query)
        except psycopg2.Error as err:
            db_error(err)

    else:
        table_nf(table_name)

    cursor.close()
    con.close()


def delete(table_name, column, row):
    con = db_connect()

    con.set_session(autocommit=True)
    cursor = con.cursor()

    if table_name == 'customers':
        try:
            cursor.execute(f"DELETE FROM orders WHERE customer_id = {row};"
                           f"DELETE FROM customers WHERE customer_id = {row};")
        except psycopg2.Error as err:
            db_error(err)
    elif table_name == 'products':
        try:
            cursor.execute(f"DELETE FROM orders WHERE product_id = {row};"
                           f"DELETE FROM products WHERE product_id = {row};")
        except psycopg2.Error as err:
            db_error(err)
    elif table_name == 'orders':
        try:
            cursor.execute(f"DELETE FROM orders WHERE {column} = {row};")
        except psycopg2.Error as err:
            db_error(err)
    else:
        table_nf(table_name)

    cursor.close()
    con.close()


def add_inf(table_name):
    con = db_connect()
    con.set_session(autocommit=True)
    cursor = con.cursor()

    if table_name == 'customers':
        print("Enter customer name:")
        customer_name = input()
        try:
            cursor.execute(f"INSERT INTO customers (name) VALUES ('{customer_name}')")
        except psycopg2.Error as err:
            db_error(err)
    elif table_name == 'products':
        print("Enter product name:")
        product_name = input()
        try:
            cursor.execute(f"INSERT INTO products (product_name) VALUES ('{product_name}')")
        except psycopg2.Error as err:
            db_error(err)
    elif table_name == 'orders':
        print("Enter customer_id and product_id")
        customer_id, product_id = input(), input()
        try:
            cursor.execute(f"INSERT INTO orders (customer_id, product_id)"
                           f"VALUES ({customer_id},{product_id})")
        except psycopg2.Error as err:
            db_error(err)
    else:
        table_nf(table_name)

    cursor.close()
    con.close()


def update_two(table1, table2, column, old_value, new_value):
    con = db_connect()
    con.set_session(autocommit=True)
    cursor = con.cursor()
    try:
        cursor.execute(
            f"UPDATE {table1} SET {column} = {new_value} WHERE {column} = {old_value})"
            f"UPDATE {table2} SET {column} = {new_value} WHERE {column} = {old_value}")
    except psycopg2.Error as err:
        db_error(err)
    cursor.close()
    con.close()


def update_one(table, column, old_name, new_name):
    con = db_connect()
    con.set_session(autocommit=True)
    cursor = con.cursor()
    try:
        cursor.execute(f"UPDATE {table} SET {column} =  {new_name} WHERE {column} = {old_name}")
    except psycopg2.Error as err:
        db_error(err)
    cursor.close()
    con.close()


def update(table_name, column_name):
    con = db_connect()
    con.set_session(autocommit=True)
    cursor = con.cursor()
    select_column(table_name, column_name)
    if table_name in ('products', 'customers') and column_name in ('customer_id', 'product_id'):
        try:
            update_two('orders', table_name, column_name, get_old_data(), get_new_data())
        except psycopg2.Error as err:
            db_error(err)
    elif table_name in ('products', 'customers', 'orders'):
        try:
            update_one(table_name, column_name, get_old_data(), get_new_data())
        except psycopg2.Error as err:
            db_error(err)
    else:
        table_nf(table_name)

    cursor.close()
    con.close()


def search():
    con = db_connect()
    con.set_session(autocommit=True)
    cursor = con.cursor()

    n = int(input("Input number of attributes to search by >>> "))
    if n not in (1, 2, 3):
        print("Error, wrong number of attributes (1 or 2 or 3). You just don't need more for this database")
        exit(-1)

    attributes = [str(input(f"Input attribute №{h + 1} >>> ")) for h in range(n)]
    print(attributes)

    std_query = f"SELECT t.table_name " \
                f"FROM information_schema.tables t " \
                f"INNER JOIN information_schema.columns c ON c.table_name = t.table_name " \
                f"WHERE c.column_name LIKE 'attribute' " \
                f"      AND t.table_schema NOT IN ('information_schema', 'pg_catalog') "

    get_table_query = ' INTERSECT '.join(std_query.replace('attribute', attribute) for attribute in attributes)

    print("\n Executed query:", get_table_query, '\n')

    cursor.execute(get_table_query)

    tables = [table_name[0] for table_name in cursor.fetchall()]

    types = []
    for attribute in attributes:
        cursor.execute(
            f"SELECT DISTINCT data_type FROM INFORMATION_SCHEMA.COLUMNS WHERE column_name = '{attribute}' and table_schema = 'public'")
        types += [list(cursor.fetchall()[0])]

    attributes = dict(zip(attributes, types))

    for attribute in attributes:
        print()
        if attributes[attribute][0] == "character varying":
            attributes[attribute] += [input(f"Enter value for {attribute}: ")]
        elif attributes[attribute][0] in ("integer", "timestamp with time zone"):
            attributes[attribute] += [input(f"Enter left boundary for {attribute}: ")]
            attributes[attribute] += [input(f"Enter right boundary for {attribute}: ")]
        else:
            print("Attribute type error")
            exit(-1)

    start_time = time.time()

    results = []
    for table in tables:
        std_query = f"SELECT * " \
                    f"FROM {table} " \
                    f"WHERE "
        tmp = []

        for attribute in attributes:
            if attributes[attribute][0] == 'integer':
                tmp += [f"{attribute} > {attributes[attribute][-2]} AND {attribute} < {attributes[attribute][-1]} "]
            elif attributes[attribute][0] == "timestamp with time zone":
                tmp += [f"{attribute} > '{attributes[attribute][-2]}' AND {attribute} < '{attributes[attribute][-1]}' "]
            elif attributes[attribute][0] == "character varying":
                tmp += [f"{attribute} LIKE '{attributes[attribute][-1]}' "]

        cursor.execute(std_query + ' AND '.join(tmp))
        print("\n Executed query:", std_query + ' AND '.join(tmp), '\n')
        results += cursor.fetchall()

    print('-' * 10)
    print(f"{len(results)} rows with specified attributes have been found:")
    print(*results, sep='\n')
    print('-' * 10)

    print("Time:%s seconds" % (time.time() - start_time))
    cursor.close()
    con.close()
