import json

from content.forms import AddNoteModelForm, AddExperienceModelForm, ExchangeRequestModelForm
from content.models import Note, Experience, Course, ExchangeRequest, Notification
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, CreateView, ListView
from django.views.generic.edit import UpdateView, DeleteView
from users.models import CustomUser


class ExperienceUpdate(UpdateView):
    model = Experience
    form_class = AddExperienceModelForm
    template_name = 'content/note_update_form.html'
    # success_url = '/books/'


class ExperienceDelete(DeleteView):
    model = Experience
    success_url = reverse_lazy('experiences')
    template_name = 'content/note_confirm_delete.html'


class ExperienceDetail(DetailView):
    model = Experience


class ExperienceCreate(LoginRequiredMixin, CreateView):
    form_class = AddExperienceModelForm
    template_name = 'content/note_add.html'
    success_url = reverse_lazy('experiences')

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


class NoteDelete(DeleteView):
    model = Note
    success_url = reverse_lazy('notes')


class NoteDetail(DetailView):
    model = Note

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs['pk']
        user = CustomUser.objects.get(email=self.request.user.email)
        context['purchased'] = True if user.purchased_notes.filter(id=id) else False
        return context


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


class NoteUpdate(UpdateView):
    model = Note
    form_class = AddNoteModelForm
    template_name_suffix = '_update_form'

    # success_url = '/books/'

    def get_form_kwargs(self):
        kwargs = super(NoteUpdate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class NoteCreate(LoginRequiredMixin, CreateView):
    form_class = AddNoteModelForm
    template_name = 'content/note_add.html'
    success_url = reverse_lazy('notes')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(NoteCreate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    # if request.method == 'POST':
    #     # create a form instance and populate it with data from the request:
    #     form = AddNoteModelForm(request.POST)
    #     # check whether it's valid:
    #     if form.is_valid():
    #         # process the data in form.cleaned_data as required
    #         # ...
    #         # redirect to a new URL:
    #         return HttpResponse('/thanks/')
    #
    # # if a GET (or any other method) we'll create a blank form
    # else:
    #     form = AddNoteModelForm()
    #
    # return render(request, 'content/note_add.html', {'form': form})


class CoursesListView(LoginRequiredMixin, ListView):
    model = Course
    context_object_name = 'courses_list'
    template_name = 'content/course_list.html'

    def get_queryset(self):
        # TODO: fix missing degree field in admin user
        print("email: %s \n" % self.request.user.email)
        user = CustomUser.objects.get(email=self.request.user.email)
        courses_qs = user.get_courses()
        courses = {}
        for course in courses_qs:
            courses[course] = (course.note_set.exclude(owner=user),
                               course.experience_set.exclude(owner=user))
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
    success_url = reverse_lazy('dashboard')
    success_message = "Exchange will be notified %s." \
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
        req = ExchangeRequest.objects.filter(user_receiver=user)
        return req

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
        return Notification.objects.filter(user_receiver=user)


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
    if exch_req and action == 'accept':
        exch_req.accepted = True
        exch_req.user_requester.purchased_notes.add(exch_req.requested_note)
        user.purchased_notes.add(exch_req.proposed_note)
        Notification.objects.create(user_receiver=exch_req.user_requester, request=exch_req)
    return HttpResponse(json.dumps({'id': id}), content_type='application/json')


@login_required
@require_POST
def delete_notification(request):
    not_id = request.POST.get('id', None)
    n = Notification.objects.get(id=not_id)
    if n:
        n.delete()
        return HttpResponse(json.dumps({}), content_type='application/json')
    return HttpResponseNotFound('<h1>Page not found</h1>')
