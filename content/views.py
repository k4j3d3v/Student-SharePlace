import json

from content.forms import AddNoteModelForm, AddExperienceModelForm, ExchangeRequestModelForm
from content.models import Note, Experience, Course, ExchangeRequest, Notification
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, CreateView, ListView
from django.views.generic.edit import UpdateView, DeleteView
from users.models import CustomUser


class ChangePermissionMixin(object):

    def get_object(self, queryset=None):
        obj = super(ChangePermissionMixin, self).get_object(queryset)
        if not self.request.user.is_owner(obj):
            raise PermissionDenied
        return obj


class ExperienceUpdate(LoginRequiredMixin, ChangePermissionMixin, UpdateView):
    model = Experience
    form_class = AddExperienceModelForm
    template_name = 'content/note_update_form.html'


class ExperienceDelete(LoginRequiredMixin, ChangePermissionMixin, DeleteView):
    model = Experience
    success_url = reverse_lazy('users:experiences')
    template_name = 'content/note_confirm_delete.html'


class ExperienceDetail(DetailView):
    model = Experience
    date_field = "publish"
    month_format = "%m"


class ExperienceCreate(LoginRequiredMixin, CreateView):
    form_class = AddExperienceModelForm
    # template_name = 'content/note_add.html'
    template_name = 'content/res_form.html'
    success_url = reverse_lazy('users:experiences')

    def get_form_kwargs(self):
        kwargs = super(ExperienceCreate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        # print(form.instance.degree)
        # for d in self.request.user.degree:
        #     form.instance.degree.add(d)
        return super().form_valid(form)


class NoteDelete(LoginRequiredMixin, ChangePermissionMixin, DeleteView):
    model = Note
    success_url = reverse_lazy('users:notes')


class NoteDetail(DetailView):
    model = Note

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs['pk']
        user = CustomUser.objects.get(email=self.request.user.email)
        context['purchased'] = True if user.purchased_notes.filter(id=id) else False
        context['owner'] = True if user.resource_set.filter(id=id) else False
        return context
    #
    # def get_object(self, queryset=None):
    #     obj = super(NoteDetail, self).get_object(queryset)
    #     if not (self.request.user.is_owner(obj) or self.request.user.has_purchased_note(obj)):
    #         raise PermissionDenied
    #     return obj


# How to make a common superclass for NoteUpdate and NoteCreate views
# to accomplish DRY principle
# class NoteManipulate(View):
#     form_class = AddNoteModelForm
#     model = Note
#
#     def get_form_kwargs(self):
#         kwargs = super(NoteCreate, self).get_form_kwargs()
#         kwargs['user'] = self.request.user
#         return kwargs


class NoteUpdate(LoginRequiredMixin, ChangePermissionMixin, UpdateView):
    model = Note
    form_class = AddNoteModelForm
    template_name_suffix = '_update_form'

    def get_form_kwargs(self):
        kwargs = super(NoteUpdate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        print(self.request.user)
        return kwargs


class NoteCreate(LoginRequiredMixin, CreateView):
    form_class = AddNoteModelForm
    template_name = 'content/note_add.html'
    success_url = reverse_lazy('users:notes')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(NoteCreate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class CoursesListView(LoginRequiredMixin, ListView):
    model = Course
    context_object_name = 'courses_list'
    # template_name = 'content/course_list.html'
    template_name = 'course_tables.html'

    def get_queryset(self):
        # TODO: fix missing degree field in admin user
        print("email: %s \n" % self.request.user.email)
        user = CustomUser.objects.get(email=self.request.user.email)
        courses_qs = user.get_courses()
        courses = {}
        print(f"Course QS: {courses_qs}")
        for course in courses_qs:
            note = course.note_set.exclude(owner=user)
            exps = course.experience_set.exclude(owner=user)
            if note.count() > 0 or exps.count() > 0:
                courses[course] = (note, exps)

        return courses

    # TODO: https://docs.djangoproject.com/en/3.1/topics/db/examples/
    # start from here
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = CustomUser.objects.get(email=self.request.user.email)
        context['notes'] = Note.objects.exclude(owner=user)
        context['exps'] = Experience.objects.exclude(owner=user)
        return context


class PurchasedNotesList(LoginRequiredMixin, ListView):
    model = Note
    context_object_name = 'notes'
    template_name = 'content/purchased_list.html'

    def get_queryset(self):
        user = CustomUser.objects.get(email=self.request.user.email)
        return user.purchased_notes.all()


@login_required
@require_POST
def buy_note(request):
    user = CustomUser.objects.get(email=request.user.email)
    id = request.POST.get('id', None)
    to_buy = Note.objects.filter(id=id).get()
    user.purchased_notes.add(to_buy)
    print(user.purchased_notes.all())
    # ctx = {'valid': valid, 'message': message}
    return HttpResponse(json.dumps({}), content_type='application/json')


class ExchangeNote(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = ExchangeRequestModelForm
    template_name = "content/note_exchange_form.html"
    success_url = reverse_lazy('content:note-request')
    success_message = "Exchange will be notified to %s." \
                      "He will decide if accept your exchange proposal."

    def form_valid(self, form):
        # response = super(type(self), self).form_valid(form)
        # do something with self.object
        self.object = form.save()
        print("object %s" % self.object)
        return super(type(self), self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(ExchangeNote, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['pk'] = self.kwargs['pk']
        return kwargs

    def get_success_message(self, cleaned_data):
        return self.success_message % self.object.user_receiver.username


class ExchangeRequestList(LoginRequiredMixin, ListView):
    model = ExchangeRequest
    context_object_name = 'reqs'
    template_name = 'content/exchange_request_list.html'

    def get_queryset(self):
        # TODO: fix missing degree field in admin user
        user = CustomUser.objects.get(email=self.request.user.email)
        req = ExchangeRequest.objects.filter(user_receiver=user).filter(seen=False)
        return req.order_by('-date')

    # TODO: https://docs.djangoproject.com/en/3.1/topics/db/examples/
    # start from here
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = CustomUser.objects.get(email=self.request.user.email)
        context['notes'] = Note.objects.exclude(owner=user)
        context['exps'] = Experience.objects.exclude(owner=user)
        return context


class NotificationList(LoginRequiredMixin, ListView):
    model = Notification
    context_object_name = 'notifs'
    template_name = 'content/notifications_list.html'

    def get_queryset(self):
        # TODO: fix missing degree field in admin user
        user = CustomUser.objects.get(email=self.request.user.email)
        return Notification.objects.filter(user_receiver=user).order_by('-date')


@login_required
@require_POST
def buy_note(request):
    user = CustomUser.objects.get(email=request.user.email)
    id = request.POST.get('id', None)
    to_buy = Note.objects.filter(id=id).get()
    user.purchased_notes.add(to_buy)
    print(user.purchased_notes.all())
    # ctx = {'valid': valid, 'message': message}
    return HttpResponse(json.dumps({}), content_type='application/json')


@login_required
@require_POST
def manage_exchange(request):
    user = CustomUser.objects.get(email=request.user.email)
    id = request.POST.get('req', None)
    action = request.POST.get('action', None)
    exch_req = ExchangeRequest.objects.filter(id=id).get()
    if exch_req:
        if action == 'accept':
            exch_req.accepted = True
            exch_req.user_requester.purchased_notes.add(exch_req.requested_note)
            user.purchased_notes.add(exch_req.proposed_note)
        elif action == 'reject':
            exch_req.accepted = False
        exch_req.seen = True
        exch_req.save()
        Notification.objects.create(user_receiver=exch_req.user_requester, request=exch_req)
    return HttpResponse(json.dumps({'id': id}), content_type='application/json')


@login_required
@require_POST
def delete_notification(request):
    not_id = request.POST.get('id', None)
    n = Notification.objects.filter(id=not_id).get()
    if n:
        # n.request.delete()
        n.delete()
        return HttpResponse(json.dumps({"id": not_id}), content_type='application/json')
    return HttpResponseNotFound('<h1>Page not found</h1>')
