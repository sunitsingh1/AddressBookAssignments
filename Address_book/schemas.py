from pydantic import BaseModel
from pydantic.types import condecimal

# Create AddressBook Schema (Pydantic Model)
class AddressBookCreate(BaseModel):
    place_name: str
    city: str
    lat: condecimal(max_digits=9,decimal_places=6)
    long: condecimal(max_digits=9,decimal_places=6)
    

# Complete AddressBook Schema (Pydantic Model)
class AddressBook(BaseModel):
    id: int
    place_name: str
    city: str
    lat: condecimal(decimal_places=6,max_digits=9)
    long: condecimal(decimal_places=6,max_digits=9)
    

    class Config:
        orm_mode = True