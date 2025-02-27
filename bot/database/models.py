from sqlalchemy import Column, Integer, Float
from database.engine import Base

class User(Base):
	__tablename__ = "users"
	id = Column(Integer, primary_key=True)  # Discord user id 

	min = Column(Float, default=0)  # Broxa
	avg = Column(Float, default=0)  # Meia bomba
	max = Column(Float, default=0)  # Duro
