import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from landing.models import PreSignUp


class PreSignUpNode(DjangoObjectType):
    class Meta:
        model = PreSignUp
        filter_fields = ("email", "created_at")
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    presignup = relay.Node.Field(PreSignUpNode)
    all_presignups = DjangoFilterConnectionField(PreSignUpNode)
