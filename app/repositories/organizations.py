from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.activity import Activity
from app.models.building import Building
from app.models.organization import Organization


class OrganizationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def _base_stmt(self):
        return select(Organization).options(
            selectinload(Organization.building),
            selectinload(Organization.phones),
            selectinload(Organization.activities),
        )

    async def get(self, organization_id: int) -> Organization | None:
        stmt = self._base_stmt().where(Organization.id == organization_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def list_by_building(self, building_id: int) -> list[Organization]:
        stmt = self._base_stmt().where(Organization.building_id == building_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def list_by_name(self, name: str) -> list[Organization]:
        stmt = self._base_stmt().where(Organization.name.ilike(f"%{name}%"))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def list_by_activity_ids(
        self, activity_ids: list[int]
    ) -> list[Organization]:
        stmt = (
            self._base_stmt()
            .join(Organization.activities)
            .where(Activity.id.in_(activity_ids))
            .distinct()
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def list_nearby(
        self, latitude: float, longitude: float, radius_km: float
    ) -> list[Organization]:
        distance_expr = self._distance_expr(latitude, longitude)
        stmt = (
            self._base_stmt()
            .join(Organization.building)
            .where(distance_expr <= radius_km)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    def _distance_expr(self, latitude: float, longitude: float):
        earth_radius_km = 6371.0
        lat_rad = func.radians(latitude)
        lon_rad = func.radians(longitude)
        return earth_radius_km * func.acos(
            func.cos(lat_rad)
            * func.cos(func.radians(Building.latitude))
            * func.cos(func.radians(Building.longitude) - lon_rad)
            + func.sin(lat_rad) * func.sin(func.radians(Building.latitude))
        )
