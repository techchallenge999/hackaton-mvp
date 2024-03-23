from django.urls import path

from app.adapters.drf.authentication.views import (
    Resend2FACodeView,
    ValidateUsernamePasswordView,
    Verify2FACodeView,
)


namespace = "time-report"

urlpatterns = [
    path("login/", ValidateUsernamePasswordView.as_view(), name="login"),
    path("verify-2fa-code/", Verify2FACodeView.as_view(), name="verify_2fa_code"),
    path("resend-2fa-code/", Resend2FACodeView.as_view(), name="resend_2fa_code"),
]
