import uuid

from django.db import models


def get_uuid():
    """Get UUID for magic link."""
    return str(uuid.uuid4())


class MagicLink(models.Model):
    """
    State for passwordless authentication flow.
    """
    id = models.CharField(
        primary_key=True,
        default=get_uuid,
        max_length=36,
    )
    email = models.CharField(max_length=128)
    token = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_expired = models.DateTimeField()
