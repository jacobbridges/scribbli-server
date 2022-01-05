from django.forms import ModelForm

from scribbli.universe.models import Region


class RegionForm(ModelForm):
    class Meta:
        model = Region
        fields = ['name', 'parent', 'universe']
