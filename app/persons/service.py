from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.persons.repository import PersonRepository
from app.persons.schemas import PersonModel, PersonBase, UpdatePerson


async def get_persons(db: AsyncSession, repo: PersonRepository) -> List[PersonModel]:
    return await repo.get_persons(db)


async def get_person(person_id: int, db: AsyncSession, repo: PersonRepository) -> PersonModel:
    return await repo.get_person(person_id, db)


async def create_person(person: PersonBase, db: AsyncSession, repo: PersonRepository) -> PersonModel:
    return await repo.create_person(person, db)


async def update_person(person_id: int, person: UpdatePerson, db: AsyncSession, repo: PersonRepository) -> PersonModel:
    return await repo.update_person(person_id, person, db)


async def delete_person(person_id: int, db: AsyncSession, repo: PersonRepository) -> None:
    await repo.delete_person(person_id, db)
