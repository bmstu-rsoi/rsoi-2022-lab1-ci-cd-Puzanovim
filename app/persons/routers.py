from typing import List

from fastapi import APIRouter, status, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import async_db_session
from app.persons.repository import PersonRepository
from app.persons.schemas import PersonModel, PersonBase, UpdatePerson
from app.persons.service import delete_person, update_person, get_persons, get_person, create_person

router = APIRouter()
person_repository = PersonRepository()


@router.get('', status_code=status.HTTP_200_OK, response_model=List[PersonModel])
async def list_persons(db: AsyncSession = Depends(async_db_session)) -> List[PersonModel]:
    return await get_persons(db, person_repository)


@router.get('/{person_id}', status_code=status.HTTP_200_OK, response_model=PersonModel)
async def get_person_by_id(person_id: int, db: AsyncSession = Depends(async_db_session)) -> PersonModel:
    return await get_person(person_id, db, person_repository)


@router.post('', status_code=status.HTTP_201_CREATED)
async def create_new_person(person: PersonBase, db: AsyncSession = Depends(async_db_session)) -> Response:
    new_person: PersonModel = await create_person(person, db, person_repository)
    return Response(status_code=status.HTTP_201_CREATED, headers={'Location': f'/api/v1/persons/{new_person.id}'})


@router.patch('/{person_id}', status_code=status.HTTP_200_OK, response_model=PersonModel)
async def edit_person(
        person_id: int, person: UpdatePerson, db: AsyncSession = Depends(async_db_session)
) -> PersonModel:
    return await update_person(person_id, person, db, person_repository)


@router.delete('/{person_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_person_by_id(person_id: int, db: AsyncSession = Depends(async_db_session)) -> None:
    await delete_person(person_id, db, person_repository)
