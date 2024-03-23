

from dataclasses import dataclass
from datetime import datetime

from app.domain.entities.time_report import TimeReportStatus, TimeReportType


@dataclass
class TimeReportDto:
    id: int
    time: datetime
    user: str
    type: TimeReportType
    status: TimeReportStatus


@dataclass
class UserDto:
    id: int
    username:str