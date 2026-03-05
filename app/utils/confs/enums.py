from enum import Enum


class ActionType(str, Enum):
    BAN = "ban"
    KICK = "kick"
    TIMEOUT = "timeout"
    WARN = "warning"


class AppealStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    DECLINED = "declined"


class LocaleType(str, Enum):
    USER = "user"
    GUILD = "guild"
