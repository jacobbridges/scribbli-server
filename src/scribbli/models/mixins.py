import uuid

from django.conf import settings
from django.db import models



class DateCreatedModelMixin(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    @property
    def created_timestamp(self):
        if self.date_created:
            return self.date_created.timestamp()
        else:
            return None


class DateUpdatedModelMixin(models.Model):
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    @property
    def updated_timestamp(self):
        if self.date_updated:
            return self.date_updated.timestamp()
        else:
            return None


class ActiveModelMixin(models.Model):
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def activate(self, should_save=True):
        self.is_active = True
        if should_save:
            self.save()

    def deactivate(self, should_save=True):
        self.is_active = False
        if should_save:
            self.save()


class UuidModelMixin(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    class Meta:
        abstract = True

    def __repr__(self):
        s = '<{self.__class__.__name__}[{self.id}]>'
        if hasattr(self, 'strfmt') and callable(self.strfmt):
            return self.strfmt(s)
        elif hasattr(self, 'strfmt') and type(self.strfmt) == str:
            return (s + ' ' + self.strfmt).format(self=self)
        return s.format(self=self)


class AuthorModelMixin(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class GeneralPurposeModelMixin(
        DateCreatedModelMixin,
        DateUpdatedModelMixin,
        ActiveModelMixin,
        UuidModelMixin,
):
    """Combination of general use model mixins."""

    class Meta:
        abstract = True


def slug_mixin_factory(field_name_to_be_slugged: str, max_len: int):
    """
    Generate SlugModelMixin based on factory pattern.

    Complex problems call for complex solutions. A model could have more than
    one sluggable field, each with their own name and length. Following the
    mixin factory pattern laid out in this[1] StackOverflow question, this
    function will generate a mixin for each case.

    - [1] https://stackoverflow.com/a/55051990
    """

    class SlugModelMixin(models.Model):
        class Meta:
            abstract = True

    SlugModelMixin.add_to_class(
        field_name_to_be_slugged + '_slugify',
        models.CharField(max_length=max_len, blank=True),
    )
    SlugModelMixin.add_to_class(
        field_name_to_be_slugged + '_slug',
        models.CharField(max_length=max_len + 4, blank=True, unique=True),
    )

    return SlugModelMixin
