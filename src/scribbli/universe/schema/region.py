import logging

import graphene
from graphene import relay, Field
from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation

from scribbli.universe.models import Region
from scribbli.universe.forms import RegionForm
from scribbli.universe.utils import get_universe_by_graphql_id
from scribbli.utils import GrapheneDecorators as GD

devlog = logging.getLogger('dev')


class RegionNode(DjangoObjectType):
    class Meta:
        model = Region
        filter_fields = {
            'name': ['icontains'],
            'level': ['exact'],
            'universe': ['exact'],
            'universe__name_slug': ['exact'],
        }
        interfaces = (relay.Node,)


class RegionMutation(DjangoModelFormMutation):
    region = Field(RegionNode)

    class Meta:
        form_class = RegionForm


class CreateWorld(relay.ClientIDMutation):
    class Input:
        universe_id = graphene.ID(required=True)
        name = graphene.String(required=True)

    world = graphene.Field(RegionNode)

    @classmethod
    @GD.ensure_auth()
    def mutate_and_get_payload(cls, root, info, **kwargs):
        universe_id = kwargs['universe_id']
        world_name = kwargs['name']
        author = kwargs['author']

        try:
            universe = get_universe_by_graphql_id(universe_id)
        except Exception as e:
            devlog.exception('Exception occurred while finding universe with graphql_id %s', universe_id)
            raise Exception('No such universe')

        try:
            world = Region.objects.create(
                universe=universe,
                name=world_name,
                level=0,
                author=author,
            )
        except Exception:
            devlog.exception('Exception occurred while creating world')
            raise Exception('Something went wrong')

        return CreateWorld(world=world)
