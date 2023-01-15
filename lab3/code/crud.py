import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from view import *


engine = create_engine('postgresql://login:password@localhost:5432/test')

Session = sessionmaker(bind=engine)


def db_error(err):
    print("WARNING: Error has occurred\n")
    print(err)
    sys.exit(-1)


def table_nf(table_name):
    print(f"ERROR: Table {table_name} was not found in the database")
    sys.exit(-1)


def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def delete(table, column, row):
    s = Session()
    try:
        s.query(table).filter(column == row).delete()
        s.commit()
    except SQLAlchemyError as err:
        db_error(err)

    s.close()


def add(element):
    s = Session()
    try:
        s.add(element)
        s.commit()
    except SQLAlchemyError as err:
        db_error(err)

    s.close()


def select(table):
    s = Session()
    try:
        # Change to return if needed.
        print(s.query(table).all())
    except SQLAlchemyError as err:
        db_error(err)


def update(table, filter_column, filter_column_value, column_to_upd, updated_value):
    s = Session()
    try:
        s.query(table).filter(filter_column == filter_column_value).update({column_to_upd: updated_value})
        s.commit()
    except SQLAlchemyError as err:
        db_error(err)

    s.close()
