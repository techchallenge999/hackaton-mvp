from typing import List
from app.domain.entities.time_report import TimeReportStatus, TimeReportType
from app.domain.interfaces.dtos import TimeReportDto
from app.domain.interfaces.time_report_repository import TimeReportRepositoryInterface


class TimeReportUseCase:
    def __init__(
        self,
        time_report_repository: TimeReportRepositoryInterface,
    ):
        self.time_report_repository = time_report_repository

    def create(self, type:str, user):
        time_report_type = TimeReportType.get_choice_by_value(type)
        last_time_report = self.time_report_repository.get_last_time_report()
        if last_time_report is not None and last_time_report.type == time_report_type:
            raise ValueError("You can't set the same time report type twice in a roll")
        elif last_time_report is None and time_report_type != TimeReportType.IN:
            raise ValueError("You can't set a out time report without a in")
        self.time_report_repository.create(
            type=type, status=TimeReportStatus.APPROVED.value, user=user
        )


    def list(self, filters: dict, exclusive_filters: dict):
        return self.time_report_repository.list(
            filters=filters,
            exclusive_filters=exclusive_filters,
        )

    def find(self, id: str):
        return self.time_report_repository.find(id=id)

    def delete(self, id: str):
        self.time_report_repository.delete(id=id)

    def update(self, update_data: TimeReportDto, user):
        self.time_report_repository.update(
            update_time_report_dto=update_data, user=user
        )

    def calculate_daily_report(self, daily_report_list: List[TimeReportDto]):
        worked_time = 0.0
        for i in range(1,len(daily_report_list), 2):
            worked_time += (
                daily_report_list[i].time - daily_report_list[i-1].time
            ).total_seconds()
        return {
            "entries": daily_report_list,
            "worked_time": f"{worked_time} seconds",
        }

    def calculate_monthly_report(self, monthly_report_list: List[TimeReportDto]):
        month_dict = {}
        for i in range(1,len(monthly_report_list), 2):
            day = monthly_report_list[i-1].time.day
            if day not in month_dict.keys():
                month_dict[day] = {
                    "worked_time": 0.0,
                    "entries": [],
                }
            month_dict[day]["worked_time"] += (monthly_report_list[i].time - monthly_report_list[i-1].time).total_seconds()
            month_dict[day]["entries"].extend([monthly_report_list[i], monthly_report_list[i-1]])

        for day in month_dict.keys():
            month_dict[day]["worked_time"] = f'{month_dict[day]["worked_time"]} seconds'
        return month_dict

