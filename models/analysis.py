from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class Analysis(Base):
    __tablename__ = "analysis"
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,index=True)
    doctor_id = Column(Integer,index=True)
    firstname = Column(String(255), index=True)
    lastname = Column(String(255), index=True)
    phone = Column(String(255), index=True)
    pdf = Column(String(255), index=True)
    max_increase = Column(String(255), index=True)
    min_decrease= Column(String(255), index=True)
    recommandation_valid = Column(String(255), index=True)