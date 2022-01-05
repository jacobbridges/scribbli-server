from django.db import models


class PreSignUp(models.Model):
    """
    Tracks Scribbli signups before the service was available.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=100, unique=True)
