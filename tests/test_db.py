from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.appeal_settings import AppealSettings
from app.db.models.guild import Guild
from app.db.models.mod_settings import ModSettings


@pytest.mark.asyncio
async def test_get_or_create_existing_guild():
    # Mock session
    session = AsyncMock(spec=AsyncSession)

    # Mock result from session.execute
    mock_guild = MagicMock(spec=Guild)
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_guild
    session.execute.return_value = mock_result

    result = await Guild.get_or_create(session, 123)

    assert result == mock_guild
    session.execute.assert_called_once()
    session.add.assert_not_called()


@pytest.mark.asyncio
async def test_get_or_create_new_guild():
    # Mock session
    session = AsyncMock(spec=AsyncSession)

    # First execute (get guild) returns None
    # Second execute (after creation) can return anything as it's not strictly used in the return
    mock_result_none = MagicMock()
    mock_result_none.scalar_one_or_none.return_value = None

    mock_result_mod = MagicMock()

    session.execute.side_effect = [mock_result_none, mock_result_mod]

    result = await Guild.get_or_create(session, 123)

    assert isinstance(result, Guild)
    assert result.id == 123

    # Check if guild, mod_settings, and appeal_settings were added
    assert session.add.call_count == 3
    added_types = [type(call.args[0]) for call in session.add.call_args_list]
    assert Guild in added_types
    assert ModSettings in added_types
    assert AppealSettings in added_types

    session.flush.assert_called_once()
