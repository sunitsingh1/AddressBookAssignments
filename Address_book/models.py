from sqlalchemy import Column, Integer, String, Numeric
from database import Base

# Define AddressBook class inheriting from Base
class AddressBook(Base):
    __tablename__ = 'addressbook'
    id = Column(Integer, primary_key=True)
    place_name = Column(String(256))
    city = Column(String(256))
    lat = Column(Numeric(9,6))
    long = Column(Numeric(9,6))
    
