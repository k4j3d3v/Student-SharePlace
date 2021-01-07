from content.models import Note, Experience, Course
from django import forms
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
            print("user degree")
            print(user)
            self.fields['course'].queryset = Course.objects.filter(degree=user.degree)
            self.fields['degree'].queryset = user.degree
            self.fields['degree'].widget = forms.CheckboxSelectMultiple()

    class Meta:
        model = Experience
        exclude = ['owner', 'publ_date']
