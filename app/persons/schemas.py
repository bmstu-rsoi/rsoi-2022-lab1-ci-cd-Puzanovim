from pydantic import BaseModel


class PersonBase(BaseModel):
    name: str
    age: int | None
    address: str | None
    work: str | None


class PersonModel(PersonBase):
    id: int

    class Config:
        orm_mode = True


class UpdatePerson(PersonBase):
    name: str | None
