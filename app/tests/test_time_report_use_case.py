import pytest
from app.adapters.postgresql.repository.time_report import TimeReportRepository
from app.domain.use_cases.time_report.time_report import TimeReportUseCase

@pytest.mark.django_db
class TestTimeReportUseCase:
    use_case = TimeReportUseCase(TimeReportRepository())
    def test_list_usecase(self, time_report_in):
        use_case_list = self.use_case.list()
        assert time_report_in in use_case_list