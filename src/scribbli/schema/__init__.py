import graphene
from graphene_django import DjangoObjectType

from scribbli.models import User

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "email")

class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)

    def resolve_all_users(root, info):
        # We can easily optimize query count in the resolve method
        return User.objects.all()

schema = graphene.Schema(query=Query)