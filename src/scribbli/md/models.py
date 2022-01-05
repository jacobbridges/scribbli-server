from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from scribbli.models import mixins



class Document(
    mixins.UuidModelMixin,
    mixins.DateCreatedModelMixin,
    mixins.DateUpdatedModelMixin,
    # mixins.AuthorModelMixin,
):
    """Any document which supports markup."""
    content = models.TextField()
    is_draft = models.BooleanField(default=True)


class DocumentRevision(
    mixins.UuidModelMixin,
    mixins.DateCreatedModelMixin,
    # mixins.AuthorModelMixin,
):
    """Historical versions of a document."""
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    content = models.TextField()


class DocumentReference(models.Model):
    """Link documents to any other object."""
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=32)
    ref = GenericForeignKey('content_type', 'object_id')
