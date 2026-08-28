from app.db.models.github.revenueSummary import RevenueSummary
from app.repositories.github.base import BaseRepository


class RevenueSummaryRepository(
    BaseRepository[RevenueSummary]
):

    def __init__(self):

        super().__init__(RevenueSummary)


revenueSummaryRepository = RevenueSummaryRepository()