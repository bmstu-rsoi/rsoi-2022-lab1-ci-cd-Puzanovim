from unittest.mock import AsyncMock

import pytest

from app.exceptions import NotFoundPerson
from app.persons.repository import PersonRepository
from app.persons.schemas import PersonBase

PERSON = PersonBase(
    name='NAME',
    age=42,
    address='MOSCOW',
    work='BMSTU',
)


@pytest.fixture
def empty_person_repo() -> AsyncMock:
    repository = AsyncMock(PersonRepository)
    repository.get_persons = AsyncMock(side_effect=NotFoundPerson)
    repository.get_person = AsyncMock(side_effect=NotFoundPerson)
    repository.create_person = AsyncMock()
    repository.update_person = AsyncMock(side_effect=NotFoundPerson)
    repository.delete_person = AsyncMock(side_effect=NotFoundPerson)
    return repository
