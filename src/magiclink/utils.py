import binascii
import os
import uuid
from datetime import timedelta
from urllib.parse import urlencode, urljoin

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.timezone import now

from magiclink.exceptions import (
    MagicLinkNotFoundError,
    MagicLinkExpiredError,
)
from magiclink.models import MagicLink


def generate_token():
    """Generate token for magic link."""
    return binascii.hexlify(os.urandom(22)).decode()


def generate_magic_link(email: str):
    """Generate new MagicLink instance."""
    return MagicLink.objects.create(
        email=email.lower(),
        token=generate_token(),
        date_expired=now() + timedelta(days=1),
    )


def get_url(magic_link: MagicLink):
    """Get auth redirect url for a given MagicLink instance."""
    # TODO: Make more generic (not specific for scribb.li)
    querystring = urlencode({
        "token": magic_link.token,
        "email": magic_link.email,
    })
    protocol = "https"
    domain = "scribb.li"
    path = f"login-magic-link?{querystring}"
    return urljoin(f"{protocol}://{domain}", path)


def send_magic_link(magic_link: MagicLink):
    """Send a magic link email with a link to initiate passwordless login."""
    # TODO: Make more generic (not specific for scribb.li)
    email_content = render_to_string("emails/magic-link.html", {
        "url": get_url(magic_link),
    })
    send_mail(
        "Scribbli Passwordless Login",
        email_content,
        "void@scribb.li",
        [magic_link.email],
        html_message=email_content,
    )


def verify_magic_link(token: str, email: str) -> bool:
    """Verify a magic link."""
    try:
        ml = MagicLink.objects.get(
            email=email.lower(),
            token=token,
            is_active=True,
        )
    except MagicLink.DoesNotExist:
        raise MagicLinkNotFoundError(
            f"No MagicLink could be found for email {email} and token {token}."
        )
    
    if ml.date_expired < now():
        ml.is_active = False
        ml.save()
        raise MagicLinkExpiredError(
            f"MagicLink for email {email} and token {token} is expired."
        )

    return True
