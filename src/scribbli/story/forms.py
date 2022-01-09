import logging

from django.forms import CharField

from scribbli.story.models import Character
from scribbli.md.utils import (
    create_doc,
    update_doc,
)

from scribbli.forms import ModelFormWithRequest

devlog = logging.getLogger('dev')


class CharacterForm(ModelFormWithRequest):
    blurb = CharField(required=False)

    class Meta:
        model = Character
        fields = ['name', 'home']

    def save(self, commit=True):
        self.instance = self.request.user
        character = super().save(commit=commit)

        blurb = self.cleaned_data['blurb']
        if not blurb:
            return character
        if character.blurb:
            update_doc(character.blurb, blurb, self.request.user)
        else:
            create_doc(character, blurb, self.request.user, purpose='blurb')
        del character.blurb

        return character
