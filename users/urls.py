from django.contrib.auth import views as auth_views
from django.urls import path, include
from users.forms import UserLoginForm
from users.views import dashboard, UserCreate, NotesListView, ExperiencesListView, ProfileUpdate

# app_name = 'users'


urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('accounts/login/', auth_views.LoginView.as_view(authentication_form=UserLoginForm)),
    path('accounts/', include('django.contrib.auth.urls')),
    path('content/', include('content.urls')),
    # path('register/', register, name='register'),
    path('register/', UserCreate.as_view(), name='register'),
    path('notes', NotesListView.as_view(), name='notes'),
    path('experiences', ExperiencesListView.as_view(), name='experiences'),
    path('edit_profile', ProfileUpdate.as_view(), name='edit_profile'),

]
