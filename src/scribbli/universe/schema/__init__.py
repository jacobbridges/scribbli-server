from graphene import relay, ObjectType, Field, String
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from scribbli.schema.custom_fields import NodeByUniqueStringField

from .universe import UniverseNode
from .region import (
    RegionNode,
    CreateRegion,
    UpdateRegion,
    CreateWorld,
)


#class NodeByUniqueStringField(Field):
#    def __init__(self, node, field_obj, **kwargs):
#        self.node_type = node
#        self.field_alias, self.field_name = list(field_obj.items())[0]
#        self.field_type = False
#        super().__init__(node, **{
#            self.field_alias: String(required=True),
#            'resolver': self.resolver,
#            **kwargs,
#        })
#
#    def resolver(self, root, info, **kwargs):
#        import logging
#        l = logging.getLogger('dev')
#        field_value = list(kwargs.values())[0]
#        l.info('========== %s(%s=%s) == %s',
#               self.node_type._meta.model,
#               self.field_name,
#               field_value,
#               self.node_type._meta.model.objects.get(**{self.field_name: field_value}))
#        return self.node_type._meta.model.objects.get(**{self.field_name: field_value})


class Query(ObjectType):
    universe = relay.Node.Field(UniverseNode)
    universe_list = DjangoFilterConnectionField(UniverseNode)

    region = relay.Node.Field(RegionNode)
    region_by_slug = NodeByUniqueStringField(RegionNode, {'slug': 'name_slug'})
    region_list = DjangoFilterConnectionField(RegionNode)

class Mutations(ObjectType):
    update_region = UpdateRegion.Field()
    create_region = CreateRegion.Field()
    create_world = CreateWorld.Field()
