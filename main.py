#Python
from importlib.resources import path
from typing import Optional
from enum import Enum
#Pydantic
from pydantic import BaseModel,HttpUrl, ValidationError
from pydantic import Field
from pydantic import EmailStr
#FastAPI
from fastapi import status
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Body, Query, Path, Form, Header, Cookie, UploadFile, File

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

class PersonBase(BaseModel):
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



class Person(PersonBase):
   
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

class PersonOut(PersonBase):
    pass

class LoginOut(BaseModel):
    username: str = Field(...,max_Length=20, example="david2022")
    message: str = Field(default="Login Successfully")


@app.get(
path="/", 
status_code = status.HTTP_200_OK
)


def home():
    return {"Hello" : "World"}

#Request and Response Body

@app.post(
    path="/person/new", 
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED)
def create_person(person: Person = Body(...)):
    return person

#Validaciones: Query parameters
@app.get(path="/person/detail",
         status_code = status.HTTP_200_OK
    )
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

persons = [1,2,3,4,5]

@app.get(path="/person/detail/{person_id}",
        
        )
def show_person(
    person_id: int = Path(
        ..., 
        gt=0,
        example=123,
        title = "Person Age",
        description="This is the person id. It's required.")
):
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This person doesn't exists!"
        )
    return {person_id: "it exists"}

#Validaciones Request Body

@app.put(path="/person/{person_id}"
        #  status_code=status.HTTP_200_OK,
         )
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

@app.post(
    path="/login",
    response_model=LoginOut,
    status_code = status.HTTP_200_OK
)
def login(username:str = Form(...),password:str=Form(...)):
    return LoginOut(username=username)

#Cookies and Headers parameters

@app.post(
    path="/contact",
    status_code = status.HTTP_200_OK,
)
def contact(
    first_name : str = Form(
        ...,
        max_Length=20,
        min_Length=1,
        ),
    last_name : str = Form(
        ...,
        max_Length=20,
        min_Length=1,
        ),
    email: EmailStr = Form(...),
    message: str = Form(
        ...,
        min_Length=20,
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
):
    return user_agent

#Files

@app.post(
    path="/post-image",

)

def post_image(
    image: UploadFile = File(...)
):

    return {
        "Filename": image.filename ,
        "Format": image.content_type ,
        "Size(kB)": round(len(image.file.read())/1024, ndigits=2)  
    }