import pytest

from app.persons.repository import PersonRepository
from app.persons.schemas import PersonBase


@pytest.fixture
def test_repo() -> PersonRepository:
    return PersonRepository()


FULL_PERSON = PersonBase(
    name='NAME',
    age=42,
    address='Moscow',
)


INCOMPLETE_PERSON = PersonBase(
    name='NAME',
    age=14,
)


JUST_NAME_PERSON = PersonBase(
    name='NAME',
)


def compare_two_person(first_person: PersonBase, second_person: PersonBase) -> None:
    assert first_person.name == second_person.name
    assert first_person.age == second_person.age
    assert first_person.address == second_person.address
    assert first_person.work == second_person.work
