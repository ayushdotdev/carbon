import pytest
from unittest.mock import MagicMock
import discord
from app.i18n.manager import I18nManager
from app.i18n.context import ExecutionContext
from app.utils.confs.enums import LocaleType


@pytest.fixture
def i18n_manager():
    return I18nManager()


def test_resolve_locale_with_explicit_locale(i18n_manager):
    locale = discord.Locale.british_english
    assert i18n_manager._resolve_locale(locale, LocaleType.USER) == "en-GB"


def test_resolve_locale_with_context_user(i18n_manager):
    ctx = ExecutionContext(
        user_locale=discord.Locale.french, guild_locale=discord.Locale.german
    )
    ExecutionContext.set(ctx)
    assert i18n_manager._resolve_locale(None, LocaleType.USER) == "fr"


def test_resolve_locale_with_context_guild(i18n_manager):
    ctx = ExecutionContext(
        user_locale=discord.Locale.french, guild_locale=discord.Locale.german
    )
    ExecutionContext.set(ctx)
    assert i18n_manager._resolve_locale(None, LocaleType.GUILD) == "de"


def test_resolve_locale_default(i18n_manager):
    ExecutionContext.set(None)
    assert i18n_manager._resolve_locale(None, LocaleType.USER) == "en"


def test_gettext_interpolation(i18n_manager):
    # Mock _get_translation to return a mock translation object
    mock_tr = MagicMock()
    mock_tr.gettext.return_value = "Hello %(name)s"
    i18n_manager._get_translation = MagicMock(return_value=mock_tr)

    result = i18n_manager.gettext("Hello %(name)s", name="World")
    assert result == "Hello World"
    mock_tr.gettext.assert_called_with("Hello %(name)s")


def test_ngettext_interpolation(i18n_manager):
    mock_tr = MagicMock()
    mock_tr.ngettext.return_value = "%(n)d items"
    i18n_manager._get_translation = MagicMock(return_value=mock_tr)

    result = i18n_manager.ngettext("%(n)d item", "%(n)d items", 5, n=5)
    assert result == "5 items"
    mock_tr.ngettext.assert_called_with("%(n)d item", "%(n)d items", 5)
