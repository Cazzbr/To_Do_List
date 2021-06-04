from sqlalchemy import Column, Integer, String, Date, Boolean, create_engine, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlite3

# Declaração da base de dados;
Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    usr = Column(String, unique=True)
    passw = Column(String)
    auto = Column(Boolean, nullable=False, default=False)
    lang = Column(String)
    datas = relationship("Data", backref='author', lazy=True)

class Data(Base):
    __tablename__ = 'data'
    id = Column(Integer, primary_key=True)
    done = Column(Boolean)
    prio = Column(Integer)
    title = Column(String)
    descr = Column(String)
    dia = Column(Date)
    dia_c = Column(Date)
    user_id = Column(Integer, ForeignKey('users.id'),  nullable=False)

# Setup da conexão com banco de dados;
conn = 'sqlite:///To_Do_List_DB.sqlite3'
engine = create_engine(conn)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
