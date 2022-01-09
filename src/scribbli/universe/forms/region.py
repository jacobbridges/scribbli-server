import logging

from django.forms import CharField

from scribbli.universe.models import Region
from scribbli.md.utils import (
    create_doc,
    update_doc,
)

from scribbli.forms import ModelFormWithRequest

devlog = logging.getLogger('dev')


class RegionForm(ModelFormWithRequest):
    blurb = CharField(required=False)

    class Meta:
        model = Region
        fields = ['name', 'parent', 'universe']

    def save(self, commit=True):
        region = super().save(commit=False)
        region.author = self.request.user
        if commit is True:
            region.save()

        blurb = self.cleaned_data['blurb']
        if not blurb:
            return region

        if region.blurb:
            update_doc(region.blurb, blurb, self.request.user)
        else:
            create_doc(region, blurb, self.request.user, purpose='blurb')
        del region.blurb

        return region


class RegionUpdateForm(ModelFormWithRequest):
    # Dumb that this requires two separate forms,
    # but I don't know how else to remove the required
    # restraint on some fields during update vs create
    blurb = CharField(required=False)

    class Meta:
        model = Region
        fields = ['blurb']

    def save(self, commit=True):
        region = super().save(commit=commit)

        blurb = self.cleaned_data['blurb']
        if not blurb:
            return region

        if region.blurb:
            update_doc(region.blurb, blurb, self.request.user)
            del region.blurb
        else:
            create_doc(region, blurb, self.request.user, purpose='blurb')
            del region.blurb

        return region
