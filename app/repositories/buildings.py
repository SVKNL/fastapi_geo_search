from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.building import Building


class BuildingRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, building_id: int) -> Building | None:
        result = await self.session.execute(
            select(Building).where(Building.id == building_id)
        )
        return result.scalars().first()

    async def list(self) -> list[Building]:
        result = await self.session.execute(select(Building))
        return result.scalars().all()
