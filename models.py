from sqlalchemy import Column,Integer,Float,String,ForeignKey
from sqlalchemy.orm import declarative_base,relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,index=True)
    username = Column(String(100),unique=True)
    password = Column(String(300))



class Category(Base):
    __tablename__ = "Categories"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(50))

    products = relationship('Product',back_populates='category')

class Product(Base):

    __tablename__ = "Products"


    id =Column (Integer,primary_key=True,index=True)
    name = Column(String(50))
    description = Column(String(100))
    price =Column(Float)
    cost_price = Column(Float)
    category_id = Column(Integer,ForeignKey("Categories.id"))

    category = relationship('Category',back_populates='products')