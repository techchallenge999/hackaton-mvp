"""
URL configuration for drf project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from app.adapters.drf.auth.views import Resend2FACodeView, ValidateUsernamePasswordView, Verify2FACodeView

urlpatterns = [
    path("login/", ValidateUsernamePasswordView.as_view(), name="login"),
    path("verify-2fa-code/", Verify2FACodeView.as_view(), name="verify_2fa_code"),
    path("resend-2fa-code/", Resend2FACodeView.as_view(), name="resend_2fa_code"),
    path('admin/', admin.site.urls),
    path("api/time-report/", include(("time_report.urls", "time-report"), namespace="time-report")),
]
