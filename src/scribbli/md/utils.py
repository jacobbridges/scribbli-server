from scribbli.md.models import (
    Document,
    DocumentReference,
    DocumentRevision,
)


def create_doc(obj, content, author, is_draft=False, purpose=None):
    """Create a new document for obj by author."""

    doc = Document.objects.create(
        author=author,
        is_draft=is_draft,
        purpose=purpose,
    )
    rev = DocumentRevision.objects.create(
        document=doc,
        author=author,
        content=content,
    )
    ref = DocumentReference.objects.create(
        document=doc,
        content_type=obj.content_type,
        object_id=obj.id,
    )

    return doc


def update_doc(doc, content, author):
    """Update a document by author."""

    if not doc:
        raise TypeError("Expected doc to be instance of scribbli.md.Document")

    if content == doc.content:
        # Contents are identical, no need for a new revision
        return doc

    rev = DocumentRevision.objects.create(
        document=doc,
        author=author,
        content=content,
    )

    # Cache bust the doc's latest content
    try:
        del doc.content
    except AttributeError:
        # no cache to bust
        pass

    return doc


def get_docs_for_obj(obj, purpose='*'):
    refs = DocumentReference.objects.filter(
        content_type=obj.content_type,
        object_id=obj.id,
    )

    if purpose != '*':
        refs = refs.filter(document__purpose=purpose)

    # TODO: Might need to paginate in the future
    # e.g. fetching all pages for a world's wiki
    return [ref.document for ref in refs]
