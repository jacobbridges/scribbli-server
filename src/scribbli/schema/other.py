from django.contrib.auth import get_user_model
import graphene as g
from graphene_django import DjangoObjectType

User = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "email")


class AppContext(g.ObjectType):
    csrftoken = g.String()  # hehee
    universe_id = g.String()
    is_logged_in = g.Boolean()
    userdata = g.Field(UserType)
