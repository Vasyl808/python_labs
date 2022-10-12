from sqlalchemy import (
    Table,
    Column,
    Integer,
    ForeignKey,
    String,
    Boolean,
    Enum,
    DateTime
)

# from sqlalchemy import orm
from sqlalchemy import create_engine, select, update, delete, values
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship

#engine = create_engine("mysql://root:password@localhost:3306/pp")
engine = create_engine("mysql+mysqlconnector://password@localhost:3306/pp")

SessionFactory = sessionmaker(bind=engine)

Session = scoped_session(SessionFactory)


BaseModel = declarative_base()


class User(BaseModel):
    __tablename__ = "user"

    id_user = Column(Integer(), primary_key=True)
    username = Column(String(255), nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    age = Column(Integer, nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    phone_number = Column(String(20), nullable=False)
    userstatus = Column(Enum("user", "pharmacist"), nullable=False)


Order_details = Table('order_details', BaseModel.metadata,
                      Column('order_id', ForeignKey('order.id_order', ondelete="CASCADE"), nullable=False),
                      Column('medicine_id', ForeignKey('medicine.id_medicine', ondelete="CASCADE"), nullable=True),
                      Column('count', Integer, nullable=False)
                      )


class Medicine(BaseModel):
    __tablename__ = "medicine"

    id_medicine = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    medicine_name = Column(String(65), nullable=False)
    manufacturer = Column(String(65), nullable=False)
    medicine_description = Column(String(255), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id_category'), nullable=False)
    price = Column(Integer, nullable=False)
    medicine_status = Column(Enum("available", "pending", "sold"), nullable=False)
    demand = Column(Boolean, nullable=False)

    order = relationship("Order", secondary=Order_details, back_populates="medicine")


class Order(BaseModel):
    __tablename__ = "order"

    id_order = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id_user', ondelete="CASCADE"), nullable=False)
    address = Column(String(350), nullable=False)
    date_of_purchase = Column(DateTime, nullable=False)
    shipData = Column(DateTime, nullable=False)
    order_status = Column(Enum("placed", "approved", "delivered"), nullable=False)
    complete = Column(Boolean, nullable=False)

    medicine = relationship("Medicine", secondary=Order_details, back_populates="order")


class Category(BaseModel):
    __tablename__ = "category"

    id_category = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    category_name = Column(String(255), nullable=False)
    description = Column(String(300), nullable=False)




