"""scribbli URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path

from graphene_django.views import GraphQLView

from scribbli.schema import schema
from scribbli.views.auth import (
    PrivateGraphQLView,
    MagicLinkCreateView,
    MagicLinkLoginView,
    LogoutView,
)
from landing.views import PreSignUpApiView


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import include
from django.views.decorators.csrf import csrf_exempt

import logging

@csrf_exempt
def test_create_magic_link(request):
    from magiclink.utils import generate_magic_link, get_url, send_magic_link
    email = request.POST['email']
    ml = generate_magic_link(email)
    send_magic_link(ml)
    return HttpResponse("email has been sent")


@csrf_exempt
def test_verify_magic_link(request):
    email = request.POST['email']
    token = request.POST['token']

    try:
        user = authenticate(request, email=email, token=token)
        if user:
            login(request, user)
            return redirect("/home/")
        else:
            return HttpResponse("No!")
    except Exception as e:
        logging.exception(e)
        return HttpResponse("FAil!")


@csrf_exempt
def test_logout(request):
    logout(request)
    # Redirect to a success page.


def test_home(request):
    if not isinstance(request.user, AnonymousUser):
        return HttpResponse(f"Hello {request.user.email}!")
    else:
        return HttpResponse("Hello World!")


def test_csrf(request):
    from django.template import Template, RequestContext
    t = Template("{% csrf_token %}")
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))


urlpatterns = [
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
    #path("login/", test_create_magic_link),
    #path("verify_magic_link/", test_verify_magic_link),
    #path("logout/", test_logout),
    path("home/", test_home),
    path("csrf/", test_csrf),
    path("api/create-magic-link/", MagicLinkCreateView.as_view()),
    path("api/verify-magic-link/", MagicLinkLoginView.as_view()),
    path("api/logout", LogoutView.as_view()),
    path("api/", include("landing.urls")),
]
