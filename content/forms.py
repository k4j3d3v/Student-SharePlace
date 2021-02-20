from content.models import Note, Experience, ExchangeRequest
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm


class AddNoteModelForm(ModelForm):
    class Meta:
        model = Note
        exclude = ['path', 'owner', 'publ_date']

    def __init__(self, user=None, **kwargs):
        super(AddNoteModelForm, self).__init__(**kwargs)
        if user:
            self.fields['course'] = forms.ModelChoiceField(queryset=user.get_courses(), widget=forms.RadioSelect)
        for name, field in self.fields.items():
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs.update({'class': 'form-control'})


class AddExperienceModelForm(ModelForm):

    def __init__(self, user=None, **kwargs):
        super(type(self), self).__init__(**kwargs)
        # TODO: manage degree or course choice for experience
        if user:
            self.fields['course'] = forms.ModelMultipleChoiceField(
                queryset=user.get_courses(),
                widget=forms.CheckboxSelectMultiple,
                required=False
            )
            self.fields['degree'] = forms.ModelChoiceField(queryset=user.degree,
                                                           widget=forms.RadioSelect,
                                                           required=False)
        # for name, field in self.fields.items():
        #     if 'class' in field.widget.attrs:
        #         field.widget.attrs['class'] += ' form-control'
        #     else:
        #         field.widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        courses = cleaned_data.get("course")
        degrees = cleaned_data.get("degree")
        if courses and degrees:
            raise ValidationError(
                "You can't add an experience relatives to Course and Degree."
                "If it's connected to a Course, is implicitly also connected to Degree from which course belongs to.")
        elif not (courses or degrees):
            raise ValidationError(
                "An experience must be relative to a Course or a Degree.")

    class Meta:
        model = Experience
        exclude = ['owner', 'publ_date']


class ExchangeRequestModelForm(ModelForm):

    def __init__(self, user=None, pk=None, **kwargs):
        super(type(self), self).__init__(**kwargs)
        if user and pk:
            self.fields['proposed_note'].queryset = Note.objects.filter(owner=user)
            had_notes = user.purchased_notes.all().values_list('id')
            self.fields['requested_note'].queryset = Note.objects.exclude(owner=user).exclude(id__in=had_notes)
            self.fields['requested_note'].initial = Note.objects.get(pk=pk)
            self.user = user

    def clean(self):
        cleaned_data = super().clean()
        proposed = cleaned_data.get("proposed_note")
        requested = cleaned_data.get("requested_note")
        # check if receiver user has already proposed note
        receiver = requested.owner
        if receiver.purchased_notes.filter(id=proposed.id).count() > 0:
            raise ValidationError(
                f"{receiver} has already obtained your {proposed} notes."
                "This exchange request is not possible!")

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
