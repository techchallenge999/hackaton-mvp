from django.db import models
from django.contrib.auth.models import User


class TwoFactorAuthentication(models.Model):
    code = models.CharField(max_length=6, null=False)
    issued_at = models.DateTimeField(auto_now_add=True, editable=False)
    token = models.CharField(max_length=250, null=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
