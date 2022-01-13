#Python
from typing import Optional
from enum import Enum
#Pydantic
from pydantic import BaseModel,HttpUrl, ValidationError
from pydantic import Field
#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

#Models

class url_validate(BaseModel):
    url:HttpUrl

class HairColor(Enum):
    white= "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class Location(BaseModel):
    city: str = Field(
        title = "City of the person",
        description = "This field is important to get a good performance at the platform",
        example = "Puebla"
    )
    state: str = Field(
        title = "State of Person",
        description="It's important your state",
        example = "Puebla"
    )
    country: str = Field(
        title = "Country of person",
        description="It's important to know your location",
        example = "Mexico"
    )

class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_Length=1,
        max_Length=50,
        example="David",
         )

    last_name: str = Field(
        ...,
        min_Length=1,
        max_Length=50,
        example = "Castillo" )
    age: int = Field(
        ...,
        gt=0,
        Le=115,
        example = 25

    )

    
    hair_color: Optional[HairColor] = Field(default=None, example="black")
    is_married: Optional[bool] = Field(default=None, example=False)
    password: str = Field(..., min_Length=8)
    # class Config:
    #     schema_extra = {
    #         "example":{
    #             "first_name": "David",
    #             "last_name": "Castillo Castro",
    #             "age":"21",
    #             "hair_color": "blonde",
    #             "is_married": False

    #         }
    #     }

class PersonOut(BaseModel):
    first_name: str = Field(
        ...,
        min_Length=1,
        max_Length=50,
        example="David",
         )

    last_name: str = Field(
        ...,
        min_Length=1,
        max_Length=50,
        example = "Castillo" )
    age: int = Field(
        ...,
        gt=0,
        Le=115,
        example = 25

    )


    hair_color: Optional[HairColor] = Field(default=None, example="black")
    is_married: Optional[bool] = Field(default=None, example=False)

@app.get("/")


def home():
    return {"Hello" : "World"}

#Request and Response Body

@app.post("/person/new", response_model=PersonOut)
def create_person(person: Person = Body(...)):
    return person

#Validaciones: Query parameters
@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
        None, 
        min_Length=1, 
        max_Length=50,
        title="Person Name",
        description="This is the person name. It's between and 50 characters",
        example="Rocio"
        ),
        
    age: str = Query(
        ...,
        title = "Person Age",
        description="this is the person age. It's required",
        example=25
        )
    ):

    return {name:age}

#Validaciones: Path Parameters

@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ..., 
        gt=0,
        example=123,
        title = "Person Age",
        description="This is the person id. It's required.")
):
    return {person_id: "it exists"}

#Validaciones Request Body

@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title = "Person ID",
        description = "This is the person ID",
        gt=0,
        example=123

    ),
    person:Person=Body(...),
    Location: Location = Body(...)
):
    # results = person.dict()
    # results.update(Location.dict())
    # return results
    return person
