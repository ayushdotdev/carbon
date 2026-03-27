from unittest.mock import MagicMock

import pendulum

from app.utils.helpers.parse_time import parse_duration_to_timedelta


def test_parsing():
    mock_bot = MagicMock()
    mock_bot.embed_factory.error_embed.side_effect = lambda msg: f"Error: {msg}"

    # Valid cases
    d1 = parse_duration_to_timedelta(mock_bot, "5h")
    assert isinstance(d1, pendulum.Duration)
    assert d1.hours == 5

    d2 = parse_duration_to_timedelta(mock_bot, "2h30m")
    assert isinstance(d2, pendulum.Duration)
    assert d2.hours == 2
    assert d2.minutes == 30

    d3 = parse_duration_to_timedelta(mock_bot, "7days")
    assert isinstance(d3, pendulum.Duration)
    assert d3.days == 7

    d4 = parse_duration_to_timedelta(mock_bot, "1d2h")
    assert isinstance(d4, pendulum.Duration)
    assert d4.days == 1
    assert d4.hours == 2

    d5 = parse_duration_to_timedelta(mock_bot, "45m")
    assert isinstance(d5, pendulum.Duration)
    assert d5.minutes == 45

    # Invalid cases
    e1 = parse_duration_to_timedelta(mock_bot, "abc")
    assert e1 == "Error: Invalid duration format"

    e2 = parse_duration_to_timedelta(mock_bot, "5z")
    assert e2 == "Error: Invalid duration format"

    e3 = parse_duration_to_timedelta(mock_bot, "")
    assert e3 == "Error: Invalid duration format"
