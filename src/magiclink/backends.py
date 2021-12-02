from typing import Optional

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.http import HttpRequest
from django.utils.timezone import now

from magiclink.exceptions import (
    MagicLinkMissingRequiredParamsError,
    MagicLinkExpiredError,
    MagicLinkNotFoundError,
    MagicLinkForDeactivatedUserError,
)
from magiclink.models import MagicLink


class MagicLinkBackend(BaseBackend):
    
    @property
    def user_model(self):
        return get_user_model()
    
    def get_user(self, user_id):
        return self.user_model.objects.filter(id=user_id).first()

    def authenticate(
        self, 
        request: HttpRequest, 
        token: Optional[str] = None, 
        email: Optional[str] = None
    ):

        if not token or not email:
            raise MagicLinkMissingRequiredParamsError(
                f"Missing the following MagicLink authentication parameters: "
                f"{'token' if not token else ''} "
                f"{'email' if not email else ''}"
            )

        email = email.lower()

        try:
            ml = MagicLink.objects.get(
                email=email,
                token=token,
            )
        except MagicLink.DoesNotExist:
            raise MagicLinkNotFoundError(
                f"Could not find MagicLink for email={email}, token={token}"
            )

        if not ml.is_active:
            raise MagicLinkExpiredError(
                f"{ml} is inactive"
            )

        if ml.date_expired < now():
            ml.is_active = False
            ml.save()
            raise MagicLinkExpiredError(
                f"{ml} is expired"
            )

        try:
            user = self.user_model.objects.get(email=email)
            
            if not user.is_active:
                raise MagicLinkForDeactivatedUserError(
                    f"{user} related to {ml} is deactivated"
                )
        except self.user_model.DoesNotExist:
            user = self.user_model.objects.create(email=email)

        return user
