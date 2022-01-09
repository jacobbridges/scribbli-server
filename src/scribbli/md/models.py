from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.functional import cached_property

from scribbli.models import mixins



class Document(
    mixins.UuidModelMixin,
    mixins.DateCreatedModelMixin,
    mixins.DateUpdatedModelMixin,
    mixins.AuthorModelMixin,
):
    """Any document which supports markup."""
    # Content should be pulled from latest revision instead
    # content = models.TextField()
    is_draft = models.BooleanField(default=True)
    purpose = models.CharField(max_length=32, null=True)

    @cached_property
    def content(self):
        latest_revision = self.revs.order_by('-date_created').first()
        return latest_revision.content


class DocumentRevision(
    mixins.UuidModelMixin,
    mixins.DateCreatedModelMixin,
    mixins.AuthorModelMixin,
):
    """Historical versions of a document."""
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='revs',
    )
    content = models.TextField()


class DocumentReference(models.Model):
    """Link documents to any other object."""
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='refs',
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=32)
    ref = GenericForeignKey('content_type', 'object_id')
