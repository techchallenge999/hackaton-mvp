import pytest
from django.contrib.auth.models import User

from app.adapters.drf.time_report.models import TimeReport
from app.domain.entities.time_report import TimeReportStatus, TimeReportType


@pytest.fixture
def user():
    return User.objects.create_user(
        username="john", email="john.doe@exemple.com", password="password"
    )


@pytest.fixture
def time_report_in(user):
    return TimeReport.objects.create(
        type=TimeReportType.IN,
        status=TimeReportStatus.APPROVED,
        created_by=user,
        updated_by=user,
    )


@pytest.fixture
def time_report_out(user):
    return TimeReport.objects.create(
        type=TimeReportType.OUT,
        status=TimeReportStatus.APPROVED,
        created_by=user,
        updated_by=user,
    )
