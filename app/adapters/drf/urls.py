from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/authorization/", include(("app.adapters.drf.authorization.urls", "authorization"), namespace="authorization")),
    path("api/time-report/", include(("app.adapters.drf.time_report.urls", "time-report"), namespace="time-report")),
]
