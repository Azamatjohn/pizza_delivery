
from sqlalchemy import Column, Integer, Boolean,String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy_utils import ChoiceType

from database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(150), nullable=False, unique=True)
    password = Column(String, nullable=False)
    email = Column(String(225), nullable=False, unique=True)
    is_staff = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=False)
    orders = relationship('Order', lazy='dynamic', back_populates='user')

    def __repr__(self):
        return f"<user {self.username}>"


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    ORDER_STATUS = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
        ('In_transit', 'In_transit'),
    )
    quantity = Column(Integer, nullable=False, default=0)
    order_statuses = Column(ChoiceType(ORDER_STATUS), nullable=False, default='Pending')
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship(User, back_populates='orders')
    product_id = Column(Integer, ForeignKey('products.id'), nullable=True)
    product = relationship("Product", back_populates='orders')

    def __repr__(self):
        return f"<order {self.id}>"



class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False)
    orders = relationship('Order', back_populates='product')

    def __repr__(self):
        return f"<product {self.name}>"



