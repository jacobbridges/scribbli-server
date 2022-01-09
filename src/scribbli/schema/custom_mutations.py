from graphene_django.forms.mutation import DjangoModelFormMutation
from graphql_relay import from_global_id


class ScribbliModelFormMutation(DjangoModelFormMutation):

    class Meta:
        abstract = True

    @classmethod
    def get_form_kwargs(cls, root, info, **data):
        new_data = dict()
        for k, v in data.items():
            if k in cls.gloobal_id_fields:
                _, pk = from_global_id(v)
                new_data[k] = pk
            else:
                new_data[k] = v
        kwargs = dict(
            data=new_data,
            request=info.context,
        )

        if new_data.get('id', None):
            kwargs['instance'] = cls._meta.model._default_manager.get(
                pk=new_data.get('id')
            )

            return kwargs
