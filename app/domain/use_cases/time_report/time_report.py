
from app.domain.entities.time_report import TimeReportStatus
from app.domain.interfaces.dtos import TimeReportDto
from app.domain.interfaces.time_report_repository import TimeReportRepositoryInterface


class TimeReportUseCase:
    def __init__(
        self,
        time_report_repository: TimeReportRepositoryInterface,
    ):
        self.time_report_repository = time_report_repository

    def create(self):
        self.time_report_repository.create(type=TimeReportStatus.APPROVED.value)

    def list(self, filters: dict, exclusive_filters: dict):
        return self.time_report_repository.list(
            filters=filters,
            exclusive_filters=exclusive_filters,
        )

    def find(self, id:str):
        return self.time_report_repository.find(id=id)

    def delete(self, id:str):
        self.time_report_repository.delete(id=id)

    def update(self, update_data: TimeReportDto):
        self.time_report_repository.update(update_time_report_dto=update_data)
