from enum import Enum


class ActionType(str, Enum):
    ban = "ban"
    kick = "kick"
    mute = "timeout"
    warn = "warning"
