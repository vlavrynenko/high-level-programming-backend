# forms.py
from django import forms
from .models import Character
from .models import UserCharacters


class CharacterListForm(forms.Form):
    character = forms.ModelChoiceField(
        queryset=Character.objects.none(),  # Initially empty queryset
        empty_label=None,
        label='Select a Character',
    )

    def __init__(self, user, *args, **kwargs):
        super(CharacterListForm, self).__init__(*args, **kwargs)

        # Filter the queryset based on the current user
        self.fields['character'].queryset = UserCharacters.objects.filter(user_id=user.id)
