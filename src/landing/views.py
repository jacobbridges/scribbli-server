import json

from django.views import View
from django.http import JsonResponse, HttpResponseBadRequest


from landing.models import PreSignUp


class PreSignUpApiView(View):
    """
    Handle pre-signups requests from a front-end form.
    """

    model = PreSignUp

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        if "email" not in data or not data["email"]:
            return HttpResponseBadRequest()

        try:
            m = PreSignUp(email=data["email"])
            m.save()
        except Exception as e:
            print(e)
            return HttpResponseBadRequest()
        return JsonResponse({"signup_id": m.id})
