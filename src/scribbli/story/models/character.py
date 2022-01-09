from django.db import models
from django.utils.functional import cached_property

from scribbli.models.mixins import (
    AuthorModelMixin,
    ContentTypeMixin,
    GeneralPurposeModelMixin,
    slug_mixin_factory,
)
from scribbli.md.utils import get_docs_for_obj
from scribbli.universe.models import Region


class Character(
        ContentTypeMixin,
        AuthorModelMixin,
        GeneralPurposeModelMixin,
        slug_mixin_factory('name', 80),
):
    """An entity through which the universe experiences itself."""
    name = models.CharField(max_length=80)
    home = models.ForeignKey(  # World of origin, not "spiritual" home
        Region,
        on_delete=models.SET_NULL,
        null=True,
    )

    @cached_property
    def blurb(self):
        docs = get_docs_for_obj(self, purpose='blurb')
        if len(docs) == 1:
            return docs[0]
        if len(docs) > 1:
            raise ValueError(f'More than one blurb found for {self}')
        return None
