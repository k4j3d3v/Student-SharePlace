from content.views import CoursesListView
from content.views import NoteDetail, NoteCreate, NoteUpdate, NoteDelete, \
    ExperienceDetail, ExperienceUpdate, ExperienceDelete, ExperienceCreate, \
    PurchasedNotesList, buy_note, ExchangeNote, ExchangeRequestList, manage_exchange, \
    NotificationList, delete_notification
from django.urls import path

app_name = 'content'

urlpatterns = [

    path('notes/details/<int:pk>', NoteDetail.as_view(), name='note-detail'),
    path('notes/update/<int:pk>', NoteUpdate.as_view(), name='note-update'),
    path('notes/delete/<int:pk>', NoteDelete.as_view(), name='note-delete'),
    path('notes/add', NoteCreate.as_view(), name='note-add'),
    path('notes/buy', buy_note, name='note-buy'),
    path('notes/exchange/<int:pk>', ExchangeNote.as_view(), name='note-exchange'),
    path('requests/exchange/', ExchangeRequestList.as_view(), name='note-request'),
    path('notifications', NotificationList.as_view(), name='notifications'),
    path('delete_notif', delete_notification, name='notif-delete'),
    path('requests/action/', manage_exchange, name='request-action'),
    path('experience/details/<int:pk>', ExperienceDetail.as_view(), name='experience-detail'),
    path('experience/update/<int:pk>', ExperienceUpdate.as_view(), name='experience-update'),
    path('experience/delete/<int:pk>', ExperienceDelete.as_view(), name='experience-delete'),
    path('experience/add', ExperienceCreate.as_view(), name='experience-add'),
    path('courses/', CoursesListView.as_view(), name='course-list'),
    path('notes/purchased/', PurchasedNotesList.as_view(), name='purchased-list'),
]
