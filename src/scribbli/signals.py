from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from scribbli.universe.models import Universe, Region


#@receiver(pre_save, sender=Region)
#@receiver(pre_save, sender=Universe)
#def slugify_model(sender, **kwargs):
#    instance = kwargs.get("instance")
#    instance.slug = slugify(instance.name)
#    return instance


@receiver(pre_save, sender=Region)
@receiver(pre_save, sender=Universe)
def process_slugs(sender, **kwargs):
    instance = kwargs.get("instance")
    klass = instance.__class__
    slug_field_names = [
        f.name for f in klass._meta.fields
        if f.name.endswith("_slug")
    ]
    for slug_field_name in slug_field_names:
        field_name = slug_field_name.replace('_slug', '')
        slugify_field_name = field_name + '_slugify'
        field_value = getattr(instance, field_name)
        if field_value:
            slugify_value = slugify(field_value)
            if getattr(instance, slugify_field_name) == slugify_value:
                continue
            count = klass.objects.filter(**{slugify_field_name: slugify_value}).count()
            slug_value = f"{count+1:0>4}_{slugify_value}"
            setattr(instance, slug_field_name, slug_value)
            setattr(instance, slugify_field_name, slugify_value)

    return instance
