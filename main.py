# Python
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel, Field
from pydantic import EmailStr, HttpUrl


# FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

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


class Person(BaseModel):
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


@app.get('/')
def home():
    return {"Hello": "World"}

# Request and response body


@app.post('/person/new')
def create_person(person: Person = Body(...)):
    return person

# Validaciones queries parameters


@app.get('/person/detail')
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title="Peron Name",
        description="This is the person name. It's between 1 and 50 charachters."
    ),
    age: str = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's required"
    )
):
    return {name: age}

# Vlidaciones: Path Parameters


@app.get('/person/detail/{person_id}')
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


@app.put("/person/{person_id}")
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
    return results
