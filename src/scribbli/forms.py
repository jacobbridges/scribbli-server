from django.forms import ModelForm


class ModelFormWithRequest(ModelForm):
    """ModelForm which takes request as an optional input."""

    def __init__(self, *args, **kwargs):
        try:
            self.request = kwargs.pop('request')
        except KeyError:
            self.request = None

        super().__init__(*args, **kwargs)
