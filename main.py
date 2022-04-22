# Python
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel, EmailStr, Field


# FastAPI
from fastapi import FastAPI, UploadFile, status, HTTPException
from fastapi import Body, Query, Path, Form, Cookie, Header, File

app = FastAPI()

# Models


class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"
    blue = "blue"


class Location(BaseModel):
    city: str = Field(
        ...,
        min_length=1,
        max_length=20,
        example="Eclhe"
    )

    state: str = Field(
        ...,
        min_length=1,
        max_length=20,
        example="Alicante"
    )
    country: str = Field(
        ...,
        min_length=1,
        max_length=20,
        example="Spain"
    )


class PersonBase(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    age: int = Field(
        ...,
        gt=0,
        lt=115
    )
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)

    class Config:
        schema_extra = {
            "example": {
                "first_name": "Luis",
                "last_name": "Berenguer",
                "age": 24,
                "hair_color": "black",
                "is_married": False
            }
        }


class Person(PersonBase):
    password: str = Field(..., min_length=8, max_length=150)


class PersonOut(PersonBase):
    pass


class LoginOut(BaseModel):
    username: str = Field(..., max_length=20, exmple="luissberenguer")


@app.get('/', status_code=status.HTTP_200_OK)
def home():
    return {"Hello": "World"}

# Request and response body


@app.post('/person/new', response_model=PersonOut, status_code=status.HTTP_201_CREATED)
def create_person(person: Person = Body(...)):
    return person

# Validaciones queries parameters


@app.get('/person/detail', status_code=status.HTTP_200_OK)
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title="Peron Name",
        description="This is the person name. It's between 1 and 50 charachters.",
        example="Laura"
    ),
    age: str = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's required",
        example=24
    )
):
    return {name: age}

# Vlidaciones: Path Parameters


@app.get('/person/detail/{person_id}', status_code=status.HTTP_200_OK)
def show_person(
    peron_id: int = Path(
        ...,
        gt=0,
        title="Person Id",
        description="This is the person id. It's required."
    )
):
    return {peron_id: 'Ese id existe!'}

# Validaciones: Request Body


persons = [1, 2, 3, 4, 5]


@app.put("/person/{person_id}", status_code=status.HTTP_200_OK)
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    # person.dict() & location.dict()   # Esta sintaxis no la soporta Fast API
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This person does not exist."
        )
    return results


@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK
)
def login(username: str = Form(...), password: str = Form(...)):
    return LoginOut(username=username)


# Cookies and Headers Parameters

@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK
)
def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    last_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    email: EmailStr = Form(...),
    message: str = Form(
        ...,
        min_length=20,
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
):
    return user_agent


# Files

@app.post(
    path="/post-image"
)
def post_image(
    image: UploadFile = File(...)
):
    return {
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read())/1024, ndigits=2)
    }
