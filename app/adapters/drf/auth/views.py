import logging
import re
import os
import ast
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import HttpResponse
from django.utils import timezone
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from app.adapters.drf.auth.models import TwoFactorAuthentication


User = get_user_model()
logger = logging.getLogger("auth")


class ValidateUsernamePasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        valid_username_regex = r"^[a-zA-Z.]+$"

        if not re.match(valid_username_regex, username):
            logger.error("Invalid password characters")
            return Response(
                data={
                    "message": "The user field must only contain letters and periods"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = authenticate(
            request,
            username=request.data.get("username"),
            password=request.data.get("password"),
        )

        if user is None:
            logger.error("Invalid password")
            return Response(status=status.HTTP_404_NOT_FOUND)

        self.clear_stored_2fa_data(user=user)
        logger.info("2fa data cleared")
        if not user.email:
            logger.error("User must to have an email registered")
            return Response(
                {"message": "user lacks email"}, status=status.HTTP_400_BAD_REQUEST
            )

        code = get_random_string(length=6, allowed_chars="1234567890")
        token = default_token_generator.make_token(user)

        TwoFactorAuthentication.objects.create(
            code=code,
            token=token,
            user=user,
        )
        logger.info("2FA token created")

        send_mail(
            "Your 2FA Code",
            f"Your 2FA code is: {code}. It is valid for 10 minutes.",
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        logger.info("2FA token sent")
        response = HttpResponse(status=status.HTTP_204_NO_CONTENT)
        response.set_cookie(
            "2fa-token",
            token,
            httponly=True,
            secure=True,
            max_age=ast.literal_eval(str(os.environ.get("2FA_TTL_SECONDS", 600))),
            samesite="None",
        )
        return response

    def clear_stored_2fa_data(self, user):
        stored_2fa_data = TwoFactorAuthentication.objects.filter(user=user).first()
        if stored_2fa_data:
            stored_2fa_data.delete()


class Verify2FACodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        regex = r"^\d{6}$"
        if not re.match(regex, request.data.get("code")):
            logger.error("2FA code invalid")
            return Response(
                data={"message": "2FA must be a 6 digit code"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        stored_2fa_data = self.get_stored_2fa_data(request=request)
        if not stored_2fa_data:
            logger.error("2FA code not found")
            return Response(
                data={"message": "Invalid code"}, status=status.HTTP_404_NOT_FOUND
            )

        if self.code_has_expired(stored_2fa_data=stored_2fa_data):
            stored_2fa_data.delete()
            logger.error("2FA code expired")
            return Response(
                data={"message": "Code has expired"}, status=status.HTTP_400_BAD_REQUEST
            )
        logger.info("2FA found!")
        login(request, stored_2fa_data.user)
        stored_2fa_data.delete()
        logger.info("User logged!")

        response = HttpResponse(status=status.HTTP_204_NO_CONTENT)
        response.set_cookie("2fa-token", expires=datetime.utcnow() - timedelta(days=1))
        response.set_cookie(
            "sessionid",
            request.session.session_key,
            httponly=True,
        )
        logger.info("Cookies has been set!")
        return response

    def get_stored_2fa_data(self, request):
        return TwoFactorAuthentication.objects.filter(
            code=request.data.get("code"),
            token=request.COOKIES.get("2fa-token"),
        ).first()

    def code_has_expired(self, stored_2fa_data):
        current_datetime = timezone.now()
        time_difference = (current_datetime - stored_2fa_data.issued_at).total_seconds()
        return time_difference > ast.literal_eval(str(os.environ.get("2FA_TTL_SECONDS", 600)))

    def get_auth_token_response(self, request):
        return super().post(request)


class Resend2FACodeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        stored_2fa_data = self.get_stored_2fa_data(request=request)

        if not stored_2fa_data:
            logger.error("2FA token not Found!")
            return Response(status=status.HTTP_404_NOT_FOUND)
        logger.info("2FA token found")
        send_mail(
            "Your 2FA Code",
            f"Your 2FA code is: {stored_2fa_data.code}.",
            settings.EMAIL_HOST_USER,
            [stored_2fa_data.user.email],
            fail_silently=False,
        )
        logger.info("2FA token sent!")
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_stored_2fa_data(self, request):
        return TwoFactorAuthentication.objects.filter(
            token=request.COOKIES.get("2fa-token")
        ).first()

