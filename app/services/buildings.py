from app.repositories.buildings import BuildingRepository


class BuildingService:
    def __init__(self, repository: BuildingRepository) -> None:
        self.repository = repository

    async def list(self):
        return await self.repository.list()
