from django.db import models

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import EmailValidator

from scribbli.models.mixins import GeneralPurposeModelMixin


class User(PermissionsMixin, AbstractBaseUser, GeneralPurposeModelMixin):
    """
    Table contains cognito-users & django-users.

    PermissionsMixin leverage built-in django model permissions system
    (which allows to limit information for staff users via Groups).
    """
    username_validator = UnicodeUsernameValidator()
    email_validator = EmailValidator()

    ### Common fields
    email = models.EmailField(unique=True, validators=[email_validator])
    username = models.CharField(max_length=60, blank=True, validators=[username_validator])

    ### Django-user related fields
    # password is inherited from AbstractBaseUser
    is_staff = models.BooleanField(
        default=False,
        help_text='Designates whether the user can log into the admin site.'
    )

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']  # used only on createsuperuser
