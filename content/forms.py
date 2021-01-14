from content.models import Note, Experience, ExchangeRequest
from django.forms import ModelForm


class AddNoteModelForm(ModelForm):
    class Meta:
        model = Note
        exclude = ['path', 'owner', 'publ_date']

    def __init__(self, user=None, **kwargs):
        super(AddNoteModelForm, self).__init__(**kwargs)
        if user:
            self.fields['course'].queryset = user.get_courses()  # .degree.course_set.all()


class AddExperienceModelForm(ModelForm):

    def __init__(self, user=None, **kwargs):
        super(type(self), self).__init__(**kwargs)
        # TODO: manage degree or course choice for experience
        # self.fields['degree'].widget = forms.TextInput()
        if user:
            print("user degree")
            print(user)
            self.fields['course'].queryset = user.get_courses()
            self.fields['degree'].queryset = user.degree
            # self.fields['degree'].widget = forms.CheckboxSelectMultiple()

    class Meta:
        model = Experience
        exclude = ['owner', 'publ_date']


class ExchangeRequestModelForm(ModelForm):

    def __init__(self, user=None, pk=None, **kwargs):
        super(type(self), self).__init__(**kwargs)
        if user and pk:
            self.fields['proposed_note'].queryset = Note.objects.filter(owner=user)
            self.fields['requested_note'].queryset = Note.objects.exclude(owner=user)
            self.fields['requested_note'].initial = Note.objects.get(pk=pk)
            self.user = user

    def save(self, commit=True):
        # Get the unsaved Pizza instance
        instance = super(type(self), self).save(False)
        instance.user_receiver = instance.requested_note.owner
        instance.user_requester = self.user
        instance.save()
        return instance

    class Meta:
        model = ExchangeRequest
        fields = ['proposed_note', 'requested_note']
