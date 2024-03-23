from django.contrib.auth.models import User

from app.adapters.drf.time_report.models import TimeReport
from app.domain.interfaces.dtos import TimeReportDto, TimeReportType
from app.domain.interfaces.time_report_repository import TimeReportRepositoryInterface


class TimeReportRepository(TimeReportRepositoryInterface):

    def create(self, type: str, user: User) -> None:
        TimeReport.objects.create(
            type=TimeReportType.get_choice_by_value(type),
            created_by=user,
            updated_by=user,
        )

    def get_last_time_report(self, user) -> TimeReportDto | None:
        last_time_report = TimeReport.objects.filter(created_by=user).order_by('-time').first()
        if last_time_report is not None:
            return TimeReportDto(
                id=last_time_report.pk,
                time=last_time_report.created_at,
                user=last_time_report.created_by.username,
                type=last_time_report.status,
                status=last_time_report.status,
            )
        return None

    def find(self, id: str) -> TimeReportDto | None:
        record = TimeReport.objects.filter(pk=id).first()
        if record is not None:
            return TimeReportDto(
                id=record.pk,
                time=record.created_at,
                user=record.created_by.username,
                type=record.status,
                status=record.status,
            )


    def list(
        self, filters: dict = {}, exclusive_filters: dict = {}
    ) -> list[TimeReportDto]:
        queryset = TimeReport.objects
        if filters:
            queryset = queryset.filter(**filters)
        if exclusive_filters:
            queryset = queryset.exclude(**exclusive_filters)
        records = queryset.order_by("-time").all()
        return [
            TimeReportDto(
                id=record.pk,
                time=record.created_at,
                user=record.created_by.username,
                type=record.status,
                status=record.status,
            ) for record in records if record
        ]


    def update(self, update_time_report_dto: TimeReportDto, user: User) -> None:
        pk = update_time_report_dto.id
        record = TimeReport.objects.filter(pk=pk).first()
        if record is None:
            raise ValueError(f"Report {id} not found!")
        record.time = update_time_report_dto.time
        record.type = update_time_report_dto.type
        record.status = update_time_report_dto.status
        record.updated_by = user
        record.save()

    def delete(self, id: str) -> None:
        record = TimeReport.objects.filter(pk=id).first()
        if record is None:
            raise ValueError(f"Report {id} not found!")
        record.delete()
