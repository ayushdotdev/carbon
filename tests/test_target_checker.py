from unittest.mock import Mock

import discord
import pytest

from app.utils.helpers.check_target import TargetChecker


@pytest.fixture
def mock_bot():
    bot = Mock()
    bot.embed_factory.error_embed.side_effect = lambda msg: msg
    return bot


@pytest.fixture
def mock_interaction():
    interaction = Mock(spec=discord.Interaction)
    interaction.guild = Mock(spec=discord.Guild)
    interaction.user = Mock(spec=discord.Member)
    interaction.guild.me = Mock(spec=discord.Member)
    return interaction


@pytest.fixture
def mock_target():
    return Mock(spec=discord.Member)


def test_validate_target_is_client(mock_bot, mock_interaction, mock_target):
    mock_target.id = 123
    mock_interaction.guild.me.id = 123
    checker = TargetChecker(mock_bot, mock_interaction, mock_target)

    result = checker.validate()
    assert result == "This action cannot be performed."


def test_validate_target_is_owner(mock_bot, mock_interaction, mock_target):
    mock_target.id = 456
    mock_interaction.guild.owner_id = 456
    mock_interaction.guild.me.id = 123
    checker = TargetChecker(mock_bot, mock_interaction, mock_target)

    result = checker.validate()
    assert result == "The server owner cannot be targeted."


def test_validate_role_hierarchy_bot_lower(mock_bot, mock_interaction, mock_target):
    mock_target.id = 1
    mock_interaction.user.id = 2
    mock_interaction.guild.me.id = 3
    mock_interaction.guild.owner_id = 4

    mock_target.top_role.position = 10
    mock_interaction.guild.me.top_role.position = 5
    mock_interaction.user.top_role.position = 15

    checker = TargetChecker(mock_bot, mock_interaction, mock_target)
    result = checker.validate()
    assert result == "My role must be higher than the target's role."


def test_validate_role_hierarchy_author_lower(mock_bot, mock_interaction, mock_target):
    mock_target.id = 1
    mock_interaction.user.id = 2
    mock_interaction.guild.me.id = 3
    mock_interaction.guild.owner_id = 4

    # Mock role positions
    mock_target.top_role.position = 10
    mock_interaction.guild.me.top_role.position = 15
    mock_interaction.user.top_role.position = 5

    checker = TargetChecker(mock_bot, mock_interaction, mock_target)
    result = checker.validate()
    assert result == "Your role must be higher than the target's role."


def test_validate_success(mock_bot, mock_interaction, mock_target):
    mock_target.id = 1
    mock_interaction.user.id = 2
    mock_interaction.guild.me.id = 3
    mock_interaction.guild.owner_id = 4

    # Mock role positions
    mock_target.top_role.position = 5
    mock_interaction.guild.me.top_role.position = 15
    mock_interaction.user.top_role.position = 10

    checker = TargetChecker(mock_bot, mock_interaction, mock_target)
    result = checker.validate()
    assert result is None
