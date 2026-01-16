from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.api_key import require_api_key
from app.repositories.activities import ActivityRepository
from app.repositories.buildings import BuildingRepository
from app.repositories.organizations import OrganizationRepository
from app.schemas.organizations import OrganizationRead
from app.services.organizations import OrganizationService


router = APIRouter(
    prefix="/organizations",
    tags=["organizations"],
    dependencies=[Depends(require_api_key)],
)


@router.get("/nearby", response_model=list[OrganizationRead])
async def list_organizations_nearby(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    radius_km: float = Query(..., gt=0),
    session: AsyncSession = Depends(get_db),
):
    service = OrganizationService(
        OrganizationRepository(session),
        ActivityRepository(session),
    )
    return await service.list_nearby(latitude, longitude, radius_km)


@router.get("", response_model=list[OrganizationRead])
async def list_organizations(
    building_id: int | None = Query(default=None, ge=1),
    activity_id: int | None = Query(default=None, ge=1),
    include_descendants: bool = Query(default=True),
    name: str | None = Query(default=None, min_length=1),
    session: AsyncSession = Depends(get_db),
):
    filters = [
        building_id is not None,
        activity_id is not None,
        name is not None,
    ]
    if activity_id is None and include_descendants:
        raise HTTPException(
            status_code=400,
            detail="include_descendants requires activity_id",
        )
    if sum(filters) == 0:
        raise HTTPException(
            status_code=400,
            detail="Specify one filter: building_id, activity_id, or name",
        )
    if sum(filters) > 1:
        raise HTTPException(
            status_code=400,
            detail="Use only one filter at a time",
        )

    activity_repository = ActivityRepository(session)
    service = OrganizationService(
        OrganizationRepository(session),
        activity_repository,
    )

    if building_id is not None:
        building = await BuildingRepository(session).get(building_id)
        if building is None:
            raise HTTPException(
                status_code=404,
                detail="Building not found",
            )
        return await service.list_by_building(building_id)
    if activity_id is not None:
        activity = await activity_repository.get(activity_id)
        if activity is None:
            raise HTTPException(
                status_code=404,
                detail="Activity not found",
            )
        return await service.list_by_activity(
            activity_id, include_descendants
        )
    return await service.list_by_name(name or "")


@router.get("/{organization_id}", response_model=OrganizationRead)
async def get_organization(
    organization_id: int,
    session: AsyncSession = Depends(get_db),
):
    service = OrganizationService(
        OrganizationRepository(session),
        ActivityRepository(session),
    )
    organization = await service.get(organization_id)
    if organization is None:
        raise HTTPException(
            status_code=404,
            detail="Organization not found",
        )
    return organization
