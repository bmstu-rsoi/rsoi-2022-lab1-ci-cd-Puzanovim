from unittest.mock import AsyncMock

import pytest as pytest

from app.persons.schemas import PersonBase
from app_tests.conftest import PERSON


@pytest.mark.parametrize('person', [PERSON])
@pytest.mark.asyncio
async def test_create_person(
    person: PersonBase,
    empty_person_repo: AsyncMock,
) -> None:

    await get_

    processor = ConfigsProcessor(empty_repo, event_sender)
    await processor.process_result(host_id, scanner_id, result)

    empty_repo.save_config.assert_awaited_once()
    empty_repo.update_config.assert_not_awaited()
    empty_repo.get_last_config.assert_not_awaited()

    empty_repo.get_standard_config.assert_awaited_once_with(host_id, scanner_id)

    saved_config = empty_repo.save_config.await_args.args[0]
    assert isinstance(saved_config, ConfigModelIn)
    assert_config_params(saved_config, host_id, scanner_id, result, True, True)

    event_sender.send_event.assert_awaited_once()
    event_sender.send_event.assert_awaited_once_with(
        event_code=1050001,
        config=ConfigForEvent(host_id=saved_config.host_id, scanner_id=saved_config.scanner_id),
        with_hostname=True,
        with_scanner_name=True,
        with_host_netbios_name=True,
        host_id=host_id,
    )