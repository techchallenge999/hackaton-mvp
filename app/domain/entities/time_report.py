from enum import Enum


class TimeReportStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

    @classmethod
    def get_choice_by_value(cls, value: str):
        for i in cls:
            if i.value == value:
                return (i.name, i.value)
        raise ValueError(f"TimeReport Status {value} not found")

    @classmethod
    @property
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class TimeReportType(Enum):
    IN = "in"
    OUT = "out"

    @classmethod
    def get_choice_by_value(cls, value: str):
        for i in cls:
            if i.value == value:
                return (i.name, i.value)
        raise ValueError(f"TimeReport Type {value} not found")

    @classmethod
    @property
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
