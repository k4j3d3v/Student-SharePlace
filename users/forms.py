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


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("email", "username", "degree", "pic")


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("email", "username", "pic")
        # widgets = {
        #     'pic': forms.ImageField(widget=PictureWidget),
        # }
