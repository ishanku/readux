from django.db import models
from django.conf import settings
from django.db.models import signals
from django.dispatch import receiver
import json
import uuid
from django_mysql.models import JSONField


class Annotation(models.Model):
    '''
    Django database model to manage IIIF annotations generated by Mirador.
    '''

    #: regex for recognizing valid UUID, for use in site urls
    UUID_REGEX = r'[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}'

    #: annotation schema version: default v1.0
    schema_version = "v1.0"
    # for now, hard-coding until or unless we need to support more than
    # one version of annotation

    #: unique id for the annotation; uses :meth:`uuid.uuid4`
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # data model includes version, do we need to set that in the db?
    # "annotator_schema_version": "v1.0",        # schema version: default v1.0

    #: datetime annotation was created; automatically set when added
    created = models.DateTimeField(auto_now_add=True)
    #: datetime annotation was last updated; automatically updated on save
    updated = models.DateTimeField(auto_now=True)
    #: content of the annotation
    text = models.TextField()
    #: the annotated text
    quote = models.TextField()
    volume_identifier = models.TextField()
    page = models.TextField()
    #: URI of the annotated document
    uri = models.URLField()
    #: user who owns the annotation
    #: when serialized, id of annotation owner OR an object with an 'id' property
    # Make user optional for now
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)

    #: Readux-specific field: URI for the volume that an annotation
    #: is associated with (i.e., volume a page is part of)
    volume_uri = models.URLField(blank=True)

    # tags still todo
    # "tags": [ "review", "error" ],             # list of tags (from Tags plugin)

    #: any additional data included in the annotation not parsed into
    #: specific model fields; this includes ranges, permissions,
    #: annotation data, etc
    iiif_annotation = JSONField(default=dict)


@receiver(signals.pre_save, sender=Annotation)
def set_uris(sender, instance, **kwargs):
    if isinstance(instance.iiif_annotation, dict):
        instance.uri = instance.iiif_annotation['on'][0]['full']
        instance.volume_uri = instance.iiif_annotation['on'][0]['within']['@id']
        instance.volume_identifier = instance.uri.split('/')[-3]
        instance.page = instance.uri.split('/')[-1]
        instance.iiif_annotation['annotatedBy'] = {'name': 'Me'}
        instance.iiif_annotation['@id'] = str(instance.pk)
