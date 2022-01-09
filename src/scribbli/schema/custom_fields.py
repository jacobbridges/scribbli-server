from graphene import Field, String


class NodeByUniqueStringField(Field):
    """Get a single node by a unique string field."""

    def __init__(self, node, field_obj, **kwargs):
        self.node_type = node
        self.field_alias, self.field_name = list(field_obj.items())[0]
        self.field_type = False
        super().__init__(node, **{
            self.field_alias: String(required=True),
            'resolver': self.resolver,
            **kwargs,
        })

    def resolver(self, root, info, **kwargs):
        field_value = list(kwargs.values())[0]
        return self.node_type._meta.model.objects.get(
            **{self.field_name: field_value}
        )
