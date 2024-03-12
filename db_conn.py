# import time
# import pyodbc
from sqlalchemy import create_engine, update
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import bindparam
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import insert as sqlite_upsert
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_PORT = os.getenv('DATABASE_PORT', 5432)
DATABASE_NAME = os.getenv('DATABASE_NAME')

SQLALCHEMY_DATABASE_URI = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@localhost:{DATABASE_PORT}/{DATABASE_NAME}"

# SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@localhost:{DATABASE_PORT}/{DATABASE_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URI)
# engine = create_engine("sqlite:///test.db")


class Base(DeclarativeBase):
    pass


class ProductsTable(Base):
    __tablename__ = "products_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    Product: Mapped[str] = mapped_column(String(8000))
    Seller: Mapped[str] = mapped_column(String(8000))
    Data_Date: Mapped[str] = mapped_column(String(8000))
    Data_Time: Mapped[str] = mapped_column(String(8000))
    Price: Mapped[str] = mapped_column(String(8000))
    Product_price: Mapped[str] = mapped_column(String(8000))
    Product_URL: Mapped[str] = mapped_column(String(8000))
    