from app.repositories.activities import ActivityRepository


class ActivityService:
    def __init__(self, repository: ActivityRepository) -> None:
        self.repository = repository
