from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.case_logs import CaseLog
from app.utils.confs.enums import ActionType


class CaseLogService:
    @staticmethod
    async def create_new_case(
        session: AsyncSession,
        guild_id: int,
        target_id: int,
        moderator_id: int,
        action_type: ActionType,
        reason: str,
        duration: int = 0,
    ) -> int:
        case = CaseLog(
            guild_id=guild_id,
            target_id=target_id,
            moderator_id=moderator_id,
            action_type=action_type,
            reason=reason,
            duration=duration,
        )
        session.add(case)

        await session.flush()
        return case.case_id
