from typing import List

import pytest

from app.db import async_session, engine
from app.persons.models import Base
from app.persons.repository import PersonRepository
from app.persons.schemas import PersonBase, PersonModel
from app.persons.service import (create_person, delete_person, get_person,
                                 get_persons)
from app_tests.conftest import (FULL_PERSON, INCOMPLETE_PERSON,
                                JUST_NAME_PERSON, compare_two_person)


@pytest.mark.asyncio
@pytest.mark.parametrize('new_person', [FULL_PERSON, INCOMPLETE_PERSON, JUST_NAME_PERSON])
async def test_get_person(new_person: PersonBase, test_repo: PersonRepository) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as db:
        created_person: PersonModel = await create_person(new_person, db, test_repo)

    compare_two_person(created_person, new_person)

    async with async_session() as db:
        person: PersonModel = await get_person(created_person.id, db, test_repo)

    assert person.id == created_person.id
    compare_two_person(person, created_person)

    async with async_session() as db:
        await delete_person(created_person.id, db, test_repo)


@pytest.mark.asyncio
@pytest.mark.parametrize('new_person', [FULL_PERSON, INCOMPLETE_PERSON, JUST_NAME_PERSON])
async def test_get_persons(new_person: PersonBase, test_repo: PersonRepository) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as db:
        first_person: PersonModel = await create_person(new_person, db, test_repo)
        second_person: PersonModel = await create_person(new_person, db, test_repo)

    assert first_person.id != second_person.id
    compare_two_person(first_person, second_person)

    created_persons = [first_person, second_person]

    async with async_session() as db:
        persons: List[PersonModel] = await get_persons(db, test_repo)

    assert len(persons) == len(created_persons)
    for first_person, second_person in zip(persons, created_persons):
        compare_two_person(first_person, second_person)

    async with async_session() as db:
        for person in created_persons:
            await delete_person(person.id, db, test_repo)
