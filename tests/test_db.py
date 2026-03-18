from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.guild import Guild
from app.db.models.mod_settings import ModSettings
from app.db.services.guild_service import GuildService
from app.db.services.modsettings_service import ModSettingsService


@pytest.mark.asyncio
async def test_get_or_create_existing_guild():
    session = AsyncMock(spec=AsyncSession)

    mock_guild = MagicMock(spec=Guild)
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_guild
    session.execute.return_value = mock_result

    result = await GuildService.get_or_create(session, 123)

    assert result == mock_guild
    session.execute.assert_called_once()
    session.add.assert_not_called()


@pytest.mark.asyncio
async def test_get_or_create_new_guild():
    session = AsyncMock(spec=AsyncSession)

    mock_result_none = MagicMock()
    mock_result_none.scalar_one_or_none.return_value = None

    mock_result_mod = MagicMock()

    session.execute.side_effect = [mock_result_none, mock_result_mod]

    result = await GuildService.get_or_create(session, 123)

    assert isinstance(result, Guild)
    assert result.id == 123

    assert session.add.call_count == 1
    added_types = [type(call.args[0]) for call in session.add.call_args_list]
    assert Guild in added_types

    session.flush.assert_called_once()


@pytest.mark.asyncio
async def test_get_existing_guild_mod_conf():
    session = AsyncMock(spec=AsyncSession)

    mock_guild_conf = MagicMock(spec=ModSettings)
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_guild_conf
    session.execute.return_value = mock_result

    result = await ModSettingsService.get_guild_config(session, 123)

    assert result == mock_guild_conf
    session.execute.assert_called_once()
    session.add.assert_not_called()
