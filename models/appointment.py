from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,index=True)
    doctor_id = Column(Integer,index=True)
    firstname = Column(String(255), index=True)
    lastname = Column(String(255), index=True)
    phone = Column(String(255), index=True)
    date = Column(String(255), index=True)
    time = Column(String(255), index=True)
    confirmation = Column(Integer, index=True)