from django.urls import path

from app.adapters.drf.time_report.views import CreateTimeReport, GetDailyReport, GetLastMonthReport

namespace = "time-report"

urlpatterns = [
    path("get-last-month/", GetLastMonthReport.as_view(), name="Get Last Month Time Report"),
    path("get-daily-month/", GetDailyReport.as_view(), name="Get Today's Time Report"),
    path("create-time-report/", CreateTimeReport.as_view(), name="Create a new Time Report"),
]