from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from app.models.activity import Activity


class ActivityRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, activity_id: int) -> Activity | None:
        result = await self.session.execute(
            select(Activity).where(Activity.id == activity_id)
        )
        return result.scalars().first()

    async def get_descendant_ids(self, activity_id: int) -> list[int]:
        activity_cte = (
            select(Activity.id, Activity.parent_id)
            .where(Activity.id == activity_id)
            .cte(recursive=True)
        )
        activity_alias = aliased(Activity)
        activity_cte = activity_cte.union_all(
            select(activity_alias.id, activity_alias.parent_id).where(
                activity_alias.parent_id == activity_cte.c.id
            )
        )
        result = await self.session.execute(select(activity_cte.c.id))
        return [row[0] for row in result]
