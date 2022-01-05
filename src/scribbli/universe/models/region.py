from mptt.models import MPTTModel, TreeForeignKey

from django.db import models

from scribbli.models.mixins import (
    AuthorModelMixin,
    GeneralPurposeModelMixin,
    slug_mixin_factory,
)


class Region(AuthorModelMixin, GeneralPurposeModelMixin, slug_mixin_factory('name', 50), MPTTModel):
    name = models.CharField(max_length=50)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    universe = models.ForeignKey('universe.Universe', on_delete=models.CASCADE)

    class MPTTMeta:
        order_insertion_by = ['name_slug']
