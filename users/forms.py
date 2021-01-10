from content.models import Degree
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import CustomUser


# from string import Template
# from django.utils.safestring import mark_safe
# from django.forms import ImageField, forms

#
# class PictureWidget(forms.widgets.Widget):
#     def render(self, name, value, attrs=None, **kwargs):
#         html = Template("""<img src="$link"/>""")
#         return mark_safe(html.substitute(link=value))

# TODO : refactoring and understand why it works


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("email", "username", "degree", "pic")

    degree = forms.ModelMultipleChoiceField(
        queryset=Degree.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    # Overriding save allows us to process the value of 'toppings' field
    def save(self, commit=True):
        # Get the unsaved Pizza instance
        instance = super(CustomUserCreationForm, self).save(False)

        # Prepare a 'save_m2m' method for the form,
        old_save_m2m = self.save_m2m

        def save_m2m():
            old_save_m2m()
            # This is where we actually link the pizza with toppings
            instance.degree.clear()
            for d in self.cleaned_data['degree']:
                instance.degree.add(d)

        self.save_m2m = save_m2m

        instance.save()
        self.save_m2m()

        return instance


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("email", "username", "pic")
        # widgets = {
        #     'pic': forms.ImageField(widget=PictureWidget),
        # }
