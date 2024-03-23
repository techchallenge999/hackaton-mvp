from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny


schema_view = get_schema_view(
    openapi.Info(
        title="Hackaton MVP API",
        default_version="v1",
    ),
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/authentication/",
        include(
            ("app.adapters.drf.authentication.urls", "authorization"),
            namespace="authorization",
        ),
    ),
    path(
        "api/time-report/",
        include(
            ("app.adapters.drf.time_report.urls", "time-report"),
            namespace="time-report",
        ),
    ),
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=2),
        name="schema-swagger-ui",
    ),
]
