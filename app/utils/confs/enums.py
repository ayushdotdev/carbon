from enum import Enum, StrEnum

from app.i18n.marker import _
from app.utils.consts.branding import GRAY, GREEN, ORANGE, RED, YELLOW


class ActionType(StrEnum):
    BAN = "ban"
    KICK = "kick"
    TIMEOUT = "timeout"
    WARN = "warning"


class AppealStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    DECLINED = "declined"


class LocaleType(StrEnum):
    USER = "user"
    GUILD = "guild"


class ModLogAction(Enum):
    KICK = (_("Member Kicked"), ORANGE, _("You were kicked"))
    BAN = (_("Member Banned"), RED, _("You were banned"))
    WARN = (_("Member Warned"), YELLOW, _("You were warned."))
    TIMEOUT = (_("Member Timed Out"), YELLOW, _("You were timed out."))
    WARN_REMOVE = (_("Warning Removed"), GREEN)
    PURGE = (_("Messages Purged"), GRAY)
    UNBAN = (_("Member Unbanned"), GREEN)

    def __init__(self, title: str, color: int, dm_title: str | None = None) -> None:
        self.title = title
        self.color = color
        self.dm_title = dm_title
