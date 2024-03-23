from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.adapters.postgresql.repository.time_report import TimeReportRepository
from app.domain.use_cases.time_report.time_report import TimeReportUseCase
from app.domain.utils import (
    get_current_month_first_days,
    get_last_month_first_days,
    get_tomorrow_first_time,
    get_today_first_time
)


class GetLastMonthReport(APIView):
    def get(self, request):
        user = request.user
        use_case = TimeReportUseCase(TimeReportRepository())
        use_case.list(
            filters={
                "created_by": user,
                "time__gte": get_last_month_first_days(),
                "time__lt": get_current_month_first_days(),
            },
            exclusive_filters={},
        )


class GetDailyReport(APIView):
    def get(self, request):
        user = request.user
        use_case = TimeReportUseCase(TimeReportRepository())
        use_case.list(
            filters={
                "created_by": user,
                "time__gte": get_today_first_time(),
                "time__lt": get_tomorrow_first_time(),
            },
            exclusive_filters={},
        )


class CreateTimeReport(APIView):
    def post(self, request):
        use_case = TimeReportUseCase(TimeReportRepository())
        use_case.create()
