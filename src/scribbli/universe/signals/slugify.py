from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from scribbli.universe.models import Universe, Region


@receiver(pre_save, sender=Region)
@receiver(pre_save, sender=Universe)
def slugify_model(sender, **kwargs):
    instance = kwargs.get("instance")
    instance.slug = slugify(instance.name)
    return instance