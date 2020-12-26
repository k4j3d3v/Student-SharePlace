from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from users.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("email", "username", "degree", "pic")


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("email", "username", "pic")
