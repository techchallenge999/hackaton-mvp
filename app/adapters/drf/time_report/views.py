from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
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
    def send_monthly_dict_report_to_email(self, username: str, email: str, monthly_dict_report: dict):
        mail_subject = "Last Month Time report"
        message = render_to_string(
            "send_monthly_dict_report_to_email.html",
            {
                "username": username,
                "monthly_dict_report": monthly_dict_report,
            },
        )
        email_message = EmailMessage(
            mail_subject, message, settings.EMAIL_HOST_USER, [email]
        )
        email_message.content_subtype = "html"
        email_message.send()

    def get(self, request):
        user = request.user
        use_case = TimeReportUseCase(TimeReportRepository())
        last_month_list = use_case.list(
            filters={
                "created_by": user,
                "time__gte": get_last_month_first_days(),
                "time__lt": get_current_month_first_days(),
            },
            exclusive_filters={},
        )
        self.send_monthly_dict_report_to_email(
            username=user.username,
            email=user.email,
            monthly_dict_report= use_case.calculate_monthly_report(last_month_list)
        )
        return Response(
            {"message": "Email sent conmtaining the report"},
            status=status.HTTP_200_OK,
        )


class GetDailyReport(APIView):
    def get(self, request):
        user = request.user
        use_case = TimeReportUseCase(TimeReportRepository())
        day_report_list = use_case.list(
            filters={
                "created_by": user,
                "time__gte": get_today_first_time(),
                "time__lt": get_tomorrow_first_time(),
            },
            exclusive_filters={},
        )
        return Response(
            {"message": use_case.calculate_daily_report(day_report_list)},
            status=status.HTTP_200_OK,
        )


class CreateTimeReport(APIView):
    def post(self, request):
        time_report_type = request.GET.get("type")
        use_case = TimeReportUseCase(TimeReportRepository())
        use_case.create(time_report_type, request.user)
