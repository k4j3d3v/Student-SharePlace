from django.urls import path, include
from users.views import home, NotesListView, ExperiencesListView, ProfileUpdate

app_name = 'users'


urlpatterns = [
    path('', home, name='home'),
    path('content/', include('content.urls')),
    path('notes', NotesListView.as_view(), name='notes'),
    path('experiences', ExperiencesListView.as_view(), name='experiences'),
    path('profile', ProfileUpdate.as_view(), name='profile'),

]
