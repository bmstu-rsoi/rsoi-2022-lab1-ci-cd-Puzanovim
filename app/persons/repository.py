from typing import List

from sqlalchemy import delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.exceptions import NotFoundPerson
from app.persons.models import Person
from app.persons.schemas import PersonBase, PersonModel, UpdatePerson


class PersonRepository:
    async def get_persons(self, db: AsyncSession) -> List[PersonModel]:
        async with db.begin():
            result = await db.execute(select(Person))

        persons: List[Person] = result.scalars().all()
        return [PersonModel.from_orm(person) for person in persons]

    async def get_person(self, person_id: int, db: AsyncSession) -> PersonModel:
        query = select(Person).where(Person.id == person_id)

        async with db.begin():
            result = await db.execute(query)

        try:
            person: Person = result.scalar_one()
        except NoResultFound:
            raise NotFoundPerson

        return PersonModel.from_orm(person)

    async def create_person(self, person: PersonBase, db: AsyncSession) -> PersonModel:
        new_person = Person(**person.dict())

        async with db.begin():
            db.add(new_person)
            await db.flush()
            await db.refresh(new_person)

        return PersonModel.from_orm(new_person)

    async def update_person(self, person_id: int, person: UpdatePerson, db: AsyncSession) -> PersonModel:
        async with db.begin():
            result = await db.execute(select(Person).where(Person.id == person_id).with_for_update())

            try:
                updated_person: Person = result.scalar_one()
            except NoResultFound:
                raise NotFoundPerson

            for key, value in person.dict(exclude_unset=True).items():
                if hasattr(updated_person, key):
                    setattr(updated_person, key, value)

            await db.flush()
            await db.refresh(updated_person)

        return PersonModel.from_orm(updated_person)

    async def delete_person(self, person_id: int, db: AsyncSession) -> None:
        await self.get_person(person_id, db)
        async with db.begin():
            await db.execute(delete(Person).where(Person.id == person_id))
