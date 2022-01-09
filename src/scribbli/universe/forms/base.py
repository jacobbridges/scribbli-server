from django.forms import ModelForm, CharField


class ModelFormWithRequest(ModelForm):

    def __init__(self, *args, **kwargs):

        try:
            self.request = kwargs.pop('request')
        except KeyError:
            self.request = None

        super().__init__(*args, **kwargs)
