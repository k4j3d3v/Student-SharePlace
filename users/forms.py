from string import Template

from content.models import Degree
from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.safestring import mark_safe
from users.models import CustomUser


class PictureWidget(forms.widgets.Widget):

    # def __init__(self):
    #     super(PictureWidget, self).__init__()
    #     self.is_hidden = False

    def render(self, name, value, attrs=None, **kwargs):
        # print(name)
        # forms.ImageField().widget.render(name,value)

        html_str = '<div class="row">\
                   <div class="small-12 medium-2 large-2 columns" style="text-align:center;">\
                     <div class="circle">\
                     <!-- User Profile Image -->\
                       <img class="profile-pic" src="$media$link" id="pic">\
                     </div>\
                     <div class="p-image" style="">\
                        <i class="fa fa-camera upload-button"></i>\
                        <input class="file-upload" type="file" accept="image/*"/>\
                     </div>\
                    </div>\
                </div>'
        # img_field = forms.ImageField(
        #     widget=forms.ClearableFileInput(attrs={'accept': 'images/*', 'id': 'pic_inp'})).widget
        # html = Template(img_field.render(name, value) + \
        #                 """<img src="$media$link" id="pic"/>""")

        html = Template(html_str)
        return mark_safe(html.substitute(media=settings.MEDIA_URL, link=value))


# TODO : refactoring and understand why it works


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("email", "username", "degree", "pic")
        widgets = {
            'pic': PictureWidget,
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
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("email", "username", "pic")
        # widgets = {
        #      'pic': PictureWidget,
        # }
