from typing import List
from fastapi import FastAPI, status, HTTPException, Depends
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
# from pydantic.types import condecimal
from fastapi.encoders import jsonable_encoder
import models
import schemas

from geopy import distance

# Create the database
Base.metadata.create_all(engine)

# Initialize app
app = FastAPI()

# Helper function to get database session
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@app.get("/")
def root():
    return "Address Book App"

@app.post("/addressbook", response_model=schemas.AddressBook, status_code=status.HTTP_201_CREATED)
def create_addressBook(addressBook: schemas.AddressBookCreate, session: Session = Depends(get_session)):

    # create an instance of the AddressBook database model
    addressBookdb = models.AddressBook(place_name = addressBook.place_name, city = addressBook.city, lat = addressBook.lat, 
                                        long = addressBook.long)

    # add it to the session and commit it
    session.add(addressBookdb)
    session.commit()
    session.refresh(addressBookdb)

    # return the addressBook object
    return addressBookdb

@app.get("/addressBook/{id}", response_model=schemas.AddressBook)
def read_addressBook(id: int, session: Session = Depends(get_session)):

    # get the addressBook item with the given id
    addressBook = session.query(models.AddressBook).get(id)

    # check if addressBook item with given id exists. If not, raise exception and return 404 not found response
    if not addressBook:
        raise HTTPException(status_code=404, detail=f"addressBook item with id {id} not found")
    # print(addressBook.long)
    return addressBook

@app.put("/addressBook/{id}", response_model=schemas.AddressBook)
def update_addressBook(id: int, addressbook_request:schemas.AddressBookCreate, session: Session = Depends(get_session)):

    # get the addressBook item with the given id 
    addressBook = session.query(models.AddressBook).get(id)

    # update addressBook item with the given task (if an item with the given id was found)
    if addressBook:
        update_item_encoded = jsonable_encoder(addressbook_request)
        addressBook.place_name = update_item_encoded["place_name"]
        addressBook.city = update_item_encoded["city"]
        addressBook.lat = update_item_encoded["lat"]
        addressBook.long = update_item_encoded["long"]
        session.commit()

    # check if addressBook item with given id exists. If not, raise exception and return 404 not found response
    if not addressBook:
        raise HTTPException(status_code=404, detail=f"addressBook item with id {id} not found")

    return addressBook

@app.delete("/addressBook/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_addressBook(id: int, session: Session = Depends(get_session)):

    # get the addressBook item with the given id
    addressBook = session.query(models.AddressBook).get(id)

    # if addressBook item with given id exists, delete it from the database. Otherwise raise 404 error
    if addressBook:
        session.delete(addressBook)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"addressBook item with id {id} not found")

    return None

@app.get("/addressBook", response_model = List[schemas.AddressBook])
def read_addressBook_list(session: Session = Depends(get_session)):

    # get all addressBook items
    addressBook_list = session.query(models.AddressBook).all()

    return addressBook_list

@app.get("/getaddressbycoordinate", response_model = List[schemas.AddressBook])
def get_address_by_coordinate(dist:float, lat:float, long:float, session:Session = Depends(get_session)):
    center_point_tuple =(lat,long)
    radius = dist # in kilometer
    address = []
    # print(center_point_tuple)
    addressBook_list = session.query(models.AddressBook).all()
    for data in addressBook_list:
        test_point_tuple = (data.lat,data.long)
        # print(test_point_tuple)
        # print((data.long))
        dis = distance.distance(center_point_tuple, test_point_tuple).km
        # print("Distance: {}".format(dis))

        if dis <= radius:
            address.append(data)
    return address