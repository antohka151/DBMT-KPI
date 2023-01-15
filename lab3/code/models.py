from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

Base = declarative_base()


class Customer(Base):
    __tablename__ = 'customers'

    customer_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    orders = relationship("Order", cascade="all,delete", passive_deletes=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Customer(customer_id='{}', name='{}')>" \
            .format(self.customer_id, self.name)


class Order(Base):
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id', ondelete='CASCADE'))
    date = Column(DateTime(timezone=True), server_default=func.now())
    product_id = Column(Integer, ForeignKey('products.product_id', ondelete='CASCADE'), nullable=False)

    def __init__(self, customer_id, product_id):
        self.customer_id = customer_id
        self.product_id = product_id

    def __repr__(self):
        return "<Order(order_id='{}', customer_id='{}', date='{}', product_id='{}')>" \
            .format(self.order_id, self.customer_id, self.date, self.product_id)


class Product(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True)
    product_name = Column(String, nullable=False)

    products = relationship("Order", cascade="all,delete", passive_deletes=True)

    def __init__(self, product_name):
        self.product_name = product_name

    def __repr__(self):
        return "<Customer(product_id='{}', product_name='{}')>" \
            .format(self.product_id, self.product_name)
