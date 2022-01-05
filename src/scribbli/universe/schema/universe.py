from graphene import relay, ObjectType, ID
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from scribbli.universe.models import Universe


class UniverseNode(DjangoObjectType):

    class Meta:
        model = Universe
        filter_fields = ['name_slug']
        fields = ['id', 'name', 'name_slug']
        interfaces = (relay.Node,)
