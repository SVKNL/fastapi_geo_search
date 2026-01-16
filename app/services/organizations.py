from app.repositories.activities import ActivityRepository
from app.repositories.organizations import OrganizationRepository


class OrganizationService:
    def __init__(
        self,
        organization_repository: OrganizationRepository,
        activity_repository: ActivityRepository,
    ) -> None:
        self.organization_repository = organization_repository
        self.activity_repository = activity_repository

    async def get(self, organization_id: int):
        return await self.organization_repository.get(organization_id)

    async def list_by_building(self, building_id: int):
        return await self.organization_repository.list_by_building(building_id)

    async def list_by_name(self, name: str):
        return await self.organization_repository.list_by_name(name)

    async def list_by_activity(
        self, activity_id: int, include_descendants: bool
    ):
        if include_descendants:
            activity_ids = await self.activity_repository.get_descendant_ids(
                activity_id
            )
        else:
            activity_ids = [activity_id]
        if not activity_ids:
            return []
        return await self.organization_repository.list_by_activity_ids(
            activity_ids
        )

    async def list_nearby(
        self, latitude: float, longitude: float, radius_km: float
    ):
        return await self.organization_repository.list_nearby(
            latitude, longitude, radius_km
        )
