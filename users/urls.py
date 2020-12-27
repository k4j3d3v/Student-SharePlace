from django.urls import path, include

from users.views import dashboard, register, NotesListView, ExperiencesListView, ProfileUpdate

# app_name = 'users'


urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('content/', include('content.urls')),
    path('register/', register, name='register'),
    path('notes', NotesListView.as_view(), name='notes'),
    path('experiences', ExperiencesListView.as_view(), name='experiences'),
    path('edit_profile', ProfileUpdate.as_view(), name='edit_profile'),

]
