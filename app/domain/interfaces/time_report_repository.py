from abc import abstractmethod
from app.domain.entities.time_report import TimeReportStatus
from app.domain.interfaces.base_repository import RepositoryInterface
from app.domain.interfaces.dtos import TimeReportDto


class TimeReportRepositoryInterface(RepositoryInterface):
    @abstractmethod
    def create(self, type: str, user, status: TimeReportStatus) -> None:
        pass

    @abstractmethod
    def find(self, id: str) -> TimeReportDto | None:
        pass

    @abstractmethod
    def list(
        self, filters: dict = {}, exclusive_filters: dict = {}
    ) -> list[TimeReportDto]:
        pass

    @abstractmethod
    def update(self, update_time_report_dto: TimeReportDto, user) -> None:
        pass

    @abstractmethod
    def delete(self, id: str) -> None:
        pass

    @abstractmethod
    def get_last_time_report(self, user) -> TimeReportDto | None:
        pass
