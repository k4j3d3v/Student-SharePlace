from content.models import Note, Experience
from django.forms import ModelForm


class AddNoteModelForm(ModelForm):
    class Meta:
        model = Note
        exclude = ['path', 'owner', 'publ_date']


class AddExperienceModelForm(ModelForm):
    class Meta:
        model = Experience
        exclude = ['owner', 'publ_date']
