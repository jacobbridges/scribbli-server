from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from landing import views


urlpatterns = [
    path("presignup/", csrf_exempt(views.PreSignUpApiView.as_view())),
]
