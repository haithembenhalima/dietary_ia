from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,index=True)
    age = Column(Integer,index=True)
    weight = Column(Integer,index=True)
    height = Column(Integer,index=True)
    blood_type = Column(String(255), index=True)
    disease = Column(String(255), index=True)
    drugs = Column(String(255), index=True)
    isValide = Column(Boolean, index=True)