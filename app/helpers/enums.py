from enum import Enum


class ActionType(str, Enum):
    ban = "ban"
    kick = "kick"
    mute = "timeout"
    warn = "warning"


class AppealStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    declined = "declined"


class LocaleType(str, Enum):
    user = "user"
    guild = "guild"
