import logging

import graphene
from graphene import relay, Field
from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation
from graphql_relay import from_global_id

from scribbli.universe.models import Region
from scribbli.universe.forms import RegionForm, RegionUpdateForm
from scribbli.universe.utils import get_universe_by_graphql_id
from scribbli.utils import GrapheneDecorators as GD

devlog = logging.getLogger('dev')


class RegionNode(DjangoObjectType):
    blurb = graphene.String()

    class Meta:
        model = Region
        filter_fields = {
            'name': ['icontains'],
            'level': ['exact', 'gt'],
            'universe': ['exact'],
            'universe__name_slug': ['exact'],
            'parent': ['exact'],
        }
        interfaces = (relay.Node,)

    def resolve_blurb(self, info):
        if not self.blurb: return None
        return self.blurb.content


class CreateRegion(DjangoModelFormMutation):
    region = Field(RegionNode)
    global_id_fields = ('id', 'parent', 'universe')

    class Meta:
        form_class = RegionForm

    @classmethod
    def get_form_kwargs(cls, root, info, **input):
        # convert global ids to django ids
        data = {
            'author': info.context.user,
        }
        for k, v in input.items():
            if k in cls.global_id_fields:
                _, pk = from_global_id(v)
                data[k] = pk
            else:
                data[k] = v
        kwargs = {'data': data, 'request': info.context}

        global_id = input.pop('id', None)
        if global_id:
            _, pk = from_global_id(global_id)
            instance = cls._meta.model._default_manager.get(pk=pk)
            kwargs['instance'] = instance

        return kwargs


class UpdateRegion(DjangoModelFormMutation):
    region = Field(RegionNode)

    class Meta:
        form_class = RegionUpdateForm

    @classmethod
    def get_form_kwargs(cls, root, info, **input):
        kwargs = {'data': input, 'request': info.context}

        global_id = input.pop('id', None)
        if global_id:
            _, pk = from_global_id(global_id)
            instance = cls._meta.model._default_manager.get(pk=pk)
            kwargs['instance'] = instance

        return kwargs


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
