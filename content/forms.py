from content.models import Note, Experience
from django.forms import ModelForm


class AddNoteModelForm(ModelForm):
    class Meta:
        model = Note
        exclude = ['path', 'owner', 'publ_date']

    def __init__(self, user=None, **kwargs):
        super(AddNoteModelForm, self).__init__(**kwargs)
        if user:
            self.fields['course'].queryset = user.degree.course_set.all()


class AddExperienceModelForm(ModelForm):

    def __init__(self, user=None, **kwargs):
        super(type(self), self).__init__(**kwargs)
        # TODO: manage degree or course choice for experience
        # self.fields['degree'].widget = forms.TextInput()
        if user:
            self.fields['course'].queryset = user.degree.course_set.all()

    class Meta:
        model = Experience
        exclude = ['owner', 'publ_date']
