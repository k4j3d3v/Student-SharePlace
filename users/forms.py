from content.models import Degree
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from users.models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Choose a password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm previous password'})

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("email", "username", "degree", "pic")
        widgets = {
            # 'pic': PictureWidget,
            'email': forms.TextInput(attrs={'placeholder': 'University Email'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),

        }

    degree = forms.ModelMultipleChoiceField(
        queryset=Degree.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    # Overriding save allows us to process the value of 'degrees' field
    def save(self, commit=True):
        # Get the unsaved instance
        instance = super(CustomUserCreationForm, self).save(False)

        # Prepare a 'save_m2m' method for the form,
        def save_m2m():
            self.save_m2m()
            # This is where we actually link the user with degree
            instance.degree.clear()
            for d in self.cleaned_data['degree']:
                instance.degree.add(d)

        instance.save()
        save_m2m()
        return instance


class CustomUserChangeForm(UserChangeForm):
    password = None

    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ("email", "username", "pic", "degree")
        widgets = {
            # 'pic': ImageWidget,
            'degree': forms.CheckboxSelectMultiple,
        }


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'University Email'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        }
    ))
