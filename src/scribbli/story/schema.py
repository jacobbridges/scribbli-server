import logging

import graphene
from graphene import relay, ObjectType, Field
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.forms.mutation import DjangoModelFormMutation
from graphql_relay import from_global_id

from scribbli.schema.custom_fields import NodeByUniqueStringField
from scribbli.schema.custom_mutations import ScribbliModelFormMutation
from scribbli.story.models import (
    Character,
)
from scribbli.story.forms import (
    CharacterForm,
)
from scribbli.utils import GrapheneDecorators as GD

devlog = logging.getLogger('dev')


class CharacterNode(DjangoObjectType):
    blurb = graphene.String()

    class Meta:
        model = Character
        filter_fields = {
            'name': ['icontains'],
        }
        interfaces = (relay.Node,)

    def resolve_blurb(self, info):
        if not self.blurb: return None
        return self.blurb.content


class CreateCharacter(ScribbliModelFormMutation):
    character = Field(CharacterNode)
    global_id_fields = ('home',)

    class Meta:
        form_class = CharacterForm


class Query(ObjectType):
    character = relay.Node.Field(CharacterNode)
    character_by_slug = NodeByUniqueStringField(
        CharacterNode,
        {'slug': 'name_slug'}
    )
    character_list = DjangoFilterConnectionField(CharacterNode)


class Mutations(ObjectType):
    create_character = CreateCharacter.Field()
    update_character = CreateCharacter.Field()
