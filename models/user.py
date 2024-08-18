from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    firstname = Column(String(255),index=True)
    lastname = Column(String(255),index=True)
    adress = Column(String(255),index=True)
    wilaya = Column(String(255),index=True)
    phone = Column(String(255),index=True)
    picture = Column(String(255),index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255), index=True)
    role = Column(String(255), index=True)
    doctor_ref = Column(Integer, index=True)