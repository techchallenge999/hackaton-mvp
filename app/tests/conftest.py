
import pytest
from django.contrib.auth.models import User

from app.adapters.drf.time_report.models import TimeReport
from app.domain.entities.time_report import TimeReportStatus, TimeReportType



@pytest.fixture
def time_report_in():
    return TimeReport.objects.create(
        type=TimeReportType.IN,
        status=TimeReportStatus.APPROVED,
    )

@pytest.fixture
def time_report_out():
    return TimeReport.objects.create(
        type=TimeReportType.OUT,
        status=TimeReportStatus.APPROVED,
    )

@pytest.fixture
def user():
    return User.objects.create_user(
        username='john',
        email='john.doe@exemple.com',
        password='password'
    )