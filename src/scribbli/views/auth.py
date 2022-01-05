from __future__ import annotations

import logging
import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import HttpRequest, JsonResponse

from graphene_django.views import GraphQLView

from magiclink.utils import (
    generate_magic_link,
    send_magic_link,
    verify_magic_link,
)
from scribbli.enums import JSON_CONTENT_TYPES
from scribbli.utils import is_email

devlog = logging.getLogger("dev")
applog = logging.getLogger("app")


class PrivateGraphQLView(LoginRequiredMixin, GraphQLView):
    pass


class MagicLinkCreateView(View):
    """Request a new magic link be sent to the given email."""

    def post(self, request: HttpRequest):
        data = self.get_data(request)
        is_valid, data, errors = self.validate_data(data)

        if not is_valid:
            return JsonResponse(errors, status=400)

        magic_link = generate_magic_link(data["email"])

        if "dev" not in data:
            send_magic_link(magic_link)

        return JsonResponse({
            "message": "Magic link sent."
        })

    @staticmethod
    def get_data(request: HttpRequest):
        if request.content_type in JSON_CONTENT_TYPES:
            data = json.loads(request.body)
        else:
            devlog.info(request.content_type)
            data = request.POST
        return data

    @staticmethod
    def validate_data(data: dict[str, str]):
        errors = {
            "email": [],
            "_": [],
        }

        if "email" not in data or not data["email"]:
            errors["email"].append("This is a required field.")
        if not data["email"].strip():
            errors["email"].append("This is a required field.")
        if not is_email(data["email"]):
            errors["email"].append("This is not a valid email address.")

        # is_valid, data, errors
        return all([len(v) == 0 for v in errors.values()]), data, errors


class MagicLinkLoginView(View):
    """Attempt to login via magic link.

    Link sent to email contains a token. That token
    is verified here by the scribbli-ui.
    """

    def post(self, request: HttpRequest):
        data = self.get_data(request)
        is_valid, data, errors = self.validate_data(data)

        if not is_valid:
            return JsonResponse(errors, status=400)

        try:
            user = authenticate(request, email=data["email"], token=data["token"])
            if user:
                login(request, user)
                return JsonResponse({
                    "email": user.email,
                    "username": user.username,
                })
            else:
                applog.error("authenticate(%s, %s, %s) did not return a user!", request, data["email"], data["token"])
                return JsonResponse({"_": "Failed to verify magic link token."}, status=400)
        except Exception as e:
            applog.exception(e)
            return JsonResponse({"_": "Failed to verify magic link token."}, status=400)

    @staticmethod
    def get_data(request: HttpRequest):
        if request.content_type in JSON_CONTENT_TYPES:
            data = json.loads(request.body)
        else:
            devlog.info(request.content_type)
            data = request.POST
        return data

    @staticmethod
    def validate_data(data: dict[str, str]):
        errors = {
            "email": [],
            "token": [],
            "_": [],
        }

        if "email" not in data or not data["email"]:
            errors["email"].append("This is a required field.")
        if not data["email"].strip():
            errors["email"].append("This is a required field.")
        if not is_email(data["email"]):
            errors["email"].append("This is not a valid email address.")
        if "token" not in data or not data["token"]:
            errors["token"].append("This is a required field.")
        if not data["token"].strip():
            errors["token"].append("This is a required field.")

        # is_valid, data, errors
        return all([len(v) == 0 for v in errors.values()]), data, errors


class LogoutView(View):
    """Dead simple logout view, just call Django's logout helper."""

    def post(self, request: HttpRequest):
        try:
            logout(request)
            return JsonResponse({"_": "Successfully logged out."})
        except Exception as e:
            applog.exception(e)
            return JsonResponse({"_": "Logout failed!"}, status=400)
