from mptt.models import MPTTModel, TreeForeignKey

from django.db import models
from django.utils.functional import cached_property

from scribbli.models.mixins import (
    AuthorModelMixin,
    ContentTypeMixin,
    GeneralPurposeModelMixin,
    slug_mixin_factory,
)
from scribbli.md.utils import get_docs_for_obj


class Region(ContentTypeMixin, AuthorModelMixin, GeneralPurposeModelMixin, slug_mixin_factory('name', 50), MPTTModel):
    name = models.CharField(max_length=50)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    universe = models.ForeignKey('universe.Universe', on_delete=models.CASCADE)
    #blurb = models.ForeignKey(
    #    Document,
    #    on_delete=models.CASCADE,
    #    related_name='blurb_for_regions',
    #    null=True,
    #)

    class MPTTMeta:
        order_insertion_by = ['name_slug']

    @cached_property
    def blurb(self):
        docs = get_docs_for_obj(self, purpose='blurb')
        if len(docs) == 1:
            return docs[0]
        if len(docs) > 1:
            raise ValueError(f'More than one blurb found for {self}')
        return None
