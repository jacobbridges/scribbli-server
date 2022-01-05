from django.db import models

from scribbli.models.mixins import (
    GeneralPurposeModelMixin,
    slug_mixin_factory,
)


class Universe(GeneralPurposeModelMixin, slug_mixin_factory("name", 50)):
    strfmt = "{self.name}"

    name = models.CharField(max_length=50)
