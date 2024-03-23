from django.contrib.auth.models import User
from django.db import models

from app.domain.entities.time_report import TimeReportStatus, TimeReportType


class TimestampMixin(models.Model):
    """
    A mixin for adding "created_at" and "updated_at" fields to Django models.
    """

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="%(class)s_created", null=True, editable=False
    )
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="%(class)s_updated", null=True
    )

    class Meta:
        abstract = True


# Create your models here.
class TimeReport(TimestampMixin):
    time = models.DateTimeField(auto_now_add=True, editable=True)
    type = models.CharField(
        max_length=3,
        choices=TimeReportType.choices,
        null=False,
        blank=False
    )
    status = models.CharField(
        max_length=10,
        choices=TimeReportStatus.choices,
        default=TimeReportStatus.PENDING,
    )
