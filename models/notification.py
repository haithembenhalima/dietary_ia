from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,index=True)
    date = Column(String(255), index=True)
    time = Column(String(255), index=True)
    confirmation = Column(String(255), index=True)
