from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.api_key import require_api_key
from app.repositories.buildings import BuildingRepository
from app.schemas.buildings import BuildingRead
from app.services.buildings import BuildingService


router = APIRouter(
    prefix="/buildings",
    tags=["buildings"],
    dependencies=[Depends(require_api_key)],
)


@router.get("", response_model=list[BuildingRead])
async def list_buildings(
    session: AsyncSession = Depends(get_db),
):
    service = BuildingService(BuildingRepository(session))
    return await service.list()
