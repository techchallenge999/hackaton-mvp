import pytest
from app.adapters.postgresql.repository.time_report import TimeReportRepository
from app.domain.use_cases.time_report.time_report import TimeReportUseCase
from dotenv import load_dotenv


load_dotenv()

@pytest.mark.django_db
class TestTimeReportUseCase:
    use_case = TimeReportUseCase(TimeReportRepository())
    def test_list_usecase(self, time_report_in, time_report_out):
        use_case_list = self.use_case.list({}, {})
        assert time_report_in.pk in [time_report.id for time_report in use_case_list]
        assert time_report_out.pk in [time_report.id for time_report in use_case_list]