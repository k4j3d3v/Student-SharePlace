from content.views import CoursesListView
from content.views import NoteDetail, NoteCreate, NoteUpdate, NoteDelete, \
    ExperienceDetail, ExperienceUpdate, ExperienceDelete, ExperienceCreate
from django.urls import path

app_name = 'content'

urlpatterns = [

    path('notes/details/<int:pk>', NoteDetail.as_view(), name='note-detail'),
    path('notes/update/<int:pk>', NoteUpdate.as_view(), name='note-update'),
    path('notes/delete/<int:pk>', NoteDelete.as_view(), name='note-delete'),
    path('notes/add', NoteCreate.as_view(), name='note-add'),
    path('experience/details/<int:pk>', ExperienceDetail.as_view(), name='experience-detail'),
    path('experience/update/<int:pk>', ExperienceUpdate.as_view(), name='experience-update'),
    path('experience/delete/<int:pk>', ExperienceDelete.as_view(), name='experience-delete'),
    path('experience/add', ExperienceCreate.as_view(), name='experience-add'),
    path('courses/', CoursesListView.as_view(), name='course-list')
]
